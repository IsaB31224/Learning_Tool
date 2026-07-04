from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QScrollArea,
    QLabel, QTextEdit, QLineEdit, QDateEdit, QPushButton, QMessageBox,
    QStackedWidget, QComboBox, QListWidget
)
from PyQt6.QtCore import QDate, QObject, QThread, pyqtSignal

from tool2_reflection.logic import generate_context_questions, generate_final_question
from db.database import get_connection, get_all_character
from medium import Hash


_STYLESHEET = """
    QWidget {
        background-color: #0f111a;
        color: #e2e8f0;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 12px;
    }
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    QLabel {
        color: #93c5fd;
        font-size: 12px;
        font-weight: 600;
        background-color: transparent;
        padding: 4px 0px;
    }
    QTextEdit {
        background-color: #1c2233;
        color: #e2e8f0;
        border: 2px solid #2d3a55;
        border-radius: 8px;
        padding: 8px;
        font-size: 12px;
    }
    QTextEdit:focus {
        border: 2px solid #3b82f6;
    }
    QTextEdit[readOnly="true"] {
        background-color: #161b27;
        color: #93c5fd;
        border: 2px solid #3b82f6;
        font-size: 14px;
        font-weight: 600;
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
    QDateEdit {
        background-color: #1c2233;
        color: #e2e8f0;
        border: 2px solid #2d3a55;
        border-radius: 8px;
        padding: 6px 10px;
    }
    QDateEdit:focus {
        border: 2px solid #3b82f6;
    }
    QDateEdit::drop-down {
        border: none;
        background-color: #2563eb;
        border-radius: 4px;
        width: 20px;
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
    QPushButton:disabled {
        background-color: #1e2a3a;
        color: #4b5563;
    }
    QPushButton#confirmBtn {
        background-color: #059669;
    }
    QPushButton#confirmBtn:hover {
        background-color: #10b981;
    }
    QPushButton#confirmBtn:pressed {
        background-color: #047857;
    }
    QScrollBar:vertical {
        background-color: #161b27;
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background-color: #3b82f6;
        border-radius: 4px;
        min-height: 24px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0;
    }
"""


class _Worker(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, fn, *args):
        super().__init__()
        self._fn = fn
        self._args = args

    def run(self):
        try:
            self.finished.emit(self._fn(*self._args))
        except Exception as e:
            self.error.emit(str(e))


