import sys
import networkx as nx
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor, QBrush, QLinearGradient
from PyQt6.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DeadlockDetectionAI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Deadlock Detection System")
        self.setGeometry(100, 100, 1000, 650)
        # Background gradient: Light Sky Blue (#B3E5FC) to Sky Blue (#4FC3F7)
        self.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B3E5FC, stop:1 #4FC3F7);
        """)
       
        self.deadlock_graph = nx.DiGraph()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Title
        self.label = QLabel("AI Deadlock Detection System")
        self.label.setFont(QFont("Helvetica", 24, QFont.Weight.Bold))  # Fallback to Helvetica
        self.label.setStyleSheet("""
            color: #000000;  /* Black */
            background: transparent;
            padding: 5px;
            border: 2px solid #000000;
            border-radius: 5px;
        """)
        # Add a shadow effect for 3D look
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.label.setGraphicsEffect(shadow)
        self.label.setFixedHeight(50)  # Ensure the title stays at the top
        main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Two-part layout (left and right halves)
        two_part_layout = QHBoxLayout()

        # Left Half: Table and Buttons
        left_layout = QVBoxLayout()
        self.table = QTableWidget(5, 5)
        self.table.setHorizontalHeaderLabels(["P1", "P2", "P3", "P4", "P5"])
        self.table.setVerticalHeaderLabels(["P1", "P2", "P3", "P4", "P5"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                color: black;
                font-size: 14px;
                border: 1px solid black;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #26A69A, stop:1 #FF6F61);
                color: white;
                font-weight: bold;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        left_layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        self.detect_button = QPushButton("Detect Deadlock")
        self.detect_button.setStyleSheet(self.button_style("#26A69A"))  # Teal
        self.detect_button.clicked.connect(self.detect_deadlock)
        # Add 3D shadow effect
        detect_shadow = QGraphicsDropShadowEffect()
        detect_shadow.setBlurRadius(15)
        detect_shadow.setXOffset(5)
        detect_shadow.setYOffset(5)
        detect_shadow.setColor(QColor(0, 0, 0, 100))
        self.detect_button.setGraphicsEffect(detect_shadow)
        button_layout.addWidget(self.detect_button)

        self.fix_button = QPushButton("Fix Deadlock")
        self.fix_button.setStyleSheet(self.button_style("#FF6F61"))  # Coral Pink
        self.fix_button.clicked.connect(self.fix_deadlock)
        # Add 3D shadow effect
        fix_shadow = QGraphicsDropShadowEffect()
        fix_shadow.setBlurRadius(15)
        fix_shadow.setXOffset(5)
        fix_shadow.setYOffset(5)
        fix_shadow.setColor(QColor(0, 0, 0, 100))
        self.fix_button.setGraphicsEffect(fix_shadow)
        button_layout.addWidget(self.fix_button)

        left_layout.addLayout(button_layout)
        two_part_layout.addLayout(left_layout, stretch=1)  # Left half takes 50% of the space

        # Right Half: Bar Chart and Message Log (split vertically)
        right_layout = QVBoxLayout()

        # Bar Chart (Top)
        self.figure = Figure(figsize=(4, 3))
        # Make the figure background transparent
        self.figure.patch.set_alpha(0)
        self.canvas = FigureCanvas(self.figure)
        # Apply gradient background to the canvas
        self.canvas.setStyleSheet("""
            border: 1px solid #000000;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B3E5FC, stop:1 #4FC3F7);
        """)
        # Connect click event for bar interaction
        self.canvas.mpl_connect('button_press_event', self.on_bar_click)
        right_layout.addWidget(self.canvas, stretch=1)
        self.update_chart()

        # Message Log (Bottom)
        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)
        self.message_log.setStyleSheet("""
            QTextEdit {
                background-color: #F5E6E8;
                color: black;
                font-size: 16px;
                border: none;
            }
        """)
        # Add a shadow effect for neon look
        message_shadow = QGraphicsDropShadowEffect()
        message_shadow.setBlurRadius(15)
        message_shadow.setXOffset(0)
        message_shadow.setYOffset(0)
        message_shadow.setColor(QColor(255, 255, 255, 200))  # White glow for neon effect
        self.message_log.setGraphicsEffect(message_shadow)
        self.add_message("System initialized...")
        right_layout.addWidget(self.message_log, stretch=1)

        two_part_layout.addLayout(right_layout, stretch=1)  # Right half takes 50% of the space

        main_layout.addLayout(two_part_layout)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def button_style(self, color):
        # Create a gradient for the button to enhance the 3D effect
        return f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {color}, stop:1 {self.darken_color(color)});
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 8px;
            border: 2px solid {self.darken_color(color)};
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {self.lighten_color(color)}, stop:1 {color});
        }}
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {self.darken_color(color)}, stop:1 {color});
        }}
        """

    
