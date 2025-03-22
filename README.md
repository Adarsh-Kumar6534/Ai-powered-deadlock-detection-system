# AI-Based Deadlock Detection and Resolution

## Overview
This project implements an AI-driven system to **detect and resolve deadlocks** using **Machine Learning (ML), Reinforcement Learning (RL), and Graph Theory**. It simulates deadlock conditions, trains a neural network to detect deadlocks, and applies deadlock resolution strategies to mitigate issues dynamically.

## Features
- **Deadlock Detection** using a **Resource Allocation Graph (RAG)**.
- **Machine Learning Model** trained on synthetic deadlock scenarios.
- **Reinforcement Learning-based Deadlock Resolution**.
- **Graph Visualization** of the process-resource allocation.
- **Deadlock Breaking Mechanism** to automatically resolve detected deadlocks.

## Technologies Used
- **Python** (Primary Language)
- **PyTorch** (Neural Network for Deadlock Detection)
- **NetworkX** (Graph-based Deadlock Detection)
- **Matplotlib** (Graph Visualization)
- **Scikit-Learn** (Dataset Splitting & Processing)
- **Numpy** (Numerical Operations)

## Installation
Ensure you have **Python 3.8+** installed. Install dependencies using:
```bash
pip install torch networkx numpy matplotlib scikit-learn
```

For Jupyter Notebook users:
```python
!pip install torch networkx numpy matplotlib scikit-learn
```

## Usage
### 1. Run the AI Model Training
```python
from deadlock_ai import train_deadlock_nn
model = train_deadlock_nn()
```

### 2. Detect & Resolve Deadlocks
```python
from deadlock_ai import DeadlockDetector, resolve_deadlock

detector = DeadlockDetector()
detector.add_process_resource("P1", "R1", holds=True)
detector.add_process_resource("P2", "R2", holds=True)
detector.add_process_resource("P1", "R2")
detector.add_process_resource("P2", "R1")  # Creates a circular wait (Deadlock)

detector.visualize_graph()
print("Deadlock Detected:", detector.detect_deadlock())
resolve_deadlock(detector)
```

## Deadlock Resolution Strategy
The AI system resolves deadlocks using:
1. **Process Termination:** Kills the least disruptive process.
2. **Graph Update:** Removes terminated process from RAG.
3. **Graph Re-evaluation:** Re-checks if deadlock persists.

## Future Improvements
- **Enhance RL Agent** for smarter deadlock prevention.
- **Improve Training Data** using real-world deadlock scenarios.
- **Deploy as a Web Service** for integration in production systems.

## License
This project is **open-source** under the **MIT License**. Feel free to use, modify, and contribute!

---

### Contributors
adarsh
anuraj
sukhpreet
*Project Lead & Developer*

