# 🛠 AI-Powered Deadlock Detection & Resolution Tool

## 🔍 Overview
The **AI-Powered Deadlock Detection & Resolution Tool** is a smart system designed to detect, analyze, and resolve deadlocks in process scheduling.
It leverages **graph theory, AI-based algorithms, and resource allocation strategies** to prevent deadlocks and optimize system performance.

With an intuitive **Graphical User Interface (GUI)** powered by **PyQt6**, the tool provides a **visual representation** of processes, resources, and dependencies, making it easier to analyze and resolve conflicts efficiently.

---

## 🎯 Key Features
✅ **Graph-Based Deadlock Detection** – Uses **NetworkX** to build a **Resource Allocation Graph (RAG)** and detect cyclic dependencies.  
✅ **Automated Resolution Mechanism** – AI-driven algorithms suggest **process preemption** and **resource reallocation**.  
✅ **Real-Time Visualization** – Interactive GUI displays **process dependencies** and **deadlock resolution** in real-time.  
✅ **Efficient Computation** – Utilizes **NumPy** for fast **matrix operations**.  
✅ **User-Friendly Interface** – Simple **drag-and-drop interaction** for process-resource mapping.  
✅ **Log Generation & Reports** – Keeps track of **detected deadlocks, resolved cases, and system performance**.  

---

## 🛠 Technologies Used

| **Technology** | **Purpose** |  
|-----------------|-------------|  
| **Python**       | Core language for algorithms |  
| **PyQt6**        | GUI framework for visualization |  
| **NetworkX**     | Graph-based detection using cycle detection algorithms |  
| **NumPy**        | Efficient matrix computations |  
| **Matplotlib**   | Visualization of deadlock scenarios |  

---

## 🚀 Installation
Follow these steps to install dependencies and run the tool:

```bash
# Clone the repository
git clone https://github.com/Adarsh-Kumar6534/deadlock-detection-ai.git
cd deadlock-detection-ai

# Install required dependencies
pip install PyQt6 networkx numpy matplotlib

# Run the application
python src/main.py
```

---

## 🎯 How It Works
1. **Define Process-Resource Dependencies**: Input processes and resources using the interactive GUI.
2. **Graph Construction**: The system creates a Resource Allocation Graph (RAG).
3. **Deadlock Detection**: It checks for cycles using Depth-First Search (DFS) or other algorithms.
4. **Automated Resolution**: AI suggests and executes preemptive actions to resolve the deadlock.
5. **Visualization & Logging**: Updates the UI in real-time and generates log reports.

---

## 📊 Performance Metrics
- Track **deadlock frequency** and **resolution time**.
- Visualize system performance with **interactive graphs**.
- Generate reports for further analysis.

---

## 🤝 Contribution Guidelines
Contributions are welcome! Here's how you can contribute:

1. **Fork** the repository.
2. **Create a new branch** (`feature-new-improvement`).
3. **Commit your changes**.
4. **Push to your fork**.
5. **Create a Pull Request**.

---

## 📜 License
This project is licensed under the **MIT License**. Feel free to contribute and improve! 🚀

---

## 📂 Project Structure

AI-Deadlock-Detection/
├── 📁 src/                     # Source Code - Core Logic & GUI
│   ├── 🧑‍💻 main.py              # Main application to run the tool
│   ├── 🖼 gui.py                # Graphical User Interface using PyQt6
│   ├── 🧠 deadlock_detection.py # Deadlock Detection Algorithms
│   ├── 🛠 resolution.py         # Deadlock Resolution Algorithms
│
├── 📁 docs/                    # Documentation
│   ├── 📖 user_guide.md         # Step-by-Step User Guide
│   ├── 📝 architecture.md       # Project Architecture Overview
│   └── 📊 report.pdf            # Project Report
│
├── 📄 README.md                 # Project Overview & Instructions
├── 📄 requirements.txt          # Dependencies for Installation
├── 📄 LICENSE                   # License Information

---

## 🚀 Developed By
🎓 **Adarsh Kumar**  
🎓 **Anurag Anand Jha**  
🎓 **Sukhpreet Kaur**  

We aim to enhance system performance by eliminating deadlocks efficiently!

