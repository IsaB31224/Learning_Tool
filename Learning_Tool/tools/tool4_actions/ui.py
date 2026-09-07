# PyQt6 UI for Tool 4 — menu with two pressable boxes that swap the on-screen page

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QPushButton,
    QComboBox, QListWidget, QTextEdit, QLineEdit
)
from PyQt6.QtCore import Qt

from db.database import get_all_character
from shared.hash_instance import Hash
from tools.tool4_actions import graph


_STYLESHEET = """
    QWidget {
        background-color: #0f111a;
        color: #e2e8f0;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 12px;
    }
    QLabel {
        color: #93c5fd;
        font-size: 12px;
        font-weight: 600;
        background-color: transparent;
        padding: 4px 0px;
    }
    QLabel#pageTitle {
        font-size: 16px;
        font-weight: 700;
    }
    QPushButton {
        background-color: #2563eb;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 13px;
        font-weight: 700;
    }
    QPushButton:hover {
        background-color: #3b82f6;
    }
    QPushButton:pressed {
        background-color: #1d4ed8;
    }
    QPushButton#navBox {
        background-color: #1c2233;
        color: #e2e8f0;
        border: 2px solid #2d3a55;
        border-radius: 12px;
        padding: 24px;
        font-size: 15px;
        font-weight: 700;
        min-height: 140px;
    }
    QPushButton#navBox:hover {
        border: 2px solid #3b82f6;
        background-color: #202840;
    }
    QPushButton#navBox:pressed {
        background-color: #161b27;
    }
    QComboBox {
        background-color: #1c2233;
        color: #e2e8f0;
        border: 2px solid #2d3a55;
        border-radius: 8px;
        padding: 6px 10px;
    }
    QComboBox:focus {
        border: 2px solid #3b82f6;
    }
    QComboBox QAbstractItemView {
        background-color: #1c2233;
        color: #e2e8f0;
        selection-background-color: #2563eb;
    }
    QListWidget {
        background-color: #1c2233;
        color: #e2e8f0;
        border: 2px solid #2d3a55;
        border-radius: 8px;
        padding: 4px;
    }
    QListWidget::item {
        padding: 6px;
    }
    QListWidget::item:selected {
        background-color: #2563eb;
        border-radius: 4px;
    }
    QTextEdit {
        background-color: #1c2233;
        color: #e2e8f0;
        border: 2px solid #2d3a55;
        border-radius: 8px;
        padding: 8px;
        font-size: 12px;
    }
    QTextEdit[readOnly="true"] {
        background-color: #161b27;
        color: #93c5fd;
    }
    QLineEdit {
        background-color: #1c2233;
        color: #e2e8f0;
        border: 2px solid #2d3a55;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 12px;
    }
    QLineEdit:focus {
        border: 2px solid #3b82f6;
    }
"""


