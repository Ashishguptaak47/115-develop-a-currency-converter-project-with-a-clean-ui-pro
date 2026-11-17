import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, 
    QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

API_URL = "https://api.exchangerate-api.com/v4/latest/"

class CurrencyService:
    @staticmethod
    :
        try:
            response = requests.get(f"{API_URL}{base_currency}", timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("rates", {})
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch exchange rates: {e}")

class CurrencyConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Converter")
        self.setFixedSize(400, 250)
        self.rates = {}
        self.init_ui()
        self.load_currencies()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Amount input
        amount_layout = QHBoxLayout()
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setText("1.0")
        amount_layout.addWidget(QLabel("Amount:"))
        amount_layout.addWidget(self.amount_input)
        main_layout.addLayout(amount_layout)

        # From Currency
        from_layout = QHBoxLayout()
        self.from_combo = QComboBox()
        self.from_combo.currentTextChanged.connect(self.update_rates)
        from_layout.addWidget(QLabel("From:"))
        from_layout.addWidget(self.from_combo)
        main_layout.addLayout(from_layout)

        # To Currency
        to_layout = QHBoxLayout()
        self.to_combo = QComboBox()
        to_layout.addWidget(QLabel("To:"))
        to_layout.addWidget(self.to_combo)
        main_layout.addLayout(to_layout)

        # Convert Button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert_currency)
        main_layout.addWidget(self.convert_btn)

        # Result Label
        self.result_label = QLabel("Converted Amount: --")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        main_layout.addWidget(self.result_label)

    def load_currencies(self):
        try:
            self.rates = CurrencyService.get_rates("USD")
            currencies = sorted(list(self.rates.keys()))
            self.from_combo.addItems(currencies)
            self.to_combo.addItems(currencies)
            self.from_combo.setCurrentText("USD")
            self.to_combo.setCurrentText("EUR")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_rates(self, base_currency):
        try:
            self.rates = CurrencyService.get_rates(base_currency)
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))

    def convert_currency(self):
        try:
            amount_text = self.amount_input.text().strip()
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid numeric amount.")
            return

        to_currency = self.to_combo.currentText()
        rate = self.rates.get(to_currency)

        if rate is not None:
            result = amount * rate
            self.result_label.setText(f"{amount:.2f} {self.from_combo.currentText()} = {result:.2f} {to_currency}")
        else:
            QMessageBox.warning(self, "Error", "Selected currency rate is unavailable.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverterApp()
    window.show()
    sys.exit(app.exec_())
