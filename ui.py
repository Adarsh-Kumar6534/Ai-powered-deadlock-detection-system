from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class DependencyChart(FigureCanvas):
    def __init__(self):
        self.figure = Figure(figsize=(4, 3))
        super().__init__(self.figure)
        self.setup_chart()

    def setup_chart(self):
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#F5F5F5')
        self.figure.patch.set_alpha(0)

    def update_chart(self, graph_data: dict):
        self.ax.clear()
        
        # Chart drawing logic here
        self.draw()


from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from ui.table import ProcessTable
from ui.chart import DependencyChart
from ui.message_log import MessageLog
from core.graph_manager import GraphManager
from core.detector import DeadlockDetector

class DeadlockDetectionAI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph_manager = GraphManager()
        self.detector = DeadlockDetector()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AI Deadlock Detection System")
        self.setGeometry(100, 100, 1000, 650)
        
        # Create UI components
        self.table = ProcessTable()
        self.chart = DependencyChart()
        self.message_log = MessageLog()
        
        # Layout setup
        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.table)
        left_layout.addWidget(self.create_buttons())
        
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.chart)
        right_layout.addWidget(self.message_log)
        
        content_layout.addLayout(left_layout, stretch=1)
        content_layout.addLayout(right_layout, stretch=1)
        main_layout.addLayout(content_layout)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_buttons(self):
        # Button creation and connections
        pass

    # Other main window methods...

from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QColor

class MessageLog(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_log()

    def setup_log(self):
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #F5E6E8;
                color: black;
                font-size: 16px;
                border: none;
            }
        """)

    def add_message(self, message: str, message_type: str = "info"):
        colors = {
            "info": "black",
            "warning": "orange",
            "error": "red",
            "success": "green"
        }
        self.append(f'<p style="color:{colors[message_type]}">{message}</p>')

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QBrush, QColor, QLinearGradient

class ProcessTable(QTableWidget):
    def __init__(self):
        super().__init__(5, 5)
        self.setup_table()

    def setup_table(self):
        self.setHorizontalHeaderLabels(["P1", "P2", "P3", "P4", "P5"])
        self.setVerticalHeaderLabels(["P1", "P2", "P3", "P4", "P5"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        for i in range(5):
            for j in range(5):
                self.setItem(i, j, QTableWidgetItem("0"))

    def get_table_data(self) -> list[list[str]]:
        data = []
        for i in range(5):
            row = []
            for j in range(5):
                item = self.item(i, j)
                row.append(item.text() if item else "0")
            data.append(row)
        return data

    def highlight_processes(self, processes: list[str], color_gradient: tuple[str, str]):
        pass
