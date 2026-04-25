from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTreeView, QSplitter, QTextEdit, QHBoxLayout
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir, Qt
import os 

class ProjectDetailPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.model = QFileSystemModel()
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        for i in range(1, 4): self.tree.hideColumn(i)
        self.tree.setHeaderHidden(True)
        self.tree.setFixedWidth(250)
        self.tree.setFrameStyle(0)

        self.title_label = QLabel("Project: -")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #888;")

        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setContentsMargins(10, 5, 10, 5)
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.title_label)

        self.editor_container = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_container)
        self.editor_layout.setContentsMargins(0, 0, 0, 0)
        self.editor_layout.setSpacing(0)

        self.close_btn = QPushButton("x")
        self.close_btn.setFixedSize(30, 25)
        self.close_btn.setStyleSheet("background: #2d2d2d; color: white; border: none;")
        self.close_btn.clicked.connect(lambda: self.editor_container.hide())

        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setFrameStyle(0)
        self.editor.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: 'Consolas' , monospace;")

        self.editor_layout.addWidget(self.close_btn, alignment=Qt.AlignmentFlag.AlignRight)
        self.editor_layout.addWidget(self.editor)
        self.editor_container.hide()

        self.back_btn = QPushButton("<- Back To Projects ")
        self.back_btn.setFixedSize(150, 30)
        self.back_btn.clicked.connect(self.go_back)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.tree)

        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        self.right_layout.addLayout(self.top_bar_layout)
        self.right_layout.addWidget(self.editor_container)
        self.right_layout.addStretch()
        self.right_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.splitter.addWidget(self.right_panel)

        self.splitter.handle(1).setEnabled(False)
        self.splitter.setStyleSheet("QSplitter::handle { background: transparent; }")

        self.main_layout.addWidget(self.splitter)

        self.tree.doubleClicked.connect(self.on_file_clicked)


    def on_file_clicked(self, index):
        file_path = self.model.filePath(index)

        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.editor.setPlainText(content)
                    self.editor_container.show()
            except Exception as e:
                self.editor.setPlainText(f"Reading Error: {e}")
                self.editor_container.show()

    def set_project_path(self, path):
        if QDir(path).exists():
            self.model.setRootPath(path)
            self.tree.setRootIndex(self.model.index(path))
            folder_name = path.split('/')[-1]
            self.title_label.setText(f"Project File: {folder_name}")


    def set_Project_name(self, name):
        self.title_label.setText(f"Proje: {name}")

    def go_back(self):
        self.main_window.stacked_widget.setCurrentIndex(0)

    def open_project_detail(self, item):
        display_text = item.text()
        project_path = self.get_path_from_name(display_text)

        if hasattr(self.main_window.detail_page, 'set_Project_name'):
            self.main_window.detail_page.set_project_path(project_path)

            self.main_window.stacked_widget.setCurrentIndex(1)
            print(f"Switching To Detail View For: {display_text} | Path: {project_path}")