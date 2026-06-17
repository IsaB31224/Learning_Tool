import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QLabel, QVBoxLayout
)
from db.database import init_db
from tool2_reflection.ui import Tool2Widget


def placeholder(name):
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.addWidget(QLabel(name))
    return widget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Learning Tool")
        self.resize(900, 600)

        tabs = QTabWidget()
        tabs.addTab(Tool2Widget(), "Reflection")
        tabs.addTab(placeholder("Tool 1 — Consumption Reflection Layer"), "Consumption")
        tabs.addTab(placeholder("Tool 3 — Narrative & Character Store"), "Narratives")
        tabs.addTab(placeholder("Tool 4 — Notes Organisation"), "Notes")

        self.setCentralWidget(tabs)


def main():
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
