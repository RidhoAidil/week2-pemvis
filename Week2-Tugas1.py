import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen

STYLE_WHITE = """
    QLineEdit {
        border: 1px solid #d0d0d0;
        border-radius: 6px;
        padding: 9px 14px;
        background-color: #ffffff;
        color: #222222;
        font-size: 13px;
    }
    QLineEdit:focus { border: 1.5px solid #999999; }
"""
STYLE_RED = """
    QLineEdit {
        border: 1.5px solid #e05555;
        border-radius: 6px;
        padding: 9px 14px;
        background-color: #fff5f5;
        color: #222222;
        font-size: 13px;
    }
"""
STYLE_GREEN = """
    QLineEdit {
        border: 1.5px solid #72c472;
        border-radius: 6px;
        padding: 9px 14px;
        background-color: #f4fbf4;
        color: #222222;
        font-size: 13px;
    }
"""
COMBO_STYLE = """
    QComboBox {
        border: 1px solid #d0d0d0;
        border-radius: 6px;
        padding: 9px 14px;
        background-color: #ffffff;
        color: #444444;
        font-size: 13px;
    }
    QComboBox:focus { border: 1.5px solid #999999; }
    QComboBox::drop-down { width: 0px; border: none; }
    QComboBox::down-arrow { width: 0px; height: 0px; image: none; }
    QComboBox QAbstractItemView {
        border: 1px solid #cccccc;
        background-color: #ffffff;
        selection-background-color: #e8f0fe;
        color: #222222;
        font-size: 13px;
    }
"""
LABEL_STYLE   = "QLabel { color: #555555; font-size: 13px; font-weight: 500; background: transparent; border: none; }"
RES_KEY_STYLE = "QLabel { color: #256025; font-size: 13px; font-weight: 600; background: transparent; border: none; min-width: 100px; }"
RES_VAL_STYLE = "QLabel { color: #2e6e2e; font-size: 13px; background: transparent; border: none; }"


