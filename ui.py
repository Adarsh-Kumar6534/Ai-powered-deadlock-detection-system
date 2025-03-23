from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
    QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QTimer
from deadlock_detection.detection import DeadlockDetector
from deadlock_detection.styles import button_style
import networkx as nx


class DeadlockDetectionUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Powered Deadlock Detector")
        self.setGeometry(100, 100, 1000, 650)
        self.setStyleSheet("background-color: #1E1E2E; color: white;")

        self.detector = DeadlockDetector()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("AI Deadlock Detection Tool", self)
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #FFD700;")
        layout.addWidget(self.label)

        self.detect_button = QPushButton("Detect Deadlock", self)
        self.detect_button.setStyleSheet(button_style("#4CAF50"))
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
        self.fix_button.setStyleSheet(button_style("#FF5722"))
        self.fix_button.clicked.connect(self.fix_deadlock)
        layout.addWidget(self.fix_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
        self.detector.deadlock_graph = self.get_table_data()
        result, cycle = self.detector.detect_deadlock()

        self.result_area.setText(result)

        if cycle:
            self.highlight_deadlock([p[0] for p in cycle])

    def fix_deadlock(self):
        fixed_message = self.detector.fix_deadlock()
        self.result_area.append(fixed_message)
        self.update_table()
        self.highlight_fix()

    def update_table(self):
        processes = ["P1", "P2", "P3", "P4", "P5"]

        for i in range(5):
            for j in range(5):
                item = self.table.item(i, j)
                if item:
                    item.setText("1" if (processes[i], processes[j]) in self.detector.deadlock_graph.edges else "0")

    def highlight_deadlock(self, deadlocked_processes):
        for process in deadlocked_processes:
            idx = int(process[1:]) - 1
            for col in range(self.table.columnCount()):
                item = self.table.item(idx, col) or QTableWidgetItem("")
                item.setBackground(QColor("#FF4500"))
                self.table.setItem(idx, col, item)

    def highlight_fix(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor("#4CAF50"))
        QTimer.singleShot(15000, self.reset_table)

    def reset_table(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor("#2E2E3E"))
