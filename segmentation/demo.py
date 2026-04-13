#!/usr/bin/env python3
"""
Demo script for Alzheimer's Classification and Weakly-Supervised Segmentation

This script demonstrates how to use the trained models for:
1. Classifying brain slices into Alzheimer's categories
2. Generating CAMs for visualization
3. Creating segmentation masks

Author: AI Assistant
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os
import argparse
from torchvision import transforms

from classifier import AlzheimerClassifier, CAMGenerator
from cam_processing import CAMProcessor
from unet import LightUNet
from data_loader import get_transforms

def load_models(classifier_path, unet_path=None):
    """Load trained models"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load classifier
    classifier = AlzheimerClassifier(num_classes=4, pretrained=True)
    classifier.load_state_dict(torch.load(classifier_path, map_location=device))
    classifier.to(device)
    classifier.eval()
    
    # Load U-Net if provided
    unet = None
    if unet_path and os.path.exists(unet_path):
        unet = LightUNet(n_channels=3, n_classes=1)
        unet.load_state_dict(torch.load(unet_path, map_location=device))
        unet.to(device)
        unet.eval()
    
    return classifier, unet, device

def preprocess_image(image_path, target_size=224):
    """Preprocess image for model input"""
    # Load image
    image = Image.open(image_path).convert('RGB')
    
    # Get transform
    _, val_transform = get_transforms(target_size)
    
    # Transform image
    image_tensor = val_transform(image)
    
    # Also return original for visualization
    image_np = np.array(image.resize((target_size, target_size)))
    
    return image_tensor, image_np

def predict_class(classifier, image_tensor, device):
    """Predict Alzheimer's class"""
    class_names = ['No Impairment', 'Very Mild Impairment', 'Mild Impairment', 'Moderate Impairment']
    
    with torch.no_grad():
        image_batch = image_tensor.unsqueeze(0).to(device)
        outputs = classifier(image_batch)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    
    return predicted_class, class_names[predicted_class], confidence, probabilities[0].cpu().numpy()

def generate_cam_visualization(classifier, image_tensor, device, predicted_class):
    """Generate and visualize CAM"""
    cam_generator = CAMGenerator(classifier)
    
    # Generate CAM
    image_batch = image_tensor.unsqueeze(0).to(device)
    cam = cam_generator.generate_cam(image_batch, class_idx=predicted_class)
    
    return cam

def generate_segmentation(unet, image_tensor, device):
    """Generate segmentation mask using U-Net"""
    if unet is None:
        return None
    
    with torch.no_grad():
        image_batch = image_tensor.unsqueeze(0).to(device)
        output = unet(image_batch)
        segmentation = torch.sigmoid(output).cpu().squeeze().numpy()
    
    return segmentation

def visualize_results(image_np, predicted_class, class_name, confidence, probabilities, 
                     cam, segmentation=None, save_path=None):
    """Create comprehensive visualization"""
    
    class_names = ['No Impairment', 'Very Mild Impairment', 'Mild Impairment', 'Moderate Impairment']
    
    if segmentation is not None:
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
    else:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
    
    # Original image
    axes[0].imshow(image_np)
    axes[0].set_title(f'Original Image\nPredicted: {class_name}\nConfidence: {confidence:.3f}')
    axes[0].axis('off')
    
    # Class probabilities
    axes[1].bar(range(len(class_names)), probabilities)
    axes[1].set_title('Class Probabilities')
    axes[1].set_xticks(range(len(class_names)))
    axes[1].set_xticklabels(class_names, rotation=45, ha='right')
    axes[1].set_ylabel('Probability')
    axes[1].grid(True, alpha=0.3)
    
    # CAM heatmap
    axes[2].imshow(image_np)
    im = axes[2].imshow(cam, alpha=0.6, cmap='jet')
    axes[2].set_title('Class Activation Map (CAM)')
    axes[2].axis('off')
    plt.colorbar(im, ax=axes[2])
    
    # CAM only
    axes[3].imshow(cam, cmap='jet')
    axes[3].set_title('CAM Heatmap')
    axes[3].axis('off')
    
    if segmentation is not None:
        # Segmentation overlay
        axes[4].imshow(image_np)
        axes[4].imshow(segmentation, alpha=0.5, cmap='Reds')
        axes[4].set_title('Segmentation Overlay')
        axes[4].axis('off')
        
        # Segmentation mask
        axes[5].imshow(segmentation, cmap='gray')
        axes[5].set_title('Segmentation Mask')
        axes[5].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {save_path}")
    
    plt.show()

