import sys
import cProfile
import pstats
from gui import security_window, MainWindow
from PyQt6.QtWidgets import QApplication


def main():
    security = security_window()
    security.gui_security()
    app = QApplication([])
    app_window = MainWindow()
    app_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    cProfile.run("main()", 'profile_output.txt')
    p = pstats.Stats('profile_output.txt')
    p.sort_stats('cumulative').print_stats(10)

