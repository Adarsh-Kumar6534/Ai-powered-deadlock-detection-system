import sys
import networkx as nx
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
    QWidget, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QTimer

class DeadlockDetectionAI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Powered Deadlock Detector")
        self.setGeometry(100, 100, 1000, 650)
        self.setStyleSheet("background-color: #1E1E2E; color: white;")
        
        self.initUI()
        self.deadlock_graph = nx.DiGraph()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("AI Deadlock Detection Tool", self)
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #FFD700;")
        layout.addWidget(self.label)
        
        self.detect_button = QPushButton("Detect Deadlock", self)
        self.detect_button.setStyleSheet(self.button_style("#4CAF50"))
        self.detect_button.clicked.connect(self.detect_deadlock)
        layout.addWidget(self.detect_button)

        self.table = QTableWidget(5, 5)
        self.table.setHorizontalHeaderLabels(["P1", "P2", "P3", "P4", "P5"])
        self.table.setVerticalHeaderLabels(["P1", "P2", "P3", "P4", "P5"])
        self.table.setStyleSheet("background-color: #2E2E3E; color: white; font-size: 14px;")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("background-color: #333B44; color: white; font-size: 14px;")
        layout.addWidget(self.result_area)

        self.fix_button = QPushButton("Fix Deadlock", self)
        self.fix_button.setStyleSheet(self.button_style("#FF5722"))
        self.fix_button.clicked.connect(self.fix_deadlock)
        layout.addWidget(self.fix_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def button_style(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 8px;
        }}
        QPushButton:hover {{
            background-color: {self.darken_color(color)};
        }}
        """
    def darken_color(self, color):
        return f"{color[:-2]}AA"

    def get_table_data(self):
        graph = nx.DiGraph()
        processes = ["P1", "P2", "P3", "P4", "P5"]
        
        for i in range(5):
            for j in range(5):
                item = self.table.item(i, j)
                if item and item.text() == "1":
                    graph.add_edge(processes[i], processes[j])
        
        return graph
    
    def detect_deadlock(self):
        self.deadlock_graph = self.get_table_data()
        
        if len(self.deadlock_graph.nodes) == 0:
            self.result_area.setText("No valid process dependencies found.")
            return
        
        deadlock_type = self.identify_deadlock_type()
        
        if "No Deadlock" in deadlock_type:
            self.result_area.setText("✅ No Deadlock Detected.")
        else:
            cycle = list(nx.find_cycle(self.deadlock_graph, orientation='original')) if "Circular Wait" in deadlock_type else []
            self.result_area.setText(f"⚠️ **Deadlock Detected!** {deadlock_type}\nCycle: {cycle}")
            self.highlight_deadlock([p[0] for p in cycle])

    def identify_deadlock_type(self):
        if not self.deadlock_graph:
            return "No Deadlock"

        edges = list(self.deadlock_graph.edges)
        if not edges:
            return "No Deadlock"

        processes = list(self.deadlock_graph.nodes)
        edges_set = set(edges)

        if any(u == v for u, v in edges):
            return "🔴 Mutual Exclusion Deadlock (Self-loop detected)."
        
        if any((v, u) in edges_set for u, v in edges):
            return "🟡 No Preemption Deadlock (Irreversible resource holding)."

        hold_wait_detected = any(any((u, v) in edges_set for v in processes) for u in processes)

        try:
            nx.find_cycle(self.deadlock_graph, orientation="original")
            return "🟠 Circular Wait Deadlock (Processes waiting in a cycle)."
        except nx.NetworkXNoCycle:
            pass

        if hold_wait_detected:
            return "🔵 Hold and Wait Deadlock (Processes holding resources and waiting)."

        return "No Deadlock"

    def highlight_deadlock(self, deadlocked_processes):
        for process in deadlocked_processes:
            idx = int(process[1:]) - 1  
            for col in range(self.table.columnCount()):
                item = self.table.item(idx, col) or QTableWidgetItem("")
                item.setBackground(QColor("#FF4500"))
                self.table.setItem(idx, col, item)
    
    def fix_deadlock(self):
        if not self.deadlock_graph:
            self.result_area.append("No deadlock detected to fix.")
            return
        
        try:
            cycle = nx.find_cycle(self.deadlock_graph, orientation='original')
            process_to_remove = cycle[0][0]
            self.deadlock_graph.remove_node(process_to_remove)
            self.update_table()
            self.result_area.append(f"✅ Deadlock Resolved! Process {process_to_remove} preempted.")
            self.highlight_fix()
        except nx.NetworkXNoCycle:
            self.result_area.append("No deadlock to fix.")
    
    def update_table(self):
        processes = ["P1", "P2", "P3", "P4", "P5"]
        
        for i in range(5):
            for j in range(5):
                item = self.table.item(i, j)
                if item:
                    item.setText("1" if (processes[i], processes[j]) in self.deadlock_graph.edges else "0")
    
    def highlight_fix(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor("#4CAF50"))  
        QTimer.singleShot(15000, self.reset_table)  

    def reset_table(self):
        """ Resets the table background color back to original after 15 seconds, keeping data intact. """
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor("#2E2E3E"))  # Reset color to match table's original background

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeadlockDetectionAI()
    window.show()
    sys.exit(app.exec())



