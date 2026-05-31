import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from app.ui import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('智慧大棚农业管理系统')
    app.setApplicationVersion('1.0.0')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
