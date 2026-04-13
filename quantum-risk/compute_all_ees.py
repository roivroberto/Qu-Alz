#!/usr/bin/env python3
"""
Compute Quantum Entanglement Entropy Score (EES) for all MRI images in the dataset
and generate a comprehensive CSV file with results.
"""

import os
import csv
import time
from pathlib import Path
import numpy as np
from quantum_ees import QuantumEES, MRIEmbeddingExtractor, QISKIT_AVAILABLE
import warnings
warnings.filterwarnings('ignore')

def find_all_images(base_path="data"):
    """Find all image files in the dataset structure"""
    image_files = []
    base_path = Path(base_path)
    
    # Define the expected structure
    splits = ["train", "test"]
    categories = ["No Impairment", "Mild Impairment", "Moderate Impairment", "Very Mild Impairment"]
    
    for split in splits:
        for category in categories:
            category_path = base_path / split / category
            if category_path.exists():
                # Find all jpg files in this directory
                for img_file in category_path.glob("*.jpg"):
                    image_files.append({
                        'filepath': str(img_file),
                        'filename': img_file.name,
                        'split': split,
                        'category': category,
                        'relative_path': str(img_file.relative_to(base_path))
                    })
    
    return image_files

def compute_ees_for_dataset(output_csv="ees_results.csv"):
    """Compute EES for all images and save to CSV"""
    
    print("🧠 Quantum Entanglement Entropy Score (EES) - Dataset Analysis")
    print("=" * 65)
    
    # Check if Qiskit is available
    if not QISKIT_AVAILABLE:
        print("❌ Qiskit not available. Install with: pip install qiskit qiskit-aer")
        return
    
    # Initialize components
    print("🔧 Initializing quantum EES system...")
    quantum_ees = QuantumEES(n_qubits=10, reps=2)
    extractor = MRIEmbeddingExtractor()
    
    # Find all images
    print("📁 Scanning for images...")
    image_files = find_all_images()
    print(f"   Found {len(image_files)} images to process")
    
    if len(image_files) == 0:
        print("❌ No images found in data directory!")
        return
    
    # Process images and collect results
    results = []
    failed_count = 0
    
    print("\n🚀 Computing EES scores...")
    start_time = time.time()
    
    for i, img_info in enumerate(image_files):
        try:
            # Extract features from MRI image
            features = extractor.extract_features(img_info['filepath'])
            
            # Compute EES
            ees_score, computation_info = quantum_ees.compute_ees(features)
            
            # Store result
            result = {
                'filename': img_info['filename'],
                'filepath': img_info['filepath'],
                'relative_path': img_info['relative_path'],
                'split': img_info['split'],
                'category': img_info['category'],
                'ees_score': round(ees_score, 6),
                'computation_time_ms': round(computation_info['computation_time_ms'], 2),
                'n_qubits': computation_info['n_qubits'],
                'circuit_depth': computation_info['circuit_depth'],
                'status': 'success'
            }
            results.append(result)
            
            # Progress update
            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                avg_time = elapsed / (i + 1)
                remaining = (len(image_files) - i - 1) * avg_time
                print(f"   Progress: {i+1}/{len(image_files)} ({(i+1)/len(image_files)*100:.1f}%) "
                      f"- ETA: {remaining/60:.1f} min")
            
        except Exception as e:
            failed_count += 1
            print(f"   ⚠️  Failed to process {img_info['filename']}: {str(e)[:50]}...")
            
            # Store failed result
            result = {
                'filename': img_info['filename'],
                'filepath': img_info['filepath'],
                'relative_path': img_info['relative_path'],
                'split': img_info['split'],
                'category': img_info['category'],
                'ees_score': None,
                'computation_time_ms': None,
                'n_qubits': None,
                'circuit_depth': None,
                'status': f'failed: {str(e)[:30]}...'
            }
            results.append(result)
    
    # Calculate summary statistics
    successful_results = [r for r in results if r['status'] == 'success']
    if successful_results:
        ees_scores = [r['ees_score'] for r in successful_results]
        avg_ees = np.mean(ees_scores)
        std_ees = np.std(ees_scores)
        min_ees = np.min(ees_scores)
        max_ees = np.max(ees_scores)
        
        avg_time = np.mean([r['computation_time_ms'] for r in successful_results])
    else:
        avg_ees = std_ees = min_ees = max_ees = avg_time = 0
    
    # Write results to CSV
    print(f"\n💾 Writing results to {output_csv}...")
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'filepath', 'relative_path', 'split', 'category', 
                     'ees_score', 'computation_time_ms', 'n_qubits', 'circuit_depth', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    # Print summary
    total_time = time.time() - start_time
    print(f"\n📊 Analysis Complete!")
    print(f"   Total images processed: {len(image_files)}")
    print(f"   Successful: {len(successful_results)}")
    print(f"   Failed: {failed_count}")
    print(f"   Total time: {total_time/60:.1f} minutes")
    
    if successful_results:
        print(f"\n📈 EES Score Statistics:")
        print(f"   Average EES: {avg_ees:.4f} ± {std_ees:.4f} bits")
        print(f"   Range: {min_ees:.4f} to {max_ees:.4f} bits")
        print(f"   Avg computation: {avg_time:.1f} ms per image")
        
        # Category breakdown
        print(f"\n📂 By Category:")
        for category in ["No Impairment", "Mild Impairment", "Moderate Impairment", "Very Mild Impairment"]:
            cat_results = [r for r in successful_results if r['category'] == category]
            if cat_results:
                cat_scores = [r['ees_score'] for r in cat_results]
                cat_avg = np.mean(cat_scores)
                print(f"   {category}: {len(cat_results)} images, avg EES = {cat_avg:.4f} bits")
    
    print(f"\n✅ Results saved to: {output_csv}")
    return output_csv

if __name__ == "__main__":
    csv_file = compute_ees_for_dataset()
    print(f"\n🎉 EES analysis complete! Check {csv_file} for full results.")