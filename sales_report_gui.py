import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QTextEdit
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class SalesReportApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('database/sales_report.db/sales.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sales Report App')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.report_text = QTextEdit(self)
        layout.addWidget(self.report_text)

        self.btn_generate_pdf = QPushButton('Gerar PDF', self)
        self.btn_generate_pdf.clicked.connect(self.generate_pdf)
        layout.addWidget(self.btn_generate_pdf)

        self.btn_exit = QPushButton('Sair', self)
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit)

        self.load_reports()
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_reports(self):
        total_sales = self.get_total_sales()
        sales_by_product = self.get_sales_by_product()
        quantity_sold = self.get_quantity_sold()
        sales_by_date = self.get_sales_by_date()

        report = f"Total de Vendas: R${total_sales:.2f}\n\n"
        report += "Vendas por Produto:\n" + "\n".join(sales_by_product) + "\n\n"
        report += "Quantidade Vendida por Produto:\n" + "\n".join(quantity_sold) + "\n\n"
        report += "Vendas por Data:\n" + "\n".join(sales_by_date) + "\n"
        
        self.report_text.setPlainText(report)

    def get_total_sales(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(total_price) FROM Sales")
        total_sales = cursor.fetchone()[0]
        return total_sales if total_sales is not None else 0

    def get_sales_by_product(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT product_name, SUM(total_price) FROM Sales GROUP BY product_name")
        sales = cursor.fetchall()
        return [f"Produto: {name}, Total: R${total:.2f}" for name, total in sales]

    def get_quantity_sold(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT product_name, SUM(quantity) FROM Sales GROUP BY product_name")
        quantities = cursor.fetchall()
        return [f"Produto: {name}, Quantidade: {quantity}" for name, quantity in quantities]

    def get_sales_by_date(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT sale_date, SUM(total_price) FROM Sales GROUP BY sale_date")
        sales = cursor.fetchall()
        return [f"Data: {date}, Total: R${total:.2f}" for date, total in sales]

    def generate_pdf(self):
        filename = 'sales_report.pdf'
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        margin = 50 

        c.drawString(margin, height - margin, "Relatório de Vendas")

        text = self.report_text.toPlainText().split('\n')
        y_position = height - margin - 20 

        for line in text:
            c.drawString(margin, y_position, line)
            y_position -= 15 
            if y_position < margin: 
                c.showPage() 
                y_position = height - margin - 20 

        c.save()
        print(f"PDF gerado: {filename}")

    def closeEvent(self, event):
        self.conn.close() 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SalesReportApp()
    ex.show()
    sys.exit(app.exec_())
