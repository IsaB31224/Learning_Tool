from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGraphicsScene, QGraphicsView,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsItem,
    QStackedWidget, QLabel, QTextEdit, QPushButton, QLineEdit
)
from PyQt6.QtGui import QBrush, QPen, QColor, QFont, QPainter
from PyQt6.QtCore import Qt
from tool1_contents.logic import Root_node, dfs_traversal, node_search

NODE_WIDTH = 140
NODE_HEIGHT = 40
H_GAP = 24
V_GAP = 90

SCENE_BG = QColor("#0f111a")
BOX_FILL = QColor("#2563eb")
BOX_BORDER = QColor("#3b82f6")
LINE_COLOR = QColor("#3b82f6")
TEXT_COLOR = QColor("#ffffff")


def _assign_positions(node, depth, next_x, positions):
    if not node.child:
        x = next_x[0] * (NODE_WIDTH + H_GAP)
        next_x[0] += 1
    else:
        child_xs = [
            _assign_positions(child, depth + 1, next_x, positions)
            for child in node.child
        ]
        x = sum(child_xs) / len(child_xs)

    positions[node] = (x, depth * V_GAP)
    return x


def _draw_node(scene, node, positions):
    x, y = positions[node]

    box = QGraphicsRectItem(x, y, NODE_WIDTH, NODE_HEIGHT)
    box.setBrush(QBrush(BOX_FILL))
    box.setPen(QPen(BOX_BORDER, 2))
    box.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
    box.setCursor(Qt.CursorShape.PointingHandCursor)
    box.node = node
    scene.addItem(box)

    label = QGraphicsTextItem(node.theme)
    label.setDefaultTextColor(TEXT_COLOR)
    label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
    label.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
    label_rect = label.boundingRect()
    label.setPos(
        x + (NODE_WIDTH - label_rect.width()) / 2,
        y + (NODE_HEIGHT - label_rect.height()) / 2,
    )
    scene.addItem(label)

    for child in node.child:
        cx, cy = positions[child]
        line = QGraphicsLineItem(
            x + NODE_WIDTH / 2, y + NODE_HEIGHT,
            cx + NODE_WIDTH / 2, cy,
        )
        line.setPen(QPen(LINE_COLOR, 2))
        scene.addItem(line)
        _draw_node(scene, child, positions)


class Tool1Widget(QWidget):
    def __init__(self):
        super().__init__()

        self._nodes_list = dfs_traversal(Root_node)

        outer_layout = QVBoxLayout(self)

        self.stack = QStackedWidget()
        outer_layout.addWidget(self.stack)

        self.graph_page = self._build_graph_page()
        self.detail_page = self._build_detail_page()

        self.stack.addWidget(self.graph_page)
        self.stack.addWidget(self.detail_page)

    def _build_graph_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        search_row = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search theme...")
        self.search_box.returnPressed.connect(self._on_search)
        search_row.addWidget(self.search_box)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self._on_search)
        search_row.addWidget(search_button)

        layout.addLayout(search_row)

        self.search_status = QLabel()
        self.search_status.setStyleSheet("color: #f87171;")
        layout.addWidget(self.search_status)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(SCENE_BG))
        self.scene.selectionChanged.connect(self._on_node_clicked)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout.addWidget(self.view)

        positions = {}
        _assign_positions(Root_node, 0, [0], positions)
        _draw_node(self.scene, Root_node, positions)

        self.view.setSceneRect(self.scene.itemsBoundingRect().adjusted(-20, -20, 20, 20))

        return page

    def _build_detail_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        close_row = QHBoxLayout()
        close_row.addStretch()
        close_button = QPushButton("X")
        close_button.setFixedSize(28, 28)
        close_button.clicked.connect(self._close_detail)
        close_row.addWidget(close_button)
        layout.addLayout(close_row)

        header = QLabel("Selected Theme")
        layout.addWidget(header)

        self.detail_name_box = QLabel()
        self.detail_name_box.setStyleSheet(
            f"background-color: {BOX_FILL.name()}; color: white; "
            f"border: 2px solid {BOX_BORDER.name()}; border-radius: 4px; "
            f"padding: 8px; font-weight: bold;"
        )
        layout.addWidget(self.detail_name_box)

        self.detail_text_box = QTextEdit()
        layout.addWidget(self.detail_text_box)

        return page

    def _on_node_clicked(self):
        selected = self.scene.selectedItems()
        if not selected:
            return

        node = selected[0].node
        text = node_search(self._nodes_list, node.theme)

        self.detail_name_box.setText(node.theme)
        self.detail_text_box.setPlainText(text or "")
        self.stack.setCurrentWidget(self.detail_page)

    def _close_detail(self):
        self.scene.clearSelection()
        self.stack.setCurrentWidget(self.graph_page)

    def _on_search(self):
        query = self.search_box.text().strip()
        if not query:
            return

        result = node_search(self._nodes_list, query)

        if result is None:
            self.search_status.setText(f'No theme found for "{query}"')
            return

        self.search_status.setText("")
        self.detail_name_box.setText(query)
        self.detail_text_box.setPlainText(result)
        self.stack.setCurrentWidget(self.detail_page)
