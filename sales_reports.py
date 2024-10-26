import sqlite3

conn = sqlite3.connect('database/sales_report.db/sales.db')
cursor = conn.cursor()

def report_total_sales():
    cursor.execute("SELECT SUM(total_price) FROM Sales")
    total_sales = cursor.fetchone()[0]
    print(f'Total de Vendas: R${total_sales:.2f}')

def report_sales_by_product():
    cursor.execute("SELECT product_name, SUM(total_price) FROM Sales GROUP BY product_name")
    results = cursor.fetchall()
    print("Vendas por Produto:")
    for row in results:
        print(f'Produto: {row[0]}, Total: R${row[1]:.2f}')

def report_sales_quantity():
    cursor.execute("SELECT product_name, SUM(quantity) FROM Sales GROUP BY product_name")
    results = cursor.fetchall()
    print("Quantidade Vendida por Produto:")
    for row in results:
        print(f'Produto: {row[0]}, Quantidade: {row[1]}')

def report_sales_by_date():
    cursor.execute("SELECT sale_date, SUM(total_price) FROM Sales GROUP BY sale_date")
    results = cursor.fetchall()
    print("Vendas por Data:")
    for row in results:
        print(f'Data: {row[0]}, Total: R${row[1]:.2f}')

if __name__ == '__main__':
    report_total_sales()
    report_sales_by_product()
    report_sales_quantity()
    report_sales_by_date()
    
    conn.close()