class Tool4Widget(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    # --- helpers ---

    def _graph_has_data(self):
        # No persisted graph yet (graph.py is still being built) — always empty for now.
        return False

    # --- UI ---

    def _build_ui(self):
        self.setStyleSheet(_STYLESHEET)
        root = QVBoxLayout(self)

        self._stack = QStackedWidget()
        root.addWidget(self._stack)

        self._build_menu_page()          # index 0
        self._build_graph_page()         # index 1
        self._build_add_sequence_page()  # index 2
        self._build_workflow_id_page()   # index 3

        self._stack.setCurrentIndex(0)

    def _build_menu_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addStretch()

        title = QLabel("Tool 4 — Actions")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        row = QHBoxLayout()

        self.view_graph_box = QPushButton()
        self.view_graph_box.setObjectName("navBox")
        self.view_graph_box.clicked.connect(lambda: self._stack.setCurrentIndex(1))
        row.addWidget(self.view_graph_box)

        add_box = QPushButton("Add Reflection Sequence to Graph")
        add_box.setObjectName("navBox")
        add_box.clicked.connect(self._open_add_sequence)
        row.addWidget(add_box)

        layout.addLayout(row)
        layout.addStretch()

        self._refresh_view_graph_box()
        self._stack.addWidget(page)

    def _refresh_view_graph_box(self):
        if self._graph_has_data():
            self.view_graph_box.setText("View Graph")
        else:
            self.view_graph_box.setText("No data yet")

    def _build_graph_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addStretch()
        self.graph_placeholder = QLabel("No data yet")
        self.graph_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.graph_placeholder)
        layout.addStretch()

        self._stack.addWidget(page)

    def _build_add_sequence_page(self):
        self._sequence_reflections = []

        page = QWidget()
        layout = QVBoxLayout(page)

        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        page_title = QLabel("Add Reflection Sequence to Graph")
        page_title.setObjectName("pageTitle")
        layout.addWidget(page_title)

        row = QHBoxLayout()

        left = QVBoxLayout()
        left.addWidget(QLabel("Character"))
        self.sequence_character_combo = QComboBox()
        self.sequence_character_combo.currentTextChanged.connect(
            self._on_sequence_character_selected
        )
        left.addWidget(self.sequence_character_combo)

        left.addWidget(QLabel("Reflections"))
        self.sequence_list = QListWidget()
        self.sequence_list.currentRowChanged.connect(self._on_sequence_reflection_selected)
        left.addWidget(self.sequence_list)

        right = QVBoxLayout()
        right.addWidget(QLabel("Details"))
        self.sequence_details_box = QTextEdit()
        self.sequence_details_box.setReadOnly(True)
        right.addWidget(self.sequence_details_box)

        row.addLayout(left, 1)
        row.addLayout(right, 2)
        layout.addLayout(row)

        begin_btn = QPushButton("Begin Reflection Workflow Sequence")
        begin_btn.clicked.connect(self._open_workflow_id_page)
        layout.addWidget(begin_btn)

        self._stack.addWidget(page)

    def _build_workflow_id_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self._stack.setCurrentIndex(2))
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        title = QLabel("Reflection Workflow Sequence")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        layout.addStretch()

        layout.addWidget(QLabel("Which character do you want"))
        self.workflow_character_combo = QComboBox()
        layout.addWidget(self.workflow_character_combo)

        layout.addWidget(QLabel("Reflection ID"))
        self.workflow_id_field = QLineEdit()
        self.workflow_id_field.setPlaceholderText("Enter the reflection_id you choose")
        layout.addWidget(self.workflow_id_field)

        layout.addWidget(QLabel("What belief have you realised you hold from this?"))
        self.workflow_belief_box = QTextEdit()
        layout.addWidget(self.workflow_belief_box)

        layout.addWidget(QLabel("What action will you take to oppose the belief?"))
        self.workflow_action_box = QTextEdit()
        layout.addWidget(self.workflow_action_box)

        self.workflow_submit_btn = QPushButton("Submit")
        self.workflow_submit_btn.clicked.connect(self._submit_workflow)
        layout.addWidget(self.workflow_submit_btn)

        self.workflow_status_label = QLabel("")
        layout.addWidget(self.workflow_status_label)

        layout.addStretch()

        self._stack.addWidget(page)

    def _open_workflow_id_page(self):
        # Repopulate the character list but keep the current pick so page-3 inputs
        # survive a Back-to-page-2-and-return (user reviewing their reflection mid-flow).
        previous = self.workflow_character_combo.currentText()
        self.workflow_character_combo.clear()
        for row in get_all_character():
            self.workflow_character_combo.addItem(row[0])
        if previous:
            self.workflow_character_combo.setCurrentText(previous)
        self._stack.setCurrentIndex(3)

    def _submit_workflow(self):
        # _submit_workflow(self) -> None
        #
        # Fires on the page-3 Submit button. Turns the four page-3 widget values into
        # arguments for graph.reflection_workflow and calls it. The graph grows in
        # place — graph.py's module-level adj_dict / node_dict are extended, never
        # reset here.
        #
        # Reads off the widgets:
        #   character_name : str -- workflow_character_combo.currentText()
        #   raw_id         : str -- workflow_id_field.text()
        #   belief         : str -- workflow_belief_box.toPlainText()
        #   action         : str -- workflow_action_box.toPlainText()
        #
        # Guards, in order — each writes workflow_status_label and returns early:
        #   (1) reflection_id = int(raw_id); empty / non-numeric -> ValueError ->
        #       "Reflection ID must be a whole number." and stop.
        #   (2) reflections = Hash.read_character(character_name), wrapped so a None
        #       return and a TypeError (empty / NULL-character slot — CLAUDE.md rough
        #       edge) both -> "No reflections stored for '<name>'." and stop.
        #   (3) reflection_workflow no longer returns a found/not-found signal, so the
        #       not-found check is done here up front via graph.node_extraction
        #       (graph's own lookup, not a reimplementation). None -> "No reflection
        #       with ID <id> for '<name>'." and stop.
        #
        # belief / action are passed through as-is; blank is allowed for now.
        character_name = self.workflow_character_combo.currentText()
        belief = self.workflow_belief_box.toPlainText()
        action = self.workflow_action_box.toPlainText()

        try:
            reflection_id = int(self.workflow_id_field.text())
        except ValueError:
            self.workflow_status_label.setText("Reflection ID must be a whole number.")
            return

        try:
            reflections = Hash.read_character(character_name)
        except TypeError:
            reflections = None
        if not reflections:
            self.workflow_status_label.setText(
                f"No reflections stored for '{character_name}'."
            )
            return

        if graph.node_extraction(reflections, reflection_id) is None:
            self.workflow_status_label.setText(
                f"No reflection with ID {reflection_id} for '{character_name}'."
            )
            return

        graph.reflection_workflow(reflection_id, reflections, belief, action)
        self.workflow_status_label.setText(
            f"Sequence added to graph for reflection {reflection_id}."
        )

    def _open_add_sequence(self):
        self.sequence_character_combo.blockSignals(True)
        self.sequence_character_combo.clear()
        for row in get_all_character():
            self.sequence_character_combo.addItem(row[0])
        self.sequence_character_combo.blockSignals(False)

        if self.sequence_character_combo.count() > 0:
            self._on_sequence_character_selected(self.sequence_character_combo.currentText())
        else:
            self.sequence_list.clear()
            self.sequence_details_box.clear()
            self._sequence_reflections = []

        self._stack.setCurrentIndex(2)

    def _on_sequence_character_selected(self, character_name):
        self.sequence_list.clear()
        self.sequence_details_box.clear()
        self._sequence_reflections = []

        if not character_name:
            return

        reflections = Hash.read_character(character_name) or []
        self._sequence_reflections = reflections
        for row in reflections:
            reflection_id, media, topic = row[0], row[5], row[6]
            self.sequence_list.addItem(
                f"ID {reflection_id} — {topic or 'No topic'} ({media})"
            )

    def _on_sequence_reflection_selected(self, row_index):
        if row_index < 0 or row_index >= len(self._sequence_reflections):
            self.sequence_details_box.clear()
            return

        row = self._sequence_reflections[row_index]
        (reflection_id, given_prompt, reflection_writing, date,
         source_author, media, topic, abstract_topic, character) = row

        details = (
            f"Reflection ID: {reflection_id}\n"
            f"Date: {date}\n"
            f"Media: {media}\n"
            f"Source Author: {source_author or '-'}\n"
            f"Topic: {topic or '-'}\n"
            f"Character Referenced: {character or '-'}\n\n"
            f"Given Prompt:\n{given_prompt}\n\n"
            f"Reflection Writing:\n{reflection_writing}\n\n"
            f"Notes:\n{abstract_topic or '-'}"
        )
        self.sequence_details_box.setPlainText(details)
