import sys
from tkinter import *
import base64
from passwd_base64 import get_pass
from typing import List
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLineEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import pyqtSlot, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from load_file import load_data_from_file
from utils import fit_line, calculate_stats


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графинатор")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon("графинатор-ico.ico"))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Predefine instance attributes
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.k_output = QLabel(" ")
        self.b_output = QLabel(" ")
        self.std_dev = QLabel(" ")
        self.confidence = QLabel(" ")

        self.add_btn = QPushButton("Добавить")
        self.calc_btn = QPushButton("Рассчитать")
        self.clear_btn = QPushButton("Очистить")
        self.load_btn = QPushButton("Открыть файл")
        self.save_btn = QPushButton("Сохранить результаты")
        self.exit_btn = QPushButton("Завершить")

        self.dev_text = QLabel("Разработчик")
        self.dev_text.setStyleSheet("QLabel {text-decoration: underline; color: #0099ff;}")
        self.dev_text.setToolTip("Сапожков Вадим\nvdsap@vdsap.com")
        self.dev_text.setToolTipDuration(5000)

        self.dev_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.xy_list = QListWidget()
        self.eq_list = QListWidget()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.x_data = []
        self.y_data = []

        self.init_ui()

    def init_ui(self):
        font = QFont("Arial", 10)

        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Введите X:"))
        input_layout.addWidget(self.x_input)
        input_layout.addWidget(QLabel("Введите Y:"))
        input_layout.addWidget(self.y_input)
        input_layout.addWidget(self.add_btn)
        input_layout.addWidget(self.calc_btn)
        input_layout.addWidget(self.clear_btn)

        result_layout = QHBoxLayout()
        result_layout.addWidget(QLabel("Среднеквадратичное отклонение:"))
        result_layout.addWidget(self.std_dev)
        result_layout.addWidget(QLabel("Доверительный интервал:"))
        result_layout.addWidget(self.confidence)
        result_layout.addWidget(QLabel("Результат K:"))
        result_layout.addWidget(self.k_output)
        result_layout.addWidget(QLabel("Результат B:"))
        result_layout.addWidget(self.b_output)

        list_layout = QVBoxLayout()
        list_layout.addWidget(QLabel("(X, Y)"))
        list_layout.addWidget(self.xy_list)
        list_layout.addWidget(QLabel("Y = B*Xᵏ"))
        list_layout.addWidget(self.eq_list)

        plot_and_lists = QHBoxLayout()
        plot_and_lists.addLayout(list_layout)
        plot_and_lists.addWidget(self.canvas)

        file_layout = QVBoxLayout()
        file_layout.addWidget(self.load_btn)
        file_layout.addWidget(self.save_btn)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.dev_text)
        bottom_layout.addWidget(self.exit_btn)

        layout.addLayout(input_layout)
        layout.addLayout(result_layout)
        layout.addLayout(plot_and_lists)
        layout.addLayout(file_layout)
        layout.addLayout(bottom_layout)

        self.central_widget.setLayout(layout)

        self.add_btn.clicked.connect(self.add_data)
        self.calc_btn.clicked.connect(self.calculate)
        self.clear_btn.clicked.connect(self.clear_all)
        self.exit_btn.clicked.connect(self.close)
        self.load_btn.clicked.connect(self.load_from_file)
        self.save_btn.clicked.connect(self.save_results)


    def add_data(self):
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            self.x_data.append(x)
            self.y_data.append(y)
            self.xy_list.addItem(f"({x}, {y})")
            self.x_input.clear()
            self.y_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите числовые значения X и Y")

    def calculate(self):
        if len(self.x_data) < 2:
            QMessageBox.warning(self, "Ошибка", "Введите минимум два значения для расчета")
            return

        x = np.array(self.x_data)
        y = np.array(self.y_data)

        k, b, y_pred = fit_line(x, y)
        std_dev, ci = calculate_stats(x, y, y_pred)

        self.k_output.setText(f"{k:.2f}")
        self.b_output.setText(f"{b:.2f}")
        self.std_dev.setText(f"{std_dev:.2f}")
        self.confidence.setText(f"±{ci:.2f}")

        self.eq_list.addItem(f"Y = {b:.2f} * (X^{k:.2f}) ")

        self.ax.clear()
        self.ax.plot(x, y, 'bo', label='Данные')
        self.ax.plot(x, y_pred, 'r-', label='Модель')
        self.ax.set_title("График Y = B*Xᵏ")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def clear_all(self):
        self.x_data.clear()
        self.y_data.clear()
        self.xy_list.clear()
        self.eq_list.clear()
        self.k_output.setText("-")
        self.b_output.setText("-")
        self.std_dev.setText("-")
        self.confidence.setText("-")
        self.ax.clear()
        self.canvas.draw()
        self.x_input.clear()
        self.y_input.clear()

    def save_results(self):
        if not self.x_data or not self.y_data:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для сохранения.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить результаты", "results.txt",
                                                   "Text Files (*.txt)")
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("""Результаты расчета:
Входные данные(X, Y):
""")
                for x, y in zip(self.x_data, self.y_data):
                    f.write(f"""({x}, {y})
""")
                f.write(f"""Уравнение: Y = B * X^K"
K: {self.k_output.text()}
B: {self.b_output.text()}
Среднеквадратичное отклонение: {self.std_dev.text()}
Доверительный интервал: {self.confidence.text()}
""")
                QMessageBox.information(self, "Успех", "Результаты успешно сохранены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    @pyqtSlot()
    def load_from_file(self) -> None:
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV файлы (*.csv);;Все файлы (*)")
        if file_dialog.exec():
            selected = file_dialog.selectedFiles()
            if selected:
                file_path = selected[0]
                try:
                    x_data, y_data = load_data_from_file(file_path)
                    self.x_data = x_data
                    self.y_data = y_data
                    self.xy_list.clear()
                    for x, y in zip(x_data, y_data):
                        self.xy_list.addItem(f"({x}, {y})")
                    self.eq_list.clear()
                    self.k_output.clear()
                    self.b_output.clear()
                    self.std_dev.clear()
                    self.confidence.clear()
                    self.ax.clear()
                    self.canvas.draw()
                except RuntimeError as e:
                    QMessageBox.critical(self, "Ошибка", str(e))


class security_window:
    pass_field = None
    window = None

    def gui_security(self):
        self.window = Tk()
        self.window.title("Графинатор-вход")
        self.window.geometry('300x300')
        title_text = Label(self.window, text="Вход", font=("Arial", 20))
        title_text.grid(column=0, row=0, padx=120, pady=50)
        pass_text = Label(self.window, text="Введите пароль", font=("Arial", 10))
        pass_text.grid(column=0, row=1)
        self.pass_field = Entry(self.window, width=25)
        self.pass_field.grid(column=0, row=2)
        self.pass_field.focus()
        enter_btn = Button(self.window, text="Войти", font=("Arial", 10), command=self.gui_security_enter)
        enter_btn.grid(column=0, row=3)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def gui_security_enter(self):
        input_passwrd = self.pass_field.get()
        input_passwrd_bytes = input_passwrd.encode('utf-8')
        input_passwrd_b64_bytes = base64.b64encode(input_passwrd_bytes)
        input_passwrd_b64 = input_passwrd_b64_bytes.decode("utf-8")
        if input_passwrd_b64 == get_pass():
            self.window.destroy()
        else:
            # messagebox.showerror('Ошибка', 'Пароль инвалид')
            self.window.destroy()

    def on_close(self):
        self.window.destroy()
        sys.exit()