class Tool2Widget(QWidget):
    def __init__(self):
        super().__init__()
        self._questions = []
        self._thread = None
        self._worker = None
        self._delete_reflections = []
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet(_STYLESHEET)
        root = QVBoxLayout(self)

        self._stack = QStackedWidget()
        root.addWidget(self._stack)

        self._build_menu_page()
        self._build_add_page()
        self._build_delete_page()
        self._build_view_page()

        self._stack.setCurrentIndex(0)

    # --- Page builders ---

    def _build_menu_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addStretch()

        layout.addWidget(QLabel("Tool 2 — Reflection"))

        add_btn = QPushButton("Add Reflection")
        add_btn.clicked.connect(lambda: self._stack.setCurrentIndex(1))
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Delete Reflection")
        delete_btn.clicked.connect(self._on_open_delete)
        layout.addWidget(delete_btn)

        view_btn = QPushButton("View Reflections")
        view_btn.clicked.connect(lambda: self._stack.setCurrentIndex(3))
        layout.addWidget(view_btn)

        layout.addStretch()
        self._stack.addWidget(page)  # index 0

    def _build_add_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)

        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        outer.addWidget(back_btn)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self._layout = QVBoxLayout(container)
        self._layout.setSpacing(12)
        scroll.setWidget(container)
        outer.addWidget(scroll)

        self._build_metadata_section()
        self._build_input_section()
        self._build_question_section()
        self._build_reflection_section()
        self._build_combined_section()
        self._build_finish_section()

        self._stack.addWidget(page)  # index 1

    def _build_delete_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)

        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        outer.addWidget(back_btn)

        row = QHBoxLayout()

        left = QVBoxLayout()
        left.addWidget(QLabel("Character"))
        self.delete_character_combo = QComboBox()
        self.delete_character_combo.currentTextChanged.connect(self._on_delete_character_selected)
        left.addWidget(self.delete_character_combo)

        left.addWidget(QLabel("Reflection ID to delete"))
        self.delete_id_field = QLineEdit()
        left.addWidget(self.delete_id_field)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self._on_delete_reflection)
        left.addWidget(self.delete_btn)
        left.addStretch()

        right = QVBoxLayout()
        right.addWidget(QLabel("Reflections"))
        self.delete_list = QListWidget()
        right.addWidget(self.delete_list)

        row.addLayout(left, 1)
        row.addLayout(right, 2)
        outer.addLayout(row)

        self._stack.addWidget(page)  # index 2

    def _build_view_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        layout.addWidget(back_btn)

        layout.addWidget(QLabel("View Reflections — coming soon"))
        layout.addStretch()

        self._stack.addWidget(page)  # index 3

    # --- Section builders (Add Reflection page) ---

    def _build_metadata_section(self):
        self._meta_section = QWidget()
        form = QFormLayout(self._meta_section)

        self.date_field = QDateEdit(QDate.currentDate())
        self.date_field.setCalendarPopup(True)
        self.media_field = QLineEdit()
        self.author_field = QLineEdit()
        self.topic_field = QLineEdit()
        self.character_field = QLineEdit()

        form.addRow("Date", self.date_field)
        form.addRow("Media *", self.media_field)
        form.addRow("Source Author", self.author_field)
        form.addRow("Topic", self.topic_field)
        form.addRow("Character Referenced", self.character_field)

        self.metadata_btn = QPushButton("Submit Metadata")
        self.metadata_btn.clicked.connect(self._on_metadata_submit)
        form.addRow(self.metadata_btn)

        self._layout.addWidget(self._meta_section)

    def _build_input_section(self):
        self._input_section = QWidget()
        layout = QVBoxLayout(self._input_section)

        layout.addWidget(QLabel("Source Content"))
        self.content_box = QTextEdit()
        layout.addWidget(self.content_box)

        layout.addWidget(QLabel("What did you understand from this content?"))
        self.initial_reflection_box = QTextEdit()
        layout.addWidget(self.initial_reflection_box)

        self.send_btn = QPushButton("Generate Questions")
        self.send_btn.clicked.connect(self._on_send)
        layout.addWidget(self.send_btn)

        self._layout.addWidget(self._input_section)
        self._input_section.hide()

    def _build_question_section(self):
        self._question_section = QWidget()
        layout = QVBoxLayout(self._question_section)

        # Hidden — stores the final question for DB save via _on_confirm
        self.question_box = QTextEdit()
        layout.addWidget(self.question_box)
        self.question_box.hide()

        layout.addWidget(QLabel("Write your response to each question"))

        self._question_displays = []
        self._response_boxes = []

        for i in range(3):
            q_display = QTextEdit()
            q_display.setReadOnly(True)
            q_display.setMaximumHeight(80)
            self._question_displays.append(q_display)
            layout.addWidget(q_display)

            r_box = QTextEdit()
            r_box.setPlaceholderText(f"Your response to question {i + 1}")
            self._response_boxes.append(r_box)
            layout.addWidget(r_box)

        self.final_question_btn = QPushButton("Generate Final Question")
        self.final_question_btn.clicked.connect(self._on_generate_final)
        layout.addWidget(self.final_question_btn)

        self._layout.addWidget(self._question_section)
        self._question_section.hide()

    def _build_reflection_section(self):
        self._reflection_section = QWidget()
        layout = QVBoxLayout(self._reflection_section)

        layout.addWidget(QLabel("Final Question — write your reflection in response"))
        self.additional_reflection_box = QTextEdit()
        layout.addWidget(self.additional_reflection_box)

        layout.addWidget(QLabel("Notes"))
        self.notes_box = QTextEdit()
        layout.addWidget(self.notes_box)

        self.combine_btn = QPushButton("Combine Reflections")
        self.combine_btn.clicked.connect(self._on_combine)
        layout.addWidget(self.combine_btn)

        self._layout.addWidget(self._reflection_section)
        self._reflection_section.hide()

    def _build_combined_section(self):
        self._combined_section = QWidget()
        layout = QVBoxLayout(self._combined_section)

        layout.addWidget(QLabel("Final Reflection"))
        self.combined_box = QTextEdit()
        self.combined_box.setReadOnly(True)
        layout.addWidget(self.combined_box)

        self._layout.addWidget(self._combined_section)
        self._combined_section.hide()

    def _build_finish_section(self):
        self._finish_section = QWidget()
        layout = QVBoxLayout(self._finish_section)

        self.finish_btn = QPushButton("Finish")
        self.finish_btn.clicked.connect(self._on_finish)
        layout.addWidget(self.finish_btn)

        self.confirm_btn = QPushButton("Confirm & Save")
        self.confirm_btn.setObjectName("confirmBtn")
        self.confirm_btn.clicked.connect(self._on_confirm)
        layout.addWidget(self.confirm_btn)

        self._layout.addWidget(self._finish_section)
        self._finish_section.hide()
        self.confirm_btn.hide()

    # --- Delete Reflection page ---

    def _on_open_delete(self):
        self.delete_character_combo.blockSignals(True)
        self.delete_character_combo.clear()
        for row in get_all_character():
            self.delete_character_combo.addItem(row[0])
        self.delete_character_combo.blockSignals(False)

        self.delete_id_field.clear()
        if self.delete_character_combo.count() > 0:
            self._on_delete_character_selected(self.delete_character_combo.currentText())
        else:
            self.delete_list.clear()
            self._delete_reflections = []

        self._stack.setCurrentIndex(2)

    def _on_delete_character_selected(self, character_name):
        self.delete_list.clear()
        self._delete_reflections = []

        if not character_name:
            return

        reflections = Hash.read_character(character_name) or []
        self._delete_reflections = reflections
        for row in reflections:
            reflection_id, media, topic = row[0], row[5], row[6]
            self.delete_list.addItem(f"ID {reflection_id} — {topic or 'No topic'} ({media})")

    def _on_delete_reflection(self):
        character_name = self.delete_character_combo.currentText()
        id_text = self.delete_id_field.text().strip()

        if not character_name:
            QMessageBox.warning(self, "No Character", "Select a character first.")
            return
        if not id_text.isdigit():
            QMessageBox.warning(self, "Invalid ID", "Enter a valid numeric Reflection ID.")
            return

        reflection_id = int(id_text)
        if not any(row[0] == reflection_id for row in self._delete_reflections):
            QMessageBox.warning(self, "Not Found", "That Reflection ID isn't in the list shown.")
            return

        Hash.delete_reflection(character_name, reflection_id)
        self.delete_id_field.clear()
        self._on_delete_character_selected(character_name)
        QMessageBox.information(self, "Deleted", f"Reflection {reflection_id} deleted.")

    # --- Threading ---

    def _start_thread(self, fn, *args, on_done, on_error):
        self._thread = QThread()
        self._worker = _Worker(fn, *args)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(on_done)
        self._worker.error.connect(on_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.error.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    # --- State transitions ---

    def _on_metadata_submit(self):
        if not self.media_field.text().strip():
            QMessageBox.warning(self, "Missing Fields", "Media is required. Please fill it in.")
            return

        for field in [self.media_field, self.author_field, self.topic_field, self.character_field]:
            if field.text().strip():
                field.setStyleSheet("border: 2px solid #10b981;")

        self.metadata_btn.setText("Update Metadata")
        self._input_section.show()

    def _on_send(self):
        content = self.content_box.toPlainText().strip()
        reflection = self.initial_reflection_box.toPlainText().strip()

        if not content:
            QMessageBox.warning(self, "Missing Input", "Please fill in the source content.")
            return
        if not reflection:
            QMessageBox.warning(self, "Missing Input", "Please fill in your understanding of the content.")
            return

        self.send_btn.setEnabled(False)
        self._question_section.show()

        for display in self._question_displays:
            display.setPlainText("Generating...")

        self._start_thread(
            generate_context_questions, content, reflection,
            on_done=self._on_questions_ready,
            on_error=self._on_call_error
        )

    def _on_questions_ready(self, questions):
        self._questions = [q.strip() for q in questions if q.strip()]
        for i, display in enumerate(self._question_displays):
            display.setPlainText(self._questions[i] if i < len(self._questions) else "")

    def _on_generate_final(self):
        responses = [box.toPlainText().strip() for box in self._response_boxes]
        if not all(responses):
            QMessageBox.warning(self, "Missing Input", "Please write a response to each question.")
            return

        self.final_question_btn.setEnabled(False)
        content = self.content_box.toPlainText().strip()
        reflection = self.initial_reflection_box.toPlainText().strip()

        self._start_thread(
            generate_final_question, content, reflection, self._questions, responses,
            on_done=self._on_final_question_ready,
            on_error=self._on_call_error
        )

    def _on_final_question_ready(self, question):
        self.question_box.setPlainText(question)
        self.additional_reflection_box.setPlainText(question)
        self._reflection_section.show()

    def _on_call_error(self, _message):
        QMessageBox.critical(self, "Error", "Request failed. Please try again.")
        self.send_btn.setEnabled(True)
        self.final_question_btn.setEnabled(True)

    def _on_combine(self):
        additional = self.additional_reflection_box.toPlainText().strip()
        if not additional:
            QMessageBox.warning(self, "Missing Input", "Please write your reflection before combining.")
            return

        initial = self.initial_reflection_box.toPlainText().strip()

        qa_parts = []
        for i, (q_display, r_box) in enumerate(zip(self._question_displays, self._response_boxes)):
            q = q_display.toPlainText().strip()
            r = r_box.toPlainText().strip()
            if q and r:
                qa_parts.append(f"Q{i + 1}: {q}\n{r}")

        qa_section = "\n\n".join(qa_parts)
        combined = f"{initial}\n\nCONTEXTUAL QUESTIONS\n\n{qa_section}\n\nFINAL REFLECTION\n\n{additional}"
        self.combined_box.setPlainText(combined)

        self._combined_section.show()
        self._finish_section.show()

    def _on_finish(self):
        self.finish_btn.hide()
        self.confirm_btn.show()

    def _on_confirm(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Reflections
                (Given_prompt, Reflection_Writing, Date, Source_Author, Media,
                 Topic_of_discussion, Abstract_topic, Character_referenced)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.question_box.toPlainText(),
                self.combined_box.toPlainText(),
                self.date_field.date().toString("yyyy-MM-dd"),
                self.author_field.text().strip() or None,
                self.media_field.text().strip(),
                self.topic_field.text().strip() or None,
                self.notes_box.toPlainText().strip() or None,
                self.character_field.text().strip() or None,
            )
        )
        conn.commit()
        conn.close()

        character = self.character_field.text().strip()
        if character:
            Hash.hash_insertion(character)

        QMessageBox.information(self, "Saved", "Reflection logged successfully.")
        self.confirm_btn.setEnabled(False)
