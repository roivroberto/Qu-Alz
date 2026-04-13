import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F

class AlzheimerClassifier(nn.Module):
    """ResNet-18 based classifier for Alzheimer's slice classification"""
    
    def __init__(self, num_classes=4, pretrained=True):
        super(AlzheimerClassifier, self).__init__()
        
        # Load ResNet-18
        if pretrained:
            self.backbone = models.resnet18(weights='DEFAULT')
        else:
            self.backbone = models.resnet18(weights=None)
        
        # Get the number of features in the final layer
        num_features = self.backbone.fc.in_features
        
        # Replace the final fully connected layer
        self.backbone.fc = nn.Linear(num_features, num_classes)
        
        # Store the feature extractor (everything except the final fc layer)
        self.features = nn.Sequential(*list(self.backbone.children())[:-1])
        self.classifier = self.backbone.fc
        
    def forward(self, x):
        # Extract features
        features = self.features(x)
        features = torch.flatten(features, 1)
        
        # Classification
        logits = self.classifier(features)
        
        return logits
    
    def get_features(self, x):
        """Extract features before the final classification layer"""
        with torch.no_grad():
            features = self.features(x)
            features = torch.flatten(features, 1)
        return features
    
    def get_conv_features(self, x):
        """Get the last convolutional features for CAM generation"""
        with torch.no_grad():
            # Forward through all layers except avgpool and fc
            conv_layers = nn.Sequential(*list(self.backbone.children())[:-2])
            conv_features = conv_layers(x)
        return conv_features

class CAMGenerator:
    """Class Activation Map generator for weakly supervised segmentation"""
    
    def __init__(self, model, target_layer=None):
        self.model = model
        self.model.eval()
        
        # Get the target layer (last conv layer by default)
        if target_layer is None:
            # For ResNet-18, this is layer4
            self.target_layer = self.model.backbone.layer4
        else:
            self.target_layer = target_layer
            
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer.register_forward_hook(self.save_activation)
        self.target_layer.register_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        self.activations = output
    
    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]
    
    def generate_cam(self, input_tensor, class_idx=None):
        """Generate Class Activation Map"""
        # Forward pass
        logits = self.model(input_tensor)
        
        if class_idx is None:
            class_idx = torch.argmax(logits, dim=1)
        
        # Backward pass
        self.model.zero_grad()
        class_loss = logits[0, class_idx]
        class_loss.backward()
        
        # Generate CAM
        gradients = self.gradients[0]  # [C, H, W]
        activations = self.activations[0]  # [C, H, W]
        
        # Global average pooling on gradients
        weights = torch.mean(gradients, dim=[1, 2])  # [C]
        
        # Weighted sum of activations
        cam = torch.zeros(activations.shape[1:], dtype=torch.float32)
        for i, w in enumerate(weights):
            cam += w * activations[i, :, :]
        
        # Apply ReLU
        cam = F.relu(cam)
        
        # Normalize to [0, 1]
        if cam.max() > 0:
            cam = cam / cam.max()
        
        return cam.detach().cpu().numpy()
    
    def generate_gradcam(self, input_tensor, class_idx=None):
        """Generate Grad-CAM"""
        return self.generate_cam(input_tensor, class_idx)

def get_pretrained_classifier(num_classes=4, model_path=None):
    """Get a pretrained classifier model"""
    import os
    model = AlzheimerClassifier(num_classes=num_classes, pretrained=True)
    
    if model_path and os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
        print(f"Loaded model from {model_path}")
    
    return model