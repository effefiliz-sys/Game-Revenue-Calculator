from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTreeView, QSplitter, QTextEdit, QHBoxLayout, QScrollArea, QFrame, QLineEdit, QSizePolicy, QLineEdit
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir, Qt
import os 
import json

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

        self.main_scroll = QScrollArea()
        self.main_scroll.setWidgetResizable(True)
        self.main_scroll.setFrameStyle(0)
        self.main_scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { width: 8px; background: #1e1e1e; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #3e3e42; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #4e4e52; }
            """)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)

        self.scroll_layout.addLayout(self.top_bar_layout)
        self.scroll_layout.addWidget(self.editor_container)

        self.setup_dynamic_contacts()
        self.scroll_layout.addStretch()

        self.main_scroll.setWidget(self.scroll_content)
        self.right_layout.addWidget(self.main_scroll)

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

    def setup_dynamic_contacts(self):
        self.contact_card = QFrame()
        self.contact_card.setStyleSheet("""
            QFrame {
                background-color: transparent; 
                border-radius: 8px; 
                padding: 15px;
            }
        """)
        self.contact_card.setMaximumWidth(500)
        card_layout = QVBoxLayout(self.contact_card)

        title = QLabel("Project Team ")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #569cd6")
        card_layout.addWidget(title)

        h_box = QHBoxLayout()
        self.c_name = QLineEdit(); self.c_name.setPlaceholderText("Name")
        self.c_name.setStyleSheet("background: #1e1e1e; color: white; padding: 5px; border: 1px solid #333;")

        add_btn = QPushButton("+")
        add_btn.setFixedSize(24, 24)
        add_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50; 
                color: white; 
                font-weight: bold; 
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #66bb6a;
            }
        """)
        add_btn.clicked.connect(self.add_new_plank)

        h_box.addWidget(self.c_name)
        h_box.addWidget(add_btn)
        card_layout.addLayout(h_box)

        self.planks_container = QVBoxLayout()
        card_layout.addLayout(self.planks_container)

        self.scroll_layout.addWidget(self.contact_card)  

        self.load_team_data()

    def add_new_plank(self, save=True):
        user_name = self.c_name.text().strip()

        if not user_name:
            return
        
        profile_card = QFrame()
        profile_card.setEnabled(True)
        profile_card.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        profile_card.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        profile_card.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e; /* Panelin kendi gri tonu */
                border: 1px solid #333;    /* Çok hafif belirgin bir çerçeve */
                border-radius: 6px;
            }
        """)

        main_v_layout = QVBoxLayout(profile_card)

        top_bar = QWidget()
        top_bar.setStyleSheet("background: transparent; border: none;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 5, 10, 5)

        name_label = QLabel(user_name)
        name_label.setStyleSheet("color: #d4d4d4; font-weight: bold; border: none;")

        expand_btn = QPushButton("↓")
        expand_btn.setFixedSize(20, 20)
        expand_btn.setStyleSheet("""
            QPushButton { background: #4CAF50; color: white; border-radius: 10px; font-weight: bold; }
            QPushButton:hover { background: #66bb6a; }
        """)

        remove_btn = QPushButton("-")
        remove_btn.setFixedSize(20, 20)
        remove_btn.setStyleSheet("""
            QPushButton { background: #c42b1c; color: white; border-radius: 10px; font-weight: bold; }
            QPushButton:hover { background: #e81123; }
        """)

        top_layout.addWidget(name_label)
        top_layout.addStretch()
        top_layout.addWidget(expand_btn)
        top_layout.addWidget(remove_btn)

        details_panel = QWidget()
        details_layout = QVBoxLayout(details_panel)
        details_panel.setVisible(False)
        details_panel.setStyleSheet("background: #252526; border: 1px solid #444;")

        role_input = QLineEdit()
        role_input.setPlaceholderText("Role")
        contact_input = QLineEdit()
        contact_input.setPlaceholderText("Contact")

        role_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        contact_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        role_input.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)

        for inp in [role_input, contact_input]:
            inp.setStyleSheet("background: #1e1e1e; color: #ccc; border: 1px solid #333; padding: 5px; margin-top: 5px;")
            details_layout.addWidget(inp)
            inp.textChanged.connect(self.save_team_data)
        
        def toggle_details():
            is_visible = details_panel.isVisible()
            details_panel.setVisible(not is_visible)

            expand_btn.setText("↑" if not is_visible else "↓")

            self.scroll_content.adjustSize()
            self.main_scroll.viewport().update()
            print(f"Panel Status: {not is_visible}")

        expand_btn.clicked.connect(toggle_details)

        def remove_and_save():
            profile_card.hide()
            profile_card.setParent(None)
            self.save_team_data()
            profile_card.deleteLater()
        
        remove_btn.clicked.connect(remove_and_save)

        main_v_layout.addWidget(top_bar)
        main_v_layout.addWidget(details_panel)

        self.planks_container.addWidget(profile_card)
        self.c_name.clear()

        if save:
            self.save_team_data()



    def remove_plank(self, layout, input_widget, button_widget):
        input_widget.deleteLater()
        button_widget.deleteLater()
        layout.deleteLater()

    def save_team_data(self):
        team_list = []

        for i in range(self.planks_container.count()):
            card = self.planks_container.itemAt(i).widget()
            if card:
                name = card.findChild(QLabel).text()
                inputs = card.findChildren(QLineEdit)
                role = inputs[0].text() if len(inputs) > 0 else ""
                contact = inputs[1].text() if len(inputs) > 1 else ""

                team_list.append({
                    "name": name,
                    "role": role,
                    "contact": contact
                })

        print(f"Number Of Recorded Data: {len(team_list)}")
        with open("team_data.json", "w", encoding="utf-8") as f:
            json.dump(team_list, f, indent=4, ensure_ascii=False)

    def load_team_data(self):
        if not os.path.exists("team_data.json"):
            return
        try:
            with open("team_data.json", "r", encoding="utf-8") as f:
                team_list = json.load(f)
                for member in team_list:
                    self.c_name.setText(member["name"])
                    self.add_new_plank(save=False)

                    last_card = self.planks_container.itemAt(self.planks_container.count()-1).widget()
                    inputs = last_card.findChildren(QLineEdit)
                    if len(inputs) >= 2:
                        inputs[0].setText(member.get("role", ""))
                        inputs[1].setText(member.get("contact", ""))
            self.c_name.clear()   
        except Exception as e:
            print(f"Downloading Error: {e}")

