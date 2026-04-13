#!/usr/bin/env python3
"""
Interactive tester for the Alzheimer's Risk Prediction Pipeline
"""

import os
from alzheimer_risk_pipeline import AlzheimerRiskPipeline, format_risk_report

def list_available_images():
    """List all available images by category"""
    
    print("📁 AVAILABLE MRI IMAGES:")
    print("=" * 40)
    
    base_path = "data/train"
    categories = ["No Impairment", "Very Mild Impairment", "Mild Impairment", "Moderate Impairment"]
    
    all_images = {}
    
    for category in categories:
        category_path = os.path.join(base_path, category)
        if os.path.exists(category_path):
            images = [f for f in os.listdir(category_path) if f.endswith('.jpg')][:10]  # Show first 10
            all_images[category] = images
            
            print(f"\n🔍 {category}:")
            for i, img in enumerate(images):
                print(f"   {i+1:2d}. {img}")
            
            if len(os.listdir(category_path)) > 10:
                print(f"   ... and {len(os.listdir(category_path)) - 10} more")
    
    return all_images

def test_risk_prediction(pipeline, image_path, category_name):
    """Test risk prediction on a specific image"""
    
    print(f"🧠 ALZHEIMER'S RISK PREDICTION")
    print("=" * 35)
    print(f"📁 Image: {os.path.basename(image_path)}")
    print(f"📍 Category: {category_name}")
    
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
    
    try:
        # Get risk prediction
        print(f"\n🔧 Processing with quantum+neural pipeline...")
        prediction = pipeline.predict_risk(image_path, category_name)
        
        # Generate formatted report
        report = format_risk_report(prediction)
        print(report)
        
        return prediction
        
    except Exception as e:
        print(f"❌ Error in risk prediction: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_predictions(pipeline):
    """Compare predictions across different categories"""
    
    print(f"\n🔍 COMPARATIVE RISK ANALYSIS")
    print("=" * 35)
    
    categories = ["No Impairment", "Very Mild Impairment", "Mild Impairment", "Moderate Impairment"]
    results = []
    
    for category in categories:
        category_path = os.path.join("data/train", category)
        if os.path.exists(category_path):
            images = [f for f in os.listdir(category_path) if f.endswith('.jpg')]
            if images:
                # Test first image from each category
                image_path = os.path.join(category_path, images[0])
                
                print(f"\n📊 Testing {category}...")
                prediction = pipeline.predict_risk(image_path, category, uncertainty_samples=20)
                
                if prediction:
                    results.append({
                        'category': category,
                        'image': images[0],
                        'risk_pct': prediction['risk_percentage'],
                        'uncertainty': prediction['uncertainty_band'],
                        'ees_score': prediction['ees_score']
                    })
                    
                    print(f"   Risk: {prediction['risk_percentage']:.1f}% ± {prediction['uncertainty_band']:.1f}%")
                    print(f"   EES: {prediction['ees_score']:.4f} bits")
    
    # Summary comparison
    if results:
        print(f"\n📈 COMPARATIVE SUMMARY:")
        print("┌─" + "─"*25 + "┬─" + "─"*12 + "┬─" + "─"*12 + "┬─" + "─"*10 + "┐")
        print("│ Category                  │ Risk (%)     │ EES Score    │ Sample     │")
        print("├─" + "─"*25 + "┼─" + "─"*12 + "┼─" + "─"*12 + "┼─" + "─"*10 + "┤")
        
        for result in results:
            risk_str = f"{result['risk_pct']:.1f}±{result['uncertainty']:.1f}"
            ees_str = f"{result['ees_score']:.4f}"
            sample_str = result['image'][:8] + "..."
            
            print(f"│ {result['category']:<25} │ {risk_str:<12} │ {ees_str:<12} │ {sample_str:<10} │")
        
        print("└─" + "─"*25 + "┴─" + "─"*12 + "┴─" + "─"*12 + "┴─" + "─"*10 + "┘")
        
        # Analysis
        risks = [r['risk_pct'] for r in results]
        print(f"\n📊 ANALYSIS:")
        print(f"   Risk range: {min(risks):.1f}% - {max(risks):.1f}%")
        print(f"   Risk spread: {max(risks) - min(risks):.1f}%")
        print(f"   Pipeline discriminates between categories: {'✅ Yes' if max(risks) - min(risks) > 10 else '⚠️  Limited'}")

def interactive_mode():
    """Interactive mode for testing the pipeline"""
    
    print("🧠 INTERACTIVE ALZHEIMER'S RISK PIPELINE TESTER")
    print("=" * 50)
    
    # Initialize pipeline
    print("🔧 Initializing risk prediction pipeline...")
    pipeline = AlzheimerRiskPipeline()
    
    # Check if trained model exists
    model_path = "alzheimer_risk_model.pth"
    if not os.path.exists(model_path):
        print("⚠️  No trained model found. Training a quick demo model...")
        
        # Quick training for demo
        from alzheimer_risk_pipeline import AlzheimerRiskDataset
        train_dataset = AlzheimerRiskDataset("data/train", max_samples_per_category=10)
        pipeline.train(train_dataset, epochs=3, batch_size=2)
        pipeline.save_model(model_path)
        print("✓ Demo model trained and saved")
    else:
        pipeline.load_model(model_path)
        print("✓ Loaded existing trained model")
    
    while True:
        print(f"\n🎯 TESTING OPTIONS:")
        print(f"   1. List available images")
        print(f"   2. Test specific image")
        print(f"   3. Test by category and number")
        print(f"   4. Compare all categories")
        print(f"   5. Exit")
        
        try:
            choice = input(f"\n👉 Select option (1-5): ").strip()
            
            if choice == "1":
                list_available_images()
                
            elif choice == "2":
                image_path = input(f"\n📁 Enter image path: ").strip()
                category = input(f"📋 Enter category (No Impairment/Very Mild Impairment/Mild Impairment/Moderate Impairment): ").strip()
                
                if image_path and category:
                    test_risk_prediction(pipeline, image_path, category)
                
            elif choice == "3":
                print(f"\nAvailable categories:")
                categories = ["No Impairment", "Very Mild Impairment", "Mild Impairment", "Moderate Impairment"]
                for i, cat in enumerate(categories):
                    print(f"   {i+1}. {cat}")
                
                try:
                    cat_choice = int(input(f"Select category (1-4): ")) - 1
                    if 0 <= cat_choice < len(categories):
                        category = categories[cat_choice]
                        
                        # List images in that category
                        category_path = os.path.join("data/train", category)
                        if os.path.exists(category_path):
                            images = [f for f in os.listdir(category_path) if f.endswith('.jpg')]
                            
                            print(f"\nFirst 10 images in {category}:")
                            for i, img in enumerate(images[:10]):
                                print(f"   {i+1:2d}. {img}")
                            
                            img_choice = int(input(f"Select image number (1-{min(10, len(images))}): ")) - 1
                            if 0 <= img_choice < len(images):
                                image_path = os.path.join(category_path, images[img_choice])
                                test_risk_prediction(pipeline, image_path, category)
                            else:
                                print("❌ Invalid image number")
                        else:
                            print(f"❌ Category path not found: {category_path}")
                    else:
                        print("❌ Invalid category number")
                except ValueError:
                    print("❌ Please enter a valid number")
                
            elif choice == "4":
                compare_predictions(pipeline)
                
            elif choice == "5":
                print(f"👋 Goodbye!")
                break
                
            else:
                print(f"❌ Invalid choice. Please select 1-5.")
                
        except KeyboardInterrupt:
            print(f"\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def quick_test(image_path, category):
    """Quick test for command line usage"""
    
    print(f"🚀 QUICK RISK ASSESSMENT")
    
    # Initialize and load model
    pipeline = AlzheimerRiskPipeline()
    
    model_path = "alzheimer_risk_model.pth"
    if os.path.exists(model_path):
        pipeline.load_model(model_path)
    else:
        print("⚠️  No trained model found. Please run interactive mode first.")
        return
    
    # Test prediction
    test_risk_prediction(pipeline, image_path, category)

def main():
    """Main function"""
    
    import sys
    
    if len(sys.argv) >= 3:
        # Command line mode: python test_risk_pipeline.py <image_path> <category>
        image_path = sys.argv[1]
        category = sys.argv[2]
        quick_test(image_path, category)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()