import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QCalendarWidget, QTextEdit, QLabel, QPushButton

class SettingsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        self.label = QLabel("Chooe Theme: ")
        self.dark_btn = QPushButton("Dark Mode")
        self.light_btn = QPushButton("Light Mode")

        self.dark_btn.clicked.connect(self.set_dark_theme)
        self.light_btn.clicked.connect(self.set_light_theme)

        layout.addWidget(self.label)
        layout.addWidget(self.dark_btn)
        layout.addWidget(self.light_btn)
        layout.addStretch()
        self.setLayout(layout)

    def set_dark_theme(self):
        dark_qss = """
            QWidget { background-color: #2b2b2b; color: #ffffff; }
            QCalendarWidget QWidget { background-color: #353535; color: #ffffff; }
            QTextEdit { background-color: #1e1e1e; border: 1px solid #555; }
            QPushButton { background-color: #444; border: 1px solid #666; padding: 5px; }
            QPushButton:hover { background-color: #555; }
        """
        QApplication.instance().setStyleSheet(dark_qss)

    def set_light_theme(self):
        light_qss = """
            QWidget { background-color: #f0f0f0; color: #000000; }
            QCalendarWidget QWidget { background-color: #ffffff; color: #000000; }
            QTextEdit { background-color: #ffffff; border: 1px solid #ccc; }
            QPushButton { background-color: #e1e1e1; border: 1px solid #bbb; padding: 5px; }
            QPushButton:hover { background-color: #d5d5d5; }
        """
        QApplication.instance().setStyleSheet(light_qss)

class Game_Production_Calendar(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Game Production Calendar")
        self.setMinimumSize(1000, 600)

        
        self.left_side_panel = QVBoxLayout()
        self.left_side_panel.setContentsMargins(0, 0, 0, 0)
        
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setFixedSize(100, 30) 

        self.settings_btn.clicked.connect(self.open_settings)
        
        self.left_side_panel.addWidget(self.settings_btn)
        self.left_side_panel.addStretch()

        self.right_panel = QVBoxLayout()
        
        self.Calendar = QCalendarWidget()
        self.Calendar.setMaximumWidth(400)
        
        self.ticket = QLabel("Selected Date Data: ")
        self.text_area = QTextEdit()
        self.text_area.setMaximumHeight(250)
        self.text_area.setMaximumWidth(400)
        
        self.right_panel.addWidget(self.Calendar)
        self.right_panel.addWidget(self.ticket)
        self.right_panel.addWidget(self.text_area)

        
        self.Main_layout = QHBoxLayout()
        self.Main_layout.setContentsMargins(30, 30, 30, 30)
        self.Main_layout.setSpacing(20)
        
        self.Main_layout.addLayout(self.left_side_panel)
        self.Main_layout.addStretch(3)
        self.Main_layout.addLayout(self.right_panel, 1)

        centre_widget = QWidget()
        centre_widget.setLayout(self.Main_layout)
        self.setCentralWidget(centre_widget)

        self.Calendar.selectionChanged.connect(self.show_data)
 
    def show_data(self):
        selected_date = self.Calendar.selectedDate().toString("d.M.yyyy")
        self.ticket.setText(f"Selected Date: {selected_date}")

        try:
            with open("Game_Production_Calendar_Data.json", "r", encoding="utf-8") as file:
                all_data =json.load(file)

            found_projects = ""
            for project in all_data:
                if project["Date"] == selected_date:
                    found_projects += f"Project: {project['Project_Name']}\n"
                    found_projects += f"Gross İncome: {project['Income']} {project.get('Currency', 'TL')}\n"
                    found_projects += "-"*25 +"\n"
            
            if found_projects:
                self.text_area.setText(found_projects)
            else:
                self.text_area.setText("No Data Recorded On This Date. ")
        
        except FileNotFoundError:
            self.text_area.setText("The Database (JSON) File Has Not Yet Been Created. ")

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = Game_Production_Calendar()
    windows.show()
    sys.exit(app.exec())

