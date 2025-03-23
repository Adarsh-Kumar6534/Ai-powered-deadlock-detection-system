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


