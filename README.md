# NeuroQLeap 🧠💻

**Quantum-Enhanced Alzheimer's Prediction & Early Risk Assessment**

[![Language](https://img.shields.io/github/languages/top/roivroberto/NeuroQLeap)](https://github.com/roivroberto/NeuroQLeap)
[![Repo size](https://img.shields.io/github/repo-size/roivroberto/NeuroQLeap)](https://github.com/roivroberto/NeuroQLeap)
[![Last commit](https://img.shields.io/github/last-commit/roivroberto/NeuroQLeap)](https://github.com/roivroberto/NeuroQLeap)
[![Stars](https://img.shields.io/github/stars/roivroberto/NeuroQLeap?style=social)](https://github.com/roivroberto/NeuroQLeap)
[![Forks](https://img.shields.io/github/forks/roivroberto/NeuroQLeap?style=social)](https://github.com/roivroberto/NeuroQLeap)
[![License](https://img.shields.io/github/license/roivroberto/NeuroQLeap)](https://github.com/roivroberto/NeuroQLeap)

---

## 🚀 Demo
![Demo](assets/demo.png)
*Replace with a real screenshot or GIF of the project in action.*

---

## 📖 About
**NeuroQLeap** is a cutting-edge healthcare solution developed for the **SEA Quantathon 2025** by team **The Qure**. It leverages **Quantum Machine Learning (QML)** and deep learning to provide early detection and risk assessment for Alzheimer's disease.

By introducing the **Quantum Entanglement Entropy Score (EES)**—a fundamentally quantum-only biomarker—this project identifies subtle patterns in MRI data that classical machine learning kernels cannot compute. This innovation aims to push the boundaries of early neurodegenerative disease diagnosis using the power of quantum information theory.

---

## 🛠️ Tech Stack
### **Frontend (Interface)**
- **Framework:** Next.js 15, React 19, TypeScript
- **Styling:** Tailwind CSS, Radix UI (shadcn/ui), Lucide Icons
- **Visualizations:** Recharts (Interactive heatmap & entanglement meters)

### **AI & Quantum (Backend/Models)**
- **Deep Learning:** PyTorch (CNN for classification, U-Net for MRI segmentation)
- **Quantum Computing:** Qiskit (Quantum circuits, ZZFeatureMap, density matrices)
- **Scientific Computing:** NumPy, SciPy, Scikit-Learn
- **Visualization:** Matplotlib, Seaborn

---

## ✨ Features
- 🧬 **Quantum-Only Biomarker**: Computes Entanglement Entropy Score (EES) using quantum superposition and density matrices.
- 🖼️ **MRI Segmentation**: Automated U-Net based segmentation of brain regions from MRI scans.
- 📊 **Disease Classification**: Multi-stage Alzheimer's classification (No Impairment, Very Mild, Mild, Moderate).
- 📈 **Risk Pipeline**: Comprehensive pipeline integrating classical features with quantum biomarkers for risk assessment.
- 🖥️ **Interactive Dashboard**: A professional clinical interface for uploading MRIs and visualizing diagnostic results.

---

## 📂 Project Structure
- `alzheimers-prediction-interface/`: Next.js web application for clinicians.
- `Classifier/`: CNN and QCNN (Quantum CNN) models for disease stage prediction.
- `Segmentation/`: U-Net models and scripts for MRI image segmentation.
- `Risk/`: Quantum EES pipeline and risk assessment models.
- `docs/`: Project documentation and presentation materials.

---

## 🚦 Getting Started

### **1. Frontend Interface**
```bash
cd alzheimers-prediction-interface
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to see the dashboard.

### **2. Quantum & AI Models**
Ensure you have Python 3.10+ installed.
```bash
cd Risk
pip install -r requirements.txt
python test_quantum_ees.py
```

---

## 📜 License
This project is licensed under the MIT License.

---

## 🏆 Hackathon Details
- **Event:** SEA Quantathon 2025 (Healthcare & Medicine Track)
- **Location:** Bangkok, Thailand
- **Team:** The Qure
- **Theme:** Prototyping quantum solutions for social good in Southeast Asia.