class ComboWithArrow(QComboBox):
    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        ax, ay = self.width() - 20, self.height() // 2
        pen = QPen(QColor("#777777"))
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.drawLine(ax - 5, ay - 2, ax, ay + 3)
        p.drawLine(ax, ay + 3, ax + 5, ay - 2)
        p.end()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Form Biodata Mahasiswa")
        self.setMinimumWidth(520)
        self.setStyleSheet("QWidget { background-color: #eef0f3; font-family: 'Segoe UI', Arial, sans-serif; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(0)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e4e8;
            }
        """)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        cl = QVBoxLayout(card)
        cl.setContentsMargins(32, 28, 32, 28)
        cl.setSpacing(0)

        title = QLabel("Form Biodata Mahasiswa")
        title.setStyleSheet("""
            QLabel {
                color: #1a1a2e;
                font-size: 16px;
                font-weight: 700;
                background: transparent;
                border: none;
                padding-bottom: 4px;
            }
        """)
        cl.addWidget(title)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFixedHeight(1)
        divider.setStyleSheet("QFrame { background-color: #e8eaed; border: none; }")
        cl.addWidget(divider)
        cl.addSpacing(20)

        def add_field(label_text, widget, gap=16):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(LABEL_STYLE)
            cl.addWidget(lbl)
            cl.addSpacing(5)
            cl.addWidget(widget)
            cl.addSpacing(gap)

        self.input_nama = QLineEdit()
        self.input_nama.setFixedHeight(38)
        self.input_nama.setStyleSheet(STYLE_WHITE)
        self.input_nama.textChanged.connect(lambda: self.update_field_style(self.input_nama))
        add_field("Nama Lengkap", self.input_nama)

        self.input_nim = QLineEdit()
        self.input_nim.setFixedHeight(38)
        self.input_nim.setPlaceholderText("Masukkan NIM")
        self.input_nim.setStyleSheet(STYLE_WHITE)
        self.input_nim.textChanged.connect(lambda: self.update_field_style(self.input_nim))
        add_field("NIM", self.input_nim)

        self.input_kelas = QLineEdit()
        self.input_kelas.setFixedHeight(38)
        self.input_kelas.setPlaceholderText("Contoh: TI-2A")
        self.input_kelas.setStyleSheet(STYLE_WHITE)
        self.input_kelas.textChanged.connect(lambda: self.update_field_style(self.input_kelas))
        add_field("Kelas", self.input_kelas)

        self.combo_jk = ComboWithArrow()
        self.combo_jk.addItems(["Laki-laki", "Perempuan"])
        self.combo_jk.setFixedHeight(38)
        self.combo_jk.setStyleSheet(COMBO_STYLE)
        add_field("Jenis Kelamin", self.combo_jk, gap=24)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_tampilkan = QPushButton("Tampilkan")
        self.btn_tampilkan.setFixedHeight(38)
        self.btn_tampilkan.setMinimumWidth(110)
        self.btn_tampilkan.setCursor(Qt.PointingHandCursor)
        self.btn_tampilkan.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; color: #ffffff;
                border: none; border-radius: 7px;
                font-size: 13px; font-weight: 600;
            }
            QPushButton:hover   { background-color: #2563eb; }
            QPushButton:pressed { background-color: #1d4ed8; }
        """)
        self.btn_tampilkan.clicked.connect(self.tampilkan_data)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setFixedHeight(38)
        self.btn_reset.setMinimumWidth(90)
        self.btn_reset.setCursor(Qt.PointingHandCursor)
        self.btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #f1f3f5; color: #555555;
                border: 1px solid #d0d0d0; border-radius: 7px;
                font-size: 13px; font-weight: 600;
            }
            QPushButton:hover   { background-color: #e2e6ea; }
            QPushButton:pressed { background-color: #ced4da; }
        """)
        self.btn_reset.clicked.connect(self.reset_form)

        btn_row.addWidget(self.btn_tampilkan)
        btn_row.addWidget(self.btn_reset)
        btn_row.addStretch()
        cl.addLayout(btn_row)
        cl.addSpacing(20)

        self.result_frame = QFrame()
        self.result_frame.setObjectName("resultFrame")
        self.result_frame.setStyleSheet("""
            QFrame#resultFrame {
                background-color: #f6fdf6;
                border: 1px solid #86c986;
                border-radius: 8px;
            }
        """)
        self.result_frame.setVisible(False)

        rl = QVBoxLayout(self.result_frame)
        rl.setContentsMargins(18, 14, 18, 16)
        rl.setSpacing(8)

        res_title = QLabel("DATA BIODATA")
        res_title.setStyleSheet("""
            QLabel {
                font-weight: 700;
                font-size: 12px;
                color: #3a7a3a;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }
        """)
        rl.addWidget(res_title)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("QFrame { background-color: #c8e6c9; border: none; }")
        rl.addWidget(sep)

        grid = QGridLayout()
        grid.setContentsMargins(0, 4, 0, 0)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)
        grid.setColumnMinimumWidth(0, 110)
        grid.setColumnMinimumWidth(1, 12)
        grid.setColumnStretch(2, 1)

        self.val_labels = {}
        for i, (key, attr) in enumerate(zip(
            ["Nama", "NIM", "Kelas", "Jenis Kelamin"],
            ["nama", "nim", "kelas", "jk"]
        )):
            k = QLabel(key)
            k.setStyleSheet(RES_KEY_STYLE)
            k.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            colon = QLabel(":")
            colon.setStyleSheet(RES_KEY_STYLE)
            colon.setAlignment(Qt.AlignCenter)

            v = QLabel()
            v.setStyleSheet(RES_VAL_STYLE)
            v.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            v.setWordWrap(True)

            grid.addWidget(k,     i, 0)
            grid.addWidget(colon, i, 1)
            grid.addWidget(v,     i, 2)
            self.val_labels[attr] = v

        rl.addLayout(grid)
        cl.addWidget(self.result_frame)

        root.addWidget(card)
        self.adjustSize()

    def update_field_style(self, field):
        if field.text().strip():
            field.setStyleSheet(STYLE_GREEN)
        else:
            field.setStyleSheet(STYLE_RED if self.submitted else STYLE_WHITE)

    def tampilkan_data(self):
        self.submitted = True
        for f in [self.input_nama, self.input_nim, self.input_kelas]:
            self.update_field_style(f)

        nama   = self.input_nama.text().strip()
        nim    = self.input_nim.text().strip()
        kelas  = self.input_kelas.text().strip()
        jk_idx = self.combo_jk.currentIndex()

        if not nama or not nim or not kelas or jk_idx == 0:
            self.result_frame.setVisible(False)
            self.adjustSize()
            return

        self.val_labels["nama"].setText(nama)
        self.val_labels["nim"].setText(nim)
        self.val_labels["kelas"].setText(kelas)
        self.val_labels["jk"].setText(self.combo_jk.currentText())
        self.result_frame.setVisible(True)
        self.adjustSize()

    def reset_form(self):
        self.submitted = False
        self.input_nama.clear()
        self.input_nim.clear()
        self.input_kelas.clear()
        self.combo_jk.setCurrentIndex(0)
        for f in [self.input_nama, self.input_nim, self.input_kelas]:
            f.setStyleSheet(STYLE_WHITE)
        self.result_frame.setVisible(False)
        self.adjustSize()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()