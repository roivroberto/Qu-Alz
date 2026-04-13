#!/usr/bin/env python3
"""
Training script for Alzheimer's Risk Prediction Model
"""

import os
import argparse
from alzheimer_risk_pipeline import AlzheimerRiskPipeline, AlzheimerRiskDataset

def train_model(data_dir: str, output_path: str, max_samples: int = 50, epochs: int = 20, batch_size: int = 8):
    """
    Train the Alzheimer's risk prediction model
    
    Args:
        data_dir: Path to training data
        output_path: Where to save the trained model
        max_samples: Maximum samples per category
        epochs: Number of training epochs
        batch_size: Training batch size
    """
    
    print("🧠 ALZHEIMER'S RISK MODEL TRAINING")
    print("=" * 40)
    
    # Create dataset
    print(f"\n📊 Loading dataset...")
    print(f"   Data directory: {data_dir}")
    print(f"   Max samples per category: {max_samples}")
    
    dataset = AlzheimerRiskDataset(data_dir, max_samples_per_category=max_samples)
    
    if len(dataset) == 0:
        print("❌ No data found! Check your data directory.")
        return
    
    # Initialize pipeline
    print(f"\n🔧 Initializing pipeline...")
    pipeline = AlzheimerRiskPipeline()
    
    # Train model
    print(f"\n🚀 Starting training...")
    print(f"   Epochs: {epochs}")
    print(f"   Batch size: {batch_size}")
    print(f"   Total samples: {len(dataset)}")
    
    pipeline.train(dataset, epochs=epochs, batch_size=batch_size)
    
    # Save model
    print(f"\n💾 Saving model to {output_path}...")
    pipeline.save_model(output_path)
    
    print(f"\n✅ Training complete!")
    print(f"   Model saved: {output_path}")
    print(f"   Ready for risk prediction!")
    
    # Quick validation test
    print(f"\n🧪 Quick validation test...")
    
    # Find a test sample
    categories = ["No Impairment", "Moderate Impairment"]
    for category in categories:
        category_path = os.path.join(data_dir, category)
        if os.path.exists(category_path):
            images = [f for f in os.listdir(category_path) if f.endswith('.jpg')]
            if images:
                test_image = os.path.join(category_path, images[0])
                
                print(f"   Testing {category}: {images[0]}")
                prediction = pipeline.predict_risk(test_image, category, uncertainty_samples=10)
                
                if prediction:
                    print(f"   ✓ Risk: {prediction['risk_percentage']:.1f}% ± {prediction['uncertainty_band']:.1f}%")
                    print(f"   ✓ EES: {prediction['ees_score']:.4f} bits")
                break

def main():
    """Main training function"""
    
    parser = argparse.ArgumentParser(description="Train Alzheimer's Risk Prediction Model")
    parser.add_argument("--data_dir", default="data/train", help="Path to training data directory")
    parser.add_argument("--output", default="alzheimer_risk_model.pth", help="Output model path")
    parser.add_argument("--max_samples", type=int, default=50, help="Max samples per category")
    parser.add_argument("--epochs", type=int, default=20, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Training batch size")
    
    args = parser.parse_args()
    
    # Validate data directory
    if not os.path.exists(args.data_dir):
        print(f"❌ Data directory not found: {args.data_dir}")
        return
    
    # Train model
    train_model(
        data_dir=args.data_dir,
        output_path=args.output,
        max_samples=args.max_samples,
        epochs=args.epochs,
        batch_size=args.batch_size
    )

if __name__ == "__main__":
    main()