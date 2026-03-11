# Nama  : Muhammad Ridho Aidil Furqon
# NIM   : F1D02310127
# Kelas : C

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt

STYLE_INPUT = """
    QLineEdit {
        border: 1px solid #d0d0d0;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #ffffff;
        color: #222222;
        font-size: 13px;
    }
    QLineEdit:focus { border: 1.5px solid #999999; }
"""
STYLE_INPUT_GREEN = """
    QLineEdit {
        border: 1.5px solid #72c472;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #f4fbf4;
        color: #222222;
        font-size: 13px;
    }
"""
STYLE_INPUT_RED = """
    QLineEdit {
        border: 1.5px solid #e05555;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #fff5f5;
        color: #222222;
        font-size: 13px;
    }
"""
LABEL_STYLE = "QLabel { color: #444444; font-size: 13px; background: transparent; border: none; }"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Login")
        self.setMinimumSize(340, 320)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setStyleSheet("QWidget { background-color: #f2f3f5; font-family: 'Segoe UI', Arial, sans-serif; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(0)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("QFrame#card { background-color: #ffffff; border-radius: 10px; border: 1px solid #e0e0e0; }")

        cl = QVBoxLayout(card)
        cl.setContentsMargins(24, 20, 24, 24)
        cl.setSpacing(0)

        btn_header = QPushButton("LOGIN")
        btn_header.setFixedHeight(44)
        btn_header.setEnabled(False)
        btn_header.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 2px;
            }
        """)
        cl.addWidget(btn_header)
        cl.addSpacing(16)

        lbl_user = QLabel("Username:")
        lbl_user.setStyleSheet(LABEL_STYLE)
        cl.addWidget(lbl_user)
        cl.addSpacing(4)

        self.input_user = QLineEdit()
        self.input_user.setFixedHeight(36)
        self.input_user.setStyleSheet(STYLE_INPUT)
        cl.addWidget(self.input_user)
        cl.addSpacing(12)

        lbl_pass = QLabel("Password:")
        lbl_pass.setStyleSheet(LABEL_STYLE)
        cl.addWidget(lbl_pass)
        cl.addSpacing(4)

        self.input_pass = QLineEdit()
        self.input_pass.setFixedHeight(36)
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setStyleSheet(STYLE_INPUT)
        cl.addWidget(self.input_pass)
        cl.addSpacing(8)

        self.chk_show = QCheckBox("Tampilkan Password")
        self.chk_show.setStyleSheet("""
            QCheckBox { color: #555555; font-size: 12px; background: transparent; border: none; }
            QCheckBox::indicator { width: 14px; height: 14px; }
        """)
        self.chk_show.stateChanged.connect(self.toggle_password)
        cl.addWidget(self.chk_show)
        cl.addSpacing(16)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_login = QPushButton("Login")
        self.btn_login.setFixedHeight(36)
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #22c55e; color: #ffffff;
                border: none; border-radius: 6px;
                padding: 0 22px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover   { background-color: #16a34a; }
            QPushButton:pressed { background-color: #15803d; }
        """)
        self.btn_login.clicked.connect(self.do_login)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setFixedHeight(36)
        self.btn_reset.setCursor(Qt.PointingHandCursor)
        self.btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #9ca3af; color: #ffffff;
                border: none; border-radius: 6px;
                padding: 0 22px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover   { background-color: #6b7280; }
            QPushButton:pressed { background-color: #4b5563; }
        """)
        self.btn_reset.clicked.connect(self.do_reset)

        btn_row.addWidget(self.btn_login)
        btn_row.addWidget(self.btn_reset)
        btn_row.addStretch()
        cl.addLayout(btn_row)
        cl.addSpacing(14)

        self.msg_frame = QFrame()
        self.msg_frame.setObjectName("msgFrame")
        self.msg_frame.setVisible(False)

        msg_layout = QVBoxLayout(self.msg_frame)
        msg_layout.setContentsMargins(12, 10, 12, 10)

        self.msg_label = QLabel()
        self.msg_label.setWordWrap(True)
        self.msg_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        msg_layout.addWidget(self.msg_label)

        cl.addWidget(self.msg_frame)

        root.addWidget(card)

        self.adjustSize()

    def toggle_password(self, state):
        mode = QLineEdit.Normal if state == 2 else QLineEdit.Password
        self.input_pass.setEchoMode(mode)

    def do_login(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text()

        if username == "admin" and password == "1234":
            self.input_user.setStyleSheet(STYLE_INPUT_GREEN)
            self.input_pass.setStyleSheet(STYLE_INPUT_GREEN)
            self.msg_frame.setStyleSheet("""
                QFrame#msgFrame {
                    background-color: #f0faf0;
                    border: 1.5px solid #72c472;
                    border-radius: 6px;
                }
            """)
            self.msg_label.setStyleSheet(
                "QLabel { color: #256025; font-size: 13px; background: transparent; border: none; }"
            )
            self.msg_label.setText(f"Login berhasil! Selamat datang, {username}.")
        else:
            self.input_user.setStyleSheet(STYLE_INPUT_RED)
            self.input_pass.setStyleSheet(STYLE_INPUT_RED)
            self.msg_frame.setStyleSheet("""
                QFrame#msgFrame {
                    background-color: #fff5f5;
                    border: 1.5px solid #e05555;
                    border-radius: 6px;
                }
            """)
            self.msg_label.setStyleSheet(
                "QLabel { color: #b91c1c; font-size: 13px; background: transparent; border: none; }"
            )
            self.msg_label.setText("Login gagal! Username atau password salah.")

        self.msg_frame.setVisible(True)
        self.adjustSize()

    def do_reset(self):
        self.input_user.clear()
        self.input_pass.clear()
        self.input_user.setStyleSheet(STYLE_INPUT)
        self.input_pass.setStyleSheet(STYLE_INPUT)
        self.chk_show.setChecked(False)
        self.msg_frame.setVisible(False)
        self.adjustSize()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()