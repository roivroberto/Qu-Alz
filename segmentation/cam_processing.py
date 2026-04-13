import numpy as np
import cv2
from scipy import ndimage
from scipy.ndimage import binary_opening, binary_closing
import torch
import torch.nn.functional as F

class CAMProcessor:
    """Process CAMs to generate pseudo-masks for weakly supervised segmentation"""
    
    def __init__(self, threshold_percentile=80, min_area=100):
        self.threshold_percentile = threshold_percentile
        self.min_area = min_area
    
    def resize_cam(self, cam, target_size):
        """Resize CAM to target image size"""
        if isinstance(target_size, int):
            target_size = (target_size, target_size)
        
        # Convert to uint8 for OpenCV
        cam_uint8 = (cam * 255).astype(np.uint8)
        
        # Resize using bilinear interpolation
        resized = cv2.resize(cam_uint8, target_size, interpolation=cv2.INTER_LINEAR)
        
        # Convert back to float
        return resized.astype(np.float32) / 255.0
    
    def threshold_cam(self, cam, percentile=None):
        """Threshold CAM to keep top percentile values"""
        if percentile is None:
            percentile = self.threshold_percentile
            
        threshold = np.percentile(cam.flatten(), percentile)
        binary_mask = (cam >= threshold).astype(np.float32)
        
        return binary_mask, threshold
    
    def clean_mask(self, mask, kernel_size=3, min_area=None):
        """Clean binary mask using morphological operations"""
        if min_area is None:
            min_area = self.min_area
            
        # Convert to uint8 for OpenCV operations
        mask_uint8 = (mask * 255).astype(np.uint8)
        
        # Morphological operations
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        # Opening to remove small noise
        opened = cv2.morphologyEx(mask_uint8, cv2.MORPH_OPEN, kernel)
        
        # Closing to fill small holes
        cleaned = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        
        # Remove small connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned)
        
        final_mask = np.zeros_like(cleaned)
        for i in range(1, num_labels):  # Skip background (label 0)
            if stats[i, cv2.CC_STAT_AREA] >= min_area:
                final_mask[labels == i] = 255
        
        return final_mask.astype(np.float32) / 255.0
    
    def apply_crf(self, image, mask, num_iterations=5):
        """Apply Conditional Random Field refinement (simplified version)"""
        # This is a simplified CRF implementation
        # For production, consider using pydensecrf library
        
        # Ensure image is in correct format for OpenCV
        if image.dtype != np.uint8:
            image = (image * 255).astype(np.uint8)
        
        # Convert image to grayscale for edge detection
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Detect edges
        edges = cv2.Canny(gray, 50, 150)
        edge_weights = edges.astype(np.float32) / 255.0
        
        # Simple edge-aware smoothing
        refined_mask = mask.copy()
        for _ in range(num_iterations):
            # Apply Gaussian filter with edge-aware weights
            smoothed = cv2.GaussianBlur(refined_mask, (5, 5), 1.0)
            
            # Preserve edges
            refined_mask = refined_mask * edge_weights + smoothed * (1 - edge_weights)
            
            # Re-threshold
            refined_mask = (refined_mask > 0.5).astype(np.float32)
        
        return refined_mask
    
    def process_cam_to_mask(self, cam, original_image=None, target_size=224, 
                           use_crf=True, return_intermediate=False):
        """
        Complete pipeline to convert CAM to refined pseudo-mask
        
        Args:
            cam: Class activation map (H, W)
            original_image: Original image for CRF (optional)
            target_size: Target size for resizing
            use_crf: Whether to apply CRF refinement
            return_intermediate: Return intermediate results
        
        Returns:
            final_mask: Refined binary mask
            intermediate_results: Dict with intermediate results (if requested)
        """
        intermediate = {}
        
        # Step 1: Resize CAM to target size
        if isinstance(target_size, tuple):
            h, w = target_size
        else:
            h = w = target_size
            
        resized_cam = self.resize_cam(cam, (w, h))
        if return_intermediate:
            intermediate['resized_cam'] = resized_cam
        
        # Step 2: Threshold CAM
        binary_mask, threshold = self.threshold_cam(resized_cam)
        if return_intermediate:
            intermediate['thresholded_mask'] = binary_mask
            intermediate['threshold'] = threshold
        
        # Step 3: Clean with morphological operations
        cleaned_mask = self.clean_mask(binary_mask)
        if return_intermediate:
            intermediate['cleaned_mask'] = cleaned_mask
        
        # Step 4: Apply CRF refinement (if requested and image is provided)
        final_mask = cleaned_mask
        if use_crf and original_image is not None:
            # Resize original image to match mask size
            if original_image.shape[:2] != (h, w):
                resized_image = cv2.resize(original_image, (w, h))
            else:
                resized_image = original_image
            
            final_mask = self.apply_crf(resized_image, cleaned_mask)
            if return_intermediate:
                intermediate['crf_refined_mask'] = final_mask
        
        if return_intermediate:
            return final_mask, intermediate
        else:
            return final_mask

def generate_pseudo_masks_batch(cam_generator, data_loader, processor, 
                               device, save_masks=True, output_dir='pseudo_masks'):
    """
    Generate pseudo-masks for a batch of images using CAMs
    
    Args:
        cam_generator: CAMGenerator instance
        data_loader: DataLoader with images
        processor: CAMProcessor instance
        device: Device to run on
        save_masks: Whether to save masks to disk
        output_dir: Directory to save masks
    
    Returns:
        pseudo_masks: Dictionary mapping image paths to masks
    """
    import os
    
    if save_masks:
        os.makedirs(output_dir, exist_ok=True)
    
    pseudo_masks = {}
    cam_generator.model.to(device)
    
    print("Generating pseudo-masks from CAMs...")
    
    for batch_idx, (images, labels, img_paths) in enumerate(data_loader):
        images = images.to(device)
        
        for i, (image, label, img_path) in enumerate(zip(images, labels, img_paths)):
            # Generate CAM for this image
            cam = cam_generator.generate_cam(
                image.unsqueeze(0), 
                class_idx=label.item()
            )
            
            # Convert image tensor back to numpy for CRF
            image_np = image.cpu().numpy().transpose(1, 2, 0)
            
            # Denormalize image
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            image_np = image_np * std + mean
            image_np = np.clip(image_np, 0, 1)
            
            # Process CAM to pseudo-mask
            pseudo_mask = processor.process_cam_to_mask(
                cam, 
                original_image=image_np,
                target_size=224
            )
            
            pseudo_masks[img_path] = pseudo_mask
            
            # Save mask if requested
            if save_masks:
                mask_name = os.path.basename(img_path).replace('.jpg', '_mask.png')
                mask_path = os.path.join(output_dir, mask_name)
                cv2.imwrite(mask_path, (pseudo_mask * 255).astype(np.uint8))
        
        if (batch_idx + 1) % 10 == 0:
            print(f"Processed {(batch_idx + 1) * len(images)} images...")
    
    print(f"Generated {len(pseudo_masks)} pseudo-masks")
    return pseudo_masks