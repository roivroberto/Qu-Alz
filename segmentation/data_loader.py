import os
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms
import numpy as np

class AlzheimerDataset(Dataset):
    """Dataset for Alzheimer's classification from slice images"""
    
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        
        # Class mapping
        self.class_to_idx = {
            'No Impairment': 0,
            'Very Mild Impairment': 1, 
            'Mild Impairment': 2,
            'Moderate Impairment': 3
        }
        
        self.idx_to_class = {v: k for k, v in self.class_to_idx.items()}
        
        # Load all image paths and labels
        self.samples = []
        for class_name in self.class_to_idx.keys():
            class_dir = os.path.join(data_dir, class_name)
            if os.path.exists(class_dir):
                for img_name in os.listdir(class_dir):
                    if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        img_path = os.path.join(class_dir, img_name)
                        label = self.class_to_idx[class_name]
                        self.samples.append((img_path, label))
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        
        # Load image
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
            
        return image, label, img_path

def get_transforms(input_size=224):
    """Get data transforms for training and validation"""
    
    train_transform = transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform

def get_data_loaders(train_dir, test_dir, batch_size=32, input_size=224):
    """Create data loaders for training and testing"""
    
    train_transform, val_transform = get_transforms(input_size)
    
    train_dataset = AlzheimerDataset(train_dir, transform=train_transform)
    test_dataset = AlzheimerDataset(test_dir, transform=val_transform)
    
    # Use pin_memory only if CUDA is available
    import torch
    pin_memory = torch.cuda.is_available()
    num_workers = 0 if not torch.cuda.is_available() else 4  # Reduce workers for CPU
    
    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=num_workers,
        pin_memory=pin_memory
    )
    
    test_loader = DataLoader(
        test_dataset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=num_workers,
        pin_memory=pin_memory
    )
    
    return train_loader, test_loader, train_dataset.class_to_idx