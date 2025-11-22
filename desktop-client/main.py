import sys
import base64
import requests
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QLineEdit, QHBoxLayout, QTextEdit, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

API_BASE = "http://127.0.0.1:8000/api"


class ModernFrame(QFrame):
    """Reusable modern white rounded card."""
    def __init__(self, padding=20):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 14px;
                border: 1px solid #d9e2ec;
            }
        """)
        self.setContentsMargins(padding, padding, padding, padding)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(1100, 650)
        self.setStyleSheet("background-color: #f4f6f9; font-family: Segoe UI;")

        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ---------------- SIDEBAR ----------------
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1b3a57;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background: #244b70;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #2d5c8d;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)

        title = QLabel("Chemical\nVisualizer")
        title.setFont(QFont("Segoe UI Semibold", 18))
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        btn_upload = QPushButton("Upload CSV")
        btn_upload.clicked.connect(self.handle_upload_click)
        sidebar_layout.addWidget(btn_upload)

        btn_load = QPushButton("Reload Summary")
        btn_load.clicked.connect(self.reload_summary)
        sidebar_layout.addWidget(btn_load)

        sidebar_layout.addStretch()

        # ---------------- MAIN CONTENT ----------------
        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)

        # Credentials bar
        top_bar = ModernFrame(15)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setSpacing(10)

        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Username")
        self.stylize_input(self.user_in)

        self.pw_in = QLineEdit()
        self.pw_in.setPlaceholderText("Password")
        self.pw_in.setEchoMode(QLineEdit.Password)
        self.stylize_input(self.pw_in)

        top_layout.addWidget(self.user_in)
        top_layout.addWidget(self.pw_in)

        content.addWidget(top_bar)

        # Panel containing chart & summary
        panel = ModernFrame(20)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(15)

        # Status label
        self.status_label = QLabel("Upload a file to begin")
        self.status_label.setStyleSheet("font-size: 14px; color: #1b3a57;")
        panel_layout.addWidget(self.status_label)

        # Chart area
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        panel_layout.addWidget(self.canvas)

        # Summary area
        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)
        self.summary_box.setStyleSheet("""
            QTextEdit {
                background: #f7f9fc;
                border: 1px solid #d9e2ec;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        panel_layout.addWidget(self.summary_box)

        content.addWidget(panel)

        main_layout.addWidget(sidebar)
        main_layout.addLayout(content)

    # ---------------- HELPERS ----------------
    def stylize_input(self, widget):
        widget.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                border: 1.8px solid #c7d4e6;
                background: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #1a73e8;
            }
        """)

    def auth_header(self):
        username = self.user_in.text()
        password = self.pw_in.text()
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {"Authorization": f"Basic {token}"}

    # ---------------- LOGIC ----------------
    def handle_upload_click(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if filepath:
            self.upload_csv(filepath)

    def upload_csv(self, filepath):
        self.status_label.setText("Uploading file...")

        try:
            files = {"file": open(filepath, "rb")}
            response = requests.post(
                f"{API_BASE}/upload/",
                files=files,
                headers=self.auth_header()
            )

            if response.status_code == 201:
                self.status_label.setText("Upload successful")
                dataset = response.json()
                self.load_summary(dataset["id"])
            else:
                self.status_label.setText("Upload failed")
                self.summary_box.setPlainText(response.text)

        except Exception as e:
            self.status_label.setText("Upload error")
            self.summary_box.setPlainText(str(e))

    def reload_summary(self):
        self.status_label.setText("Reload functionality can be extended.")

    def load_summary(self, dataset_id):
        try:
            response = requests.get(
                f"{API_BASE}/datasets/{dataset_id}/summary/",
                headers=self.auth_header()
            )
            if response.ok:
                summary = response.json()
                self.show_summary(summary)
        except Exception as e:
            self.summary_box.setPlainText(str(e))

    # ---------------- STRUCTURED SUMMARY ----------------
    def show_summary(self, summary):
        total = summary.get("total_count", 0)

        # Averages
        avg = summary.get("averages", {})
        avg_text = "".join([f"    • {k}: {round(v, 2)}\n" for k, v in avg.items()])

        # Type distribution
        dist = summary.get("type_distribution", {})
        dist_text = "".join([f"    • {k}: {v}\n" for k, v in dist.items()])

        formatted = (
            f"SUMMARY REPORT\n"
            f"----------------------------\n"
            f"Total Equipment: {total}\n\n"
            f"Averages:\n{avg_text if avg_text else '    No average data available'}\n"
            f"Equipment Distribution:\n{dist_text if dist_text else '    No distribution data available'}"
        )

        self.summary_box.setPlainText(formatted)

        # ---- Update Chart ----
        labels = list(dist.keys())
        values = list(dist.values())

        self.ax.clear()
        if labels:
            self.ax.bar(labels, values, color="#1a73e8")
            self.ax.set_title("Equipment Count by Type", fontsize=12)
            self.ax.set_xlabel("Type")
            self.ax.set_ylabel("Count")
        else:
            self.ax.text(0.5, 0.5, "No data available", ha="center")

        self.canvas.draw()


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
