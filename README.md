🛠 AI-Powered Deadlock Detection & Resolution Tool
🔍 Overview
The AI-Powered Deadlock Detection & Resolution Tool is a smart system designed to detect and resolve deadlocks in process scheduling. By leveraging graph theory and AI-based algorithms, it analyzes dependencies, identifies potential deadlocks, and provides an automated resolution mechanism. The tool is built with PyQt6, NetworkX, and NumPy, featuring an intuitive Graphical User Interface (GUI) to visualize and resolve deadlocks efficiently.

👥 Team Members
This project is developed by:

Adarsh Kumar

Anurag Anand Jha

Sukhpreet Kaur

📌 Key Features
✅ Graph-Based Deadlock Detection – Uses NetworkX to represent process-resource dependencies as a Resource Allocation Graph (RAG).
✅ Detection of Multiple Deadlock Types – Identifies deadlocks based on the Four Coffman Conditions:

Mutual Exclusion

Hold and Wait

No Preemption

Circular Wait
✅ Automated Deadlock Resolution – Preempts a process or modifies dependencies to break the deadlock cycle.
✅ Interactive GUI – Built using PyQt6, providing an intuitive interface for entering dependencies, detecting, and resolving deadlocks.
✅ Real-Time Graph Visualization – Highlights deadlocked processes in red and resolved processes in green.
✅ Matrix-Based Input System – Allows users to enter process-resource allocations in a structured format.


⚙️ Installation
Follow these steps to install dependencies and run the tool:

bash
Copy
Edit
# Clone the repository
git clone https://github.com/your-username/deadlock-detection-ai.git
cd deadlock-detection-ai

# Install required dependencies
pip install PyQt6 networkx numpy

# Run the application
python main.py
🎯 How It Works
Define Process-Resource Dependencies

Users input a matrix defining which processes hold or request resources.

Graph-Based Deadlock Detection

The system constructs a Resource Allocation Graph (RAG) and checks for cycles.

Deadlock Identification

If a cycle exists, the system identifies the deadlocked processes.

Automated Deadlock Resolution

The AI suggests and executes preemptive actions to resolve the deadlock.

Visualization & Updates

The UI updates with real-time feedback, showing the changes made to resolve deadlocks.

🏗️ Future Enhancements
🔹 Support for Dynamic Resource Allocation – Extend the system to handle dynamic process creation and resource requests.
🔹 Machine Learning Integration – Use AI models to predict and prevent deadlocks.
🔹 Simulation Mode – Allow users to run step-by-step deadlock simulation for learning purposes.
🔹 Priority-Based Resource Allocation – Implement priority handling to resolve deadlocks based on process importance.

🤝 Contribution Guidelines
Contributions are welcome! If you'd like to improve the project, follow these steps:

Fork the repository.

Create a feature branch (feature-new-improvement).

Commit your changes.

Push to your fork and create a Pull Request.

📜 License
This project is licensed under the MIT License.
