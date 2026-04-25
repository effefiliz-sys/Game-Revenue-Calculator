from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, 
                             QLineEdit, QComboBox, QPushButton, QHBoxLayout, QFileDialog)

class ProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")
        self.setFixedWidth(400)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Please Enter Project Name ")
        form_layout.addRow("Project Name: ", self.name_input)

        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Godot Engine", "Unity", "Unreal Engine", "Pygame"])
        form_layout.addRow("Game Engine: ", self.engine_combo)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["GDScript", "c#", "c++", "Python", "Java", "Blue Print Code"])
        form_layout.addRow("Software Language: ", self.lang_combo)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("No Folder Selected ")
        self.path_input.setReadOnly(True)

        self.browse_btn = QPushButton("Browse ")
        self.browse_btn.clicked.connect(self.browse_folder)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)

        form_layout.addRow("Project Path:", path_layout)

        layout.addLayout(form_layout)

        buttons = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addLayout(buttons)

        self.setLayout(layout)


    
    def browse_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if directory:
            self.path_input.setText(directory)

    def get_data(self):
        return{
            "Name": self.name_input.text(),
            "Engine": self.engine_combo.currentText(),
            "Language": self.lang_combo.currentText(),
            "path": self.path_input.text()
        }