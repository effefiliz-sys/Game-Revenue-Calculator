import json
import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QCalendarWidget, QTextEdit, QFrame
from PyQt6.QtCore import Qt
from Project_dialog import ProjectDialog

class DashboardPage(QWidget):
    def __init__(self, main_window):
        
        super().__init__()
        self.main_window = main_window

        self.main_h_layout = QHBoxLayout(self)
        self.main_h_layout.setContentsMargins(10, 10, 10, 10)
        self.main_h_layout.setSpacing(15)

        self.left_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        self.add_btn = QPushButton("+ New Project ")
        self.add_btn.setFixedSize(120, 35)
        self.remove_btn = QPushButton("- Remove Project")
        self.remove_btn.setFixedSize(120, 30)
        self.remove_btn.clicked.connect(self.remove_project)
        self.add_btn.clicked.connect(self.open_create_dialog)
        self.remove_btn.clicked.connect(self.remove_project)

        self.project_list = QListWidget()

        self.project_list.itemDoubleClicked.connect(self.open_project_detail)
    
        header = QHBoxLayout()
        self.title = QLabel("Project management ")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")

        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.add_btn)
        header.addWidget(self.remove_btn)

        self.left_layout.addLayout(header)
        self.left_layout.addWidget(self.project_list)

        self.right_panel = QFrame()
        self.right_panel.setFixedWidth(350)
        self.right_panel.setStyleSheet("background-color: #252526; border-radius: 8px; border: 1px solid #333;")
        self.right_layout = QVBoxLayout(self.right_panel)

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget QAbstractItemView:enabled { 
                background-color: #1e1e1e; 
                color: #d4d4d4; 
                selection-background-color: #3d3d3d; 
                selection-color: white;
            }
            QCalendarWidget QWidget { alternate-background-color: #252526; color: #aaa; }
            QCalendarWidget QToolButton { color: white; border: none; font-weight: bold; }
        """)

        self.daily_notes = QTextEdit()
        self.daily_notes.setPlaceholderText("Take Notes Here ")
        self.daily_notes.textChanged.connect(self.save_notes)

        self.daily_notes.setStyleSheet("background-color: #1e1e1e; color: white; border: none; padding: 10px;")

        self.right_layout.addWidget(QLabel("Calendar"))
        self.right_layout.addWidget(self.calendar)
        self.right_layout.addWidget(QLabel("Notes"))
        self.right_layout.addWidget(self.daily_notes)

        self.main_h_layout.addWidget(self.left_container, stretch=65)
        self.main_h_layout.addWidget(self.right_panel, stretch=35)

        self.load_Projects()
        self.load_notes()
        self.daily_notes.textChanged.connect(self.save_notes)

    def open_create_dialog(self):
        dialog = ProjectDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            
            project_entry = f"{data['Name']} - {data['Engine']} [{data['Language']}]"
            self.project_list.addItem(project_entry)

            current_projects = []
            if os.path.exists("projects.json"):
                with open("projects.json", "r", encoding="utf-8") as f:
                    try:
                        current_projects = json.load(f)
                        if not isinstance(current_projects, list): current_projects = []
                    except:
                        current_projects = []

            current_projects.append(data)

            with open("projects.json", "w", encoding="utf-8")as f:
                json.dump(current_projects, f, ensure_ascii=False, indent=4)

            print(f"Added On List: {project_entry}")

    def save_projects(self):
        projects = []
        for i in range(self.project_list.count()):
            projects.append(self.project_list.item(i).text())

        with open("projects.json", "w", encoding="utf-8") as f:
            json.dump(projects, f, ensure_ascii=False, indent=4)
        pass

    def load_Projects(self):
        if os.path.exists("projects.json"):
            with open("projects.json", "r", encoding="utf-8") as f:
                try:
                    projects = json.load(f)
                    for p in projects:
                        if isinstance(p, dict):
                            entry = f"{p['Name']} - {p['Engine']} [{p['Language']}]"
                            self.project_list.addItem(entry)
                        else:
                            self.project_list.addItem(p)
                except:
                    pass        

    def remove_project(self):
        current_item = self.project_list.currentItem()

        if current_item:
            row = self.project_list.row(current_item)
            self.project_list.takeItem(row)

            if os.path.exists("projects.json"):
                with open("projects.json", "r", encoding="utf-8") as f:
                    projects = json.load(f)

                if row < len(projects):
                    projects.pop(row)
                with open("projects.json", "w", encoding="utf-8") as f:
                    json.dump(projects, f, ensure_ascii=False, indent=4)

        
            print("Project Removed And Json Synced ")

    def open_project_detail(self, item):
        project_name = item.text()
        if hasattr(self.main_window.detail_page, 'set_project_name'):
            self.main_window.detail_page.set_project_name(project_name)

        self.main_window.stacked_widget.setCurrentIndex(1)
        print(f"Switching To Detail View For: {project_name}")

        project_path = self.get_path_from_name(item.text())

        self.main_window.detail_page.set_project_path(project_path)
        self.main_window.stacked_widget.setCurrentIndex(1)

    def get_path_from_name(self, display_text):
        project_name = display_text.split(" - ")[0].strip().lower()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        filename = os.path.join(current_dir, "projects.json") 

        print(f"Debug: Bakılan dosya -> {filename}")

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    projects = json.load(f)
                    for p in projects:
                        if isinstance(p, dict):
                            json_name = str(p.get("Name")).strip().lower()

                            print(f"Debug: Karşılaştırılıyor -> {json_name} == {project_name}")

                            if json_name == project_name:
                                p_path = p.get("path") or p.get("Path")
                                print(f"Folder Path Found: {p_path}")
                                return p_path if p_path else os.getcwd()
                except Exception as e:
                    print(f"Json Read Error: {e}")
                    
        print("Debug: Dosya bulunamadı veya eşleşme yok!")
        return os.getcwd()
    
    def save_notes(self):
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.write(self.daily_notes.toPlainText())

    def load_notes(self):
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r", encoding="utf-8") as f:
                self.daily_notes.setPlainText(f.read())
        self.daily_notes.setStyleSheet("background-color: #1e1e1e; color: white; font-size: 13px; padding: 10px; border: none;")