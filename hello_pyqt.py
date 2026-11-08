import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Hello from PyQt6")
layout = QVBoxLayout(window)
label = QLabel("Hello, Kuromi Library!")
button = QPushButton("Click me ♡")
button.clicked.connect(lambda: label.setText("Button clicked! ✨"))
layout.addWidget(label)
layout.addWidget(button)
window.show()
sys.exit(app.exec())
