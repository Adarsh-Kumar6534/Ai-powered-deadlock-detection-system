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


    def darken_color(self, color):
        # Darken the color by reducing its brightness
        return f"{color[:-2]}80"

    def lighten_color(self, color):
        # Lighten the color by increasing its brightness
        return f"{color[:-2]}FF"

    def update_chart(self):
        # Include all 5 processes (P1 to P5)
        self.processes = ["P1", "P2", "P3", "P4", "P5"]
        # Series 1: Outgoing dependencies (how many processes Pi depends on)
        self.series1 = [sum(1 for u, v in self.deadlock_graph.edges if u == p) for p in self.processes]
        # Series 2: Incoming dependencies (how many processes depend on Pi)
        self.series2 = [sum(1 for u, v in self.deadlock_graph.edges if v == p) for p in self.processes]
        # Series 3: Placeholder (e.g., resource requests; set to 1 for now)
        self.series3 = [1] * 5

        # Store the processes each process is waiting on or waited by
        self.waiting_on_details = {p: [] for p in self.processes}
        self.waited_by_details = {p: [] for p in self.processes}
        for u, v in self.deadlock_graph.edges:
            if u in self.processes:
                self.waiting_on_details[u].append(v)
            if v in self.processes:
                self.waited_by_details[v].append(u)

        self.figure.clear()
        # Use 2D axes for a simpler, straight bar chart
        ax = self.figure.add_subplot(111)
        # Set a light background color for the plot area
        ax.set_facecolor('#F5F5F5')  # Light gray background
        self.figure.patch.set_alpha(0)

        x = np.arange(len(self.processes))
        width = 0.2  # Reduced width to accommodate 5 processes

        # Define colors with a slight gradient effect for a 3D-like appearance
        waiting_on_color = '#4682B4'  # Steel Blue
        waited_by_color = '#FF6347'   # Tomato
        resources_held_color = '#3CB371'  # Medium Sea Green

        # Plot 2D bars with enhanced shadows for a 3D-like effect
        # Waiting On
        bars1 = ax.bar(x - width, self.series1, width, label="Waiting On", color=waiting_on_color, edgecolor="black", zorder=2)
        for bar in bars1:
            bar.set_hatch('/')
            # Add a shadow effect by plotting a slightly offset bar
            ax.bar(bar.get_x() + 0.02, bar.get_height(), width, bottom=0, color="black", alpha=0.1, zorder=1)

        # Waited By
        bars2 = ax.bar(x, self.series2, width, label="Waited By", color=waited_by_color, edgecolor="black", zorder=2)
        for bar in bars2:
            bar.set_hatch('/')
            ax.bar(bar.get_x() + 0.02, bar.get_height(), width, bottom=0, color="black", alpha=0.1, zorder=1)

        # Resources Held
        bars3 = ax.bar(x + width, self.series3, width, label="Resources Held", color=resources_held_color, edgecolor="black", zorder=2)
        for bar in bars3:
            bar.set_hatch('/')
            ax.bar(bar.get_x() + 0.02, bar.get_height(), width, bottom=0, color="black", alpha=0.1, zorder=1)

        # Set labels and styling
        ax.set_xticks(x)
        ax.set_xticklabels(self.processes, fontname="Arial", fontsize=12, color="black")
        ax.set_ylabel("Number of Dependencies", fontname="Arial", fontsize=12, color="black")
        ax.set_title("Process Dependency Analysis", fontname="Arial", fontsize=14, pad=15, color="black")
        ax.legend(prop={'family': 'Arial', 'size': 10}, facecolor='white', framealpha=0.8, loc='upper right')

        # Set limits with extra padding
        ax.set_xlim(-0.5, len(self.processes) - 0.5)
        max_height = max(max(self.series1, default=0), max(self.series2, default=0), max(self.series3, default=0)) + 1
        ax.set_ylim(0, max_height)

        # Add a light grid for better readability
        ax.yaxis.grid(True, linestyle='--', alpha=0.7, color='gray')
        ax.set_axisbelow(True)  # Ensure grid lines are behind the bars

        # Ensure text and spines are visible against the gradient
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        for spine in ax.spines.values():
            spine.set_color('black')
            spine.set_linewidth(0.5)

        # Store bar positions for click detection
        self.bars = [
            (x - width, self.series1, "Waiting On"),
            (x, self.series2, "Waited By"),
            (x + width, self.series3, "Resources Held")
        ]
        self.canvas.draw()

    def on_bar_click(self, event):
        # Check if a bar was clicked
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if x is None or y is None:
                return

            for bar_x, heights, label in self.bars:
                for i, (bx, h) in enumerate(zip(bar_x, heights)):
                    # Check if the click is within the bar's bounds
                    if abs(x - bx) < 0.15 and y >= 0 and y <= h:
                        process = self.processes[i]
                        # Detailed message based on the bar type
                        if label == "Waiting On":
                            waiting_on = self.waiting_on_details[process]
                            message = (
                                f"📊 <b>Process {process} - Waiting On Details:</b><br>"
                                f"🔹 <b>Count:</b> {int(h)} process{'es' if h != 1 else ''}<br>"
                                f"🔹 <b>Definition:</b> This indicates the number of processes that {process} is waiting for to release resources.<br>"
                                f"🔹 <b>Processes:</b> {', '.join(waiting_on) if waiting_on else 'None'}"
                            )
                        elif label == "Waited By":
                            waited_by = self.waited_by_details[process]
                            message = (
                                f"📊 <b>Process {process} - Waited By Details:</b><br>"
                                f"🔹 <b>Count:</b> {int(h)} process{'es' if h != 1 else ''}<br>"
                                f"🔹 <b>Definition:</b> This indicates the number of processes that are waiting for {process} to release resources.<br>"
                                f"🔹 <b>Processes:</b> {', '.join(waited_by) if waited_by else 'None'}"
                            )
                        else:  # Resources Held
                            message = (
                                f"📊 <b>Process {process} - Resources Held Details:</b><br>"
                                f"🔹 <b>Count:</b> {int(h)} resource{'s' if h != 1 else ''}<br>"
                                f"🔹 <b>Definition:</b> This indicates the number of resources currently held by {process}.<br>"
                                f"🔹 <b>Note:</b> This is a placeholder metric and may be updated with actual resource data."
                            )
                        self.add_message(message)
                        return

    def add_message(self, msg):
        # Format the message with HTML to apply different styles
        if "System initialized" in msg:
            formatted_msg = f'<p style="font-family: \'Big Shoulders Display\', Arial Black; font-size: 16px; font-weight: bold; color: black;">{msg}</p>'
        elif "No Deadlock Detected" in msg:
            formatted_msg = f'<p style="font-family: \'Big Shoulders Display\', Arial Black; font-size: 16px; font-weight: bold; color: black;">✅ {msg}</p>'
        elif "Deadlock Resolved" in msg:
            formatted_msg = f'<p style="font-family: \'Big Shoulders Display\', Arial Black; font-size: 16px; font-weight: bold; color: black;">✅ {msg}</p>'
        elif "No valid process dependencies found" in msg or "No deadlock to fix" in msg:
            formatted_msg = f'<p style="font-family: \'Big Shoulders Display\', Arial Black; font-size: 16px; font-weight: bold; color: black;">{msg}</p>'
        elif "📊" in msg:  # Histogram bar click message
            # Style the histogram message with a blue title and detailed formatting
            formatted_msg = f'<p style="font-family: Arial; font-size: 14px; color: #1E90FF;">{msg}</p>'
        else:
            # Deadlock detected message with highlighted type
            lines = msg.split('\n')
            deadlock_type = lines[0].split("Type: ")[1].split("\n")[0]
            formatted_lines = [
                f'<p style="font-family: \'Big Shoulders Display\', Arial Black; font-size: 16px; font-weight: bold; color: black;">⚠️ Deadlock Detected! Type: <span style="color: #FF4500;">{deadlock_type}</span></p>',
                f'<p style="font-family: Arial; font-size: 14px; color: black;">{lines[1]}</p>',
                f'<p style="font-family: Arial; font-size: 14px; color: black;">{lines[2]}</p>',
                f'<p style="font-family: Arial; font-size: 14px; color: black;">{lines[3]}</p>',
                f'<p style="font-family: Arial; font-size: 14px; color: black;">{lines[4]}</p>'
            ]
            formatted_msg = "".join(formatted_lines)
       
        self.message_log.append(formatted_msg)
        self.message_log.ensureCursorVisible()

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
            self.add_message("No valid process dependencies found.")
            return
       
        deadlock_type = self.identify_deadlock_type()
       
        if "No Deadlock" in deadlock_type:
            self.add_message("✅ No Deadlock Detected.")
        else:
            # Check for a cycle if the deadlock type is Circular Wait
            cycle = list(nx.find_cycle(self.deadlock_graph, orientation='original')) if "Circular Wait" in deadlock_type else []
            # Each element in cycle is a tuple (u, v, direction), so we only need u and v
            cycle_str = " -> ".join([f"{u} to {v}" for u, v, _ in cycle]) if cycle else "N/A"
            processes_involved = [p[0] for p in cycle] if cycle else list(self.deadlock_graph.nodes)
           
            # Detailed explanation
            explanation = f"⚠️ Deadlock Detected! Type: {deadlock_type}\n"
            explanation += f"Processes Involved: {', '.join(processes_involved)}\n"
            explanation += f"Cycle (if applicable): {cycle_str}\n"
           
            # Add cause and prevention tips based on deadlock type
            if "Mutual Exclusion" in deadlock_type:
                explanation += "Cause: A process is waiting for itself (self-loop), violating mutual exclusion.\n"
                explanation += "Prevention: Ensure processes do not request resources they already hold.\n"
            elif "No Preemption" in deadlock_type:
                explanation += "Cause: Two processes are holding resources the other needs, with no preemption.\n"
                explanation += "Prevention: Allow resource preemption or ensure resources are released before new requests.\n"
            elif "Circular Wait" in deadlock_type:
                explanation += "Cause: Processes form a cycle, each waiting for the next to release a resource.\n"
                explanation += "Prevention: Impose a total ordering on resources and request them in order.\n"
            elif "Hold and Wait" in deadlock_type:
                explanation += "Cause: A process holding a resource is waiting for another, leading to a potential deadlock.\n"
                explanation += "Prevention: Require processes to request all resources at once or release resources before requesting new ones.\n"
           
            self.add_message(explanation)
            self.highlight_deadlock(processes_involved)
       
        # Update the chart with the new graph state
        self.update_chart()

    def identify_deadlock_type(self):
        if not self.deadlock_graph or not self.deadlock_graph.edges:
            return "No Deadlock"

        edges = list(self.deadlock_graph.edges)
        processes = list(self.deadlock_graph.nodes)
        edges_set = set(edges)

        # Check for self-loops (Mutual Exclusion Deadlock)
        has_self_loop = any(u == v for u, v in edges)
        if has_self_loop:
            return "🔴 Mutual Exclusion Deadlock (Self-loop detected)."

        # Check for bidirectional edges (No Preemption Deadlock)
        has_bidirectional = any((v, u) in edges_set for u, v in edges)
        if has_bidirectional:
            # Ensure this isn't part of a larger cycle
            try:
                nx.find_cycle(self.deadlock_graph, orientation="original")
                return "🟠 Circular Wait Deadlock (Processes waiting in a cycle)."
            except nx.NetworkXNoCycle:
                return "🟡 No Preemption Deadlock (Irreversible resource holding)."

        # Check for cycles (Circular Wait Deadlock)
        try:
            nx.find_cycle(self.deadlock_graph, orientation="original")
            return "🟠 Circular Wait Deadlock (Processes waiting in a cycle)."
        except nx.NetworkXNoCycle:
            pass

        # Check for Hold and Wait (a process holds a resource and waits for another, without a cycle)
        hold_wait_detected = False
        for u in processes:
            outgoing = set(v for _, v in self.deadlock_graph.out_edges(u))
            incoming = set(v for v, _ in self.deadlock_graph.in_edges(u))
            # A process must be holding a resource (outgoing edge) and waiting for another (incoming edge)
            # Additionally, ensure this isn't part of a cycle (already checked above)
            if outgoing and incoming and u not in outgoing:  # Exclude self-loops (already checked)
                hold_wait_detected = True
                break
        if hold_wait_detected:
            return "🔵 Hold and Wait Deadlock (Processes holding resources and waiting)."

        return "No Deadlock"

    def highlight_deadlock(self, deadlocked_processes):
        # Create a gradient for the red highlight
        gradient = QLinearGradient(0, 0, 100, 100)  # Gradient direction
        gradient.setColorAt(0, QColor("#8B0000"))  # Dark red
        gradient.setColorAt(1, QColor("#FF6347"))  # Light red
        brush = QBrush(gradient)

        for process in deadlocked_processes:
            idx = int(process[1:]) - 1  
            for col in range(self.table.columnCount()):
                item = self.table.item(idx, col) or QTableWidgetItem("")
                item.setBackground(brush)  # Apply the gradient brush
                self.table.setItem(idx, col, item)
   
    def fix_deadlock(self):
        if not self.deadlock_graph:
            self.add_message("No deadlock detected to fix.")
            return
       
        try:
            cycle = nx.find_cycle(self.deadlock_graph, orientation='original')
            process_to_remove = cycle[0][0]  # Remove the first process in the cycle
            self.deadlock_graph.remove_node(process_to_remove)
            self.update_table()
            self.add_message(f"✅ Deadlock Resolved! Process {process_to_remove} preempted.")
            self.highlight_fix()
            self.update_chart()
        except nx.NetworkXNoCycle:
            self.add_message("No deadlock to fix.")
   
    def update_table(self):
        processes = ["P1", "P2", "P3", "P4", "P5"]
       
        for i in range(5):
            for j in range(5):
                item = self.table.item(i, j)
                if item:
                    item.setText("1" if (processes[i], processes[j]) in self.deadlock_graph.edges else "0")
   
    def highlight_fix(self):
        # Create a gradient for the green highlight
        gradient = QLinearGradient(0, 0, 100, 100)  # Gradient direction
        gradient.setColorAt(0, QColor("#006400"))  # Dark green
        gradient.setColorAt(1, QColor("#90EE90"))  # Light green
        brush = QBrush(gradient)

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(brush)  # Apply the gradient brush
                    self.table.setItem(row, col, item)
        QTimer.singleShot(15000, self.reset_table)  

    def reset_table(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor("#FFFFFF"))  # Reset to white

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeadlockDetectionAI()
    window.show()
    sys.exit(app.exec())

    
