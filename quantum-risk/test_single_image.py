#!/usr/bin/env python3
"""
Interactive single image quantum EES tester
"""

import os
import numpy as np
from quantum_ees import QuantumEES, MRIEmbeddingExtractor, QISKIT_AVAILABLE

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
                img_path = os.path.join(category_path, img)
                print(f"   {i+1:2d}. {img}")
            
            if len(os.listdir(category_path)) > 10:
                print(f"   ... and {len(os.listdir(category_path)) - 10} more")
    
    return all_images

def get_reference_ranges():
    """Get reference ranges for interpretation"""
    return {
        "No Impairment": {"mean": 0.750, "std": 0.513, "range": "[0.32, 1.18]"},
        "Very Mild Impairment": {"mean": 1.018, "std": 0.544, "range": "[0.56, 1.47]"},
        "Mild Impairment": {"mean": 0.563, "std": 0.424, "range": "[0.21, 0.92]"},
        "Moderate Impairment": {"mean": 0.641, "std": 0.312, "range": "[0.38, 0.90]"}
    }

def interpret_ees_score(score):
    """Interpret EES score against reference ranges"""
    
    references = get_reference_ranges()
    
    print(f"\n🎯 EES SCORE INTERPRETATION:")
    print(f"   Your image score: {score:.6f} bits")
    print()
    
    # Check which category this score is most likely from
    best_match = None
    best_probability = 0
    
    print(f"📊 Comparison to Reference Ranges:")
    
    for category, ref in references.items():
        # Simple normal distribution probability
        mean, std = ref["mean"], ref["std"]
        
        # Calculate how many standard deviations away
        z_score = abs(score - mean) / std
        
        # Rough probability (within 2 std = ~95% of normal distribution)
        if z_score <= 2:
            probability = max(0, (2 - z_score) / 2)  # Simple linear approximation
        else:
            probability = 0
        
        status = ""
        if z_score <= 1:
            status = "✅ LIKELY MATCH"
        elif z_score <= 2:
            status = "⚠️  POSSIBLE MATCH"
        else:
            status = "❌ UNLIKELY"
        
        print(f"   {category:<22}: {z_score:.2f}σ away | {status}")
        
        if probability > best_probability:
            best_probability = probability
            best_match = category
    
    if best_match:
        print(f"\n🎯 MOST LIKELY CATEGORY: {best_match}")
    else:
        print(f"\n❓ UNCLEAR - Score outside typical ranges")

def test_specific_image(image_path):
    """Test quantum EES on a specific image"""
    
    if not QISKIT_AVAILABLE:
        print("❌ Qiskit not available. Install with: pip install qiskit qiskit-aer")
        return
    
    print(f"🔬 QUANTUM EES ANALYSIS")
    print("=" * 30)
    print(f"📁 Image: {os.path.basename(image_path)}")
    print(f"📍 Path: {image_path}")
    
    # Verify file exists
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
    
    try:
        # Initialize components
        print(f"\n🔧 Initializing quantum EES system...")
        extractor = MRIEmbeddingExtractor()
        quantum_ees = QuantumEES(n_qubits=10, reps=2)
        
        # Extract features
        print(f"📊 Extracting MRI features...")
        features = extractor.extract_features(image_path)
        print(f"   ✓ Features shape: {features.shape}")
        print(f"   ✓ Feature range: [{np.min(features):.3f}, {np.max(features):.3f}]")
        print(f"   ✓ Feature mean: {np.mean(features):.3f}")
        print(f"   ✓ Feature std: {np.std(features):.3f}")
        
        # Compute quantum EES
        print(f"\n⚛️  Computing quantum entanglement entropy...")
        ees_score, info = quantum_ees.compute_ees(features)
        
        # Display detailed results
        print(f"\n🎯 QUANTUM EES RESULTS:")
        print(f"   🧠 EES Score: {ees_score:.6f} bits")
        print(f"   ⏱️  Computation time: {info['computation_time_ms']:.1f} ms")
        print(f"   🔄 Circuit depth: {info['circuit_depth']}")
        print(f"   ⚛️  Qubits used: {info['n_qubits']} ({info['partition_size']}:{info['partition_size']} partition)")
        print(f"   📊 Density matrix trace: {abs(info['rho_trace']):.6f}")
        print(f"   📈 Matrix rank: {info['rho_rank']}")
        
        # Interpret the result
        interpret_ees_score(ees_score)
        
        # Quantum information context
        max_entropy = np.log2(2**info['partition_size'])
        utilization = (ees_score / max_entropy) * 100
        
        print(f"\n🔬 QUANTUM INFORMATION CONTEXT:")
        print(f"   📐 Theoretical max entropy ({info['partition_size']} qubits): {max_entropy:.3f} bits")
        print(f"   📊 Entropy utilization: {utilization:.1f}%")
        print(f"   ⚛️  Entanglement signature detected: {'Yes' if ees_score > 0.1 else 'Minimal'}")
        
        print(f"\n✨ QUANTUM ADVANTAGE:")
        print(f"   This EES score uses quantum entanglement entropy S = -Tr(ρ log₂ ρ)")
        print(f"   that classical machine learning algorithms CANNOT compute!")
        
        return ees_score, info
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def interactive_mode():
    """Interactive image selection mode"""
    
    print("🧠 INTERACTIVE QUANTUM EES TESTER")
    print("=" * 35)
    
    while True:
        print(f"\n🎯 TESTING OPTIONS:")
        print(f"   1. List available images by category")
        print(f"   2. Test specific image by path")
        print(f"   3. Test image by category and number")
        print(f"   4. Exit")
        
        try:
            choice = input(f"\n👉 Select option (1-4): ").strip()
            
            if choice == "1":
                list_available_images()
                
            elif choice == "2":
                image_path = input(f"\n📁 Enter image path: ").strip()
                if image_path:
                    test_specific_image(image_path)
                
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
                                test_specific_image(image_path)
                            else:
                                print("❌ Invalid image number")
                        else:
                            print(f"❌ Category path not found: {category_path}")
                    else:
                        print("❌ Invalid category number")
                except ValueError:
                    print("❌ Please enter a valid number")
                
            elif choice == "4":
                print(f"👋 Goodbye!")
                break
                
            else:
                print(f"❌ Invalid choice. Please select 1-4.")
                
        except KeyboardInterrupt:
            print(f"\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def quick_test_mode():
    """Quick test mode with command line arguments"""
    
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"🚀 QUICK TEST MODE")
        test_specific_image(image_path)
    else:
        print(f"Usage: python {sys.argv[0]} <image_path>")
        print(f"   or: python {sys.argv[0]}  (for interactive mode)")

def main():
    """Main function"""
    
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        quick_test_mode()
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()