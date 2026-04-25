import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from dashboard import DashboardPage
from Project_detail import ProjectDetailPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Production Manager")
        self.setMinimumSize(1000, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setCentralWidget(self.stacked_widget)
        self.detail_page = ProjectDetailPage(self)

        self.dashboard = DashboardPage(self)

        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.detail_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())