def process_image(image_path, classifier_path, unet_path=None, save_visualization=True):
    """Process a single image through the complete pipeline"""
    
    print(f"Processing: {image_path}")
    
    # Load models
    classifier, unet, device = load_models(classifier_path, unet_path)
    
    # Preprocess image
    image_tensor, image_np = preprocess_image(image_path)
    
    # Predict class
    predicted_class, class_name, confidence, probabilities = predict_class(
        classifier, image_tensor, device
    )
    
    # Generate CAM
    cam = generate_cam_visualization(classifier, image_tensor, device, predicted_class)
    
    # Generate segmentation (if U-Net is available)
    segmentation = generate_segmentation(unet, image_tensor, device)
    
    # Print results
    print(f"Classification Results:")
    print(f"├── Predicted Class: {class_name}")
    print(f"├── Confidence: {confidence:.3f}")
    print(f"└── All Probabilities:")
    class_names = ['No Impairment', 'Very Mild Impairment', 'Mild Impairment', 'Moderate Impairment']
    for i, (name, prob) in enumerate(zip(class_names, probabilities)):
        print(f"    {name}: {prob:.3f}")
    
    if segmentation is not None:
        print(f"Segmentation Generated: ✅")
    else:
        print(f"Segmentation: ❌ (U-Net model not available)")
    
    # Visualize results
    if save_visualization:
        save_path = f"demo_results_{os.path.basename(image_path).replace('.jpg', '.png')}"
    else:
        save_path = None
    
    visualize_results(
        image_np, predicted_class, class_name, confidence, 
        probabilities, cam, segmentation, save_path
    )
    
    return {
        'predicted_class': predicted_class,
        'class_name': class_name,
        'confidence': confidence,
        'probabilities': probabilities,
        'cam': cam,
        'segmentation': segmentation
    }

def demo_batch_processing(data_dir, classifier_path, unet_path=None, num_samples=5):
    """Demo batch processing on multiple images"""
    
    print(f"\nDemo: Batch processing {num_samples} random samples")
    print("="*60)
    
    # Collect all image paths
    all_images = []
    for class_dir in os.listdir(data_dir):
        class_path = os.path.join(data_dir, class_dir)
        if os.path.isdir(class_path):
            for img_name in os.listdir(class_path):
                if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    all_images.append(os.path.join(class_path, img_name))
    
    # Select random samples
    selected_images = np.random.choice(all_images, min(num_samples, len(all_images)), replace=False)
    
    results = []
    for img_path in selected_images:
        print(f"\n📸 Processing: {os.path.basename(img_path)}")
        result = process_image(img_path, classifier_path, unet_path, save_visualization=False)
        results.append({
            'image_path': img_path,
            'result': result
        })
    
    # Summary
    print(f"\n📊 Batch Processing Summary:")
    print("="*40)
    for i, item in enumerate(results):
        img_name = os.path.basename(item['image_path'])
        result = item['result']
        print(f"{i+1}. {img_name}")
        print(f"   ├── Class: {result['class_name']}")
        print(f"   └── Confidence: {result['confidence']:.3f}")

def main():
    parser = argparse.ArgumentParser(description='Demo for Alzheimer\'s Classification and Segmentation')
    parser.add_argument('--image', type=str, help='Path to input image')
    parser.add_argument('--classifier', type=str, default='best_alzheimer_classifier.pth', 
                       help='Path to trained classifier model')
    parser.add_argument('--unet', type=str, default='best_unet_segmentation.pth',
                       help='Path to trained U-Net model')
    parser.add_argument('--batch', action='store_true', help='Run batch demo on test data')
    parser.add_argument('--data_dir', type=str, default='data/test', help='Directory for batch demo')
    parser.add_argument('--num_samples', type=int, default=5, help='Number of samples for batch demo')
    
    args = parser.parse_args()
    
    # Check if models exist
    if not os.path.exists(args.classifier):
        print(f"❌ Classifier model not found: {args.classifier}")
        print("Please run the training pipeline first!")
        return
    
    unet_path = args.unet if os.path.exists(args.unet) else None
    if unet_path is None:
        print(f"⚠️  U-Net model not found: {args.unet}")
        print("Segmentation will not be available")
    
    if args.batch:
        # Batch processing demo
        demo_batch_processing(args.data_dir, args.classifier, unet_path, args.num_samples)
    
    elif args.image:
        # Single image processing
        if not os.path.exists(args.image):
            print(f"❌ Image not found: {args.image}")
            return
        
        process_image(args.image, args.classifier, unet_path)
    
    else:
        # Interactive demo with sample images
        print("🎯 Interactive Demo Mode")
        print("="*30)
        
        # Try to find sample images
        sample_dirs = ['data/test', 'data/train']
        sample_image = None
        
        for sample_dir in sample_dirs:
            if os.path.exists(sample_dir):
                for class_dir in os.listdir(sample_dir):
                    class_path = os.path.join(sample_dir, class_dir)
                    if os.path.isdir(class_path):
                        images = [f for f in os.listdir(class_path) 
                                if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                        if images:
                            sample_image = os.path.join(class_path, images[0])
                            break
                if sample_image:
                    break
        
        if sample_image:
            print(f"Processing sample image: {sample_image}")
            process_image(sample_image, args.classifier, unet_path)
        else:
            print("❌ No sample images found. Please provide --image or --batch option.")

if __name__ == "__main__":
    main()