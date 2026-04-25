from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir

class ProjectDetailPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        self.title_label = QLabel("Project Files")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")

        self.model = QFileSystemModel()
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        for i in range(1, 4):
            self.tree.hideColumn(i)

        self.back_btn = QPushButton("<- Get Back to Project List")
        self.back_btn.setFixedSize(180, 35)
        self.back_btn.clicked.connect(self.go_back)

        layout.addWidget(self.title_label)
        layout.addWidget(self.tree)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

    def set_project_path(self, path):
        if QDir(path).exists():
            self.model.setRootPath(path)
            self.tree.setRootIndex(self.model.index(path))
            folder_name = path.split('/')[-1]
            self.title_label.setText(f"Project File: {folder_name}")


    def set_Project_name(self, name):
        self.label.setText(f"Proje: {name}")

    def go_back(self):
        self.main_window.stacked_widget.setCurrentIndex(0)

    def open_project_detail(self, item):
        display_text = item.text()
        project_path = self.get_path_from_name(display_text)

        if hasattr(self.main_window.detail_page, 'set_Project_name'):
            self.main_window.detail_page.set_project_path(project_path)

            self.main_window.stacked_widget.setCurrentIndex(1)
            print(f"Switching To Detail View For: {display_text} | Path: {project_path}")