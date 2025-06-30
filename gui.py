from tkinter import *
from tkinter import messagebox
import base64
from passwd_base64 import get_pass
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class main_window:
    class qt_window(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Графинатор")
            button = QPushButton("Press Me!")
            self.setCentralWidget(button)
            self.setFixedSize(QSize(1200, 700))

    def gui_main(self):
        app = QApplication([])
        window = self.qt_window()
        window.show()
        app.exec()


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
        self.window.mainloop()

    def gui_security_enter(self):
        input_passwrd = self.pass_field.get()
        input_passwrd_bytes = input_passwrd.encode('utf-8')
        input_passwrd_b64_bytes = base64.b64encode(input_passwrd_bytes)
        input_passwrd_b64 = input_passwrd_b64_bytes.decode("utf-8")
        if input_passwrd_b64 == get_pass():
            self.window.destroy()
        else:
            messagebox.showerror('Ошибка', 'Пароль инвалид')
