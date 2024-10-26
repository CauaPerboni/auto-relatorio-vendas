import sqlite3
import schedule
import time
import keyboard 

def generate_reports():
    conn = sqlite3.connect('database/sales_report.db/sales.db')
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(total_price) FROM Sales")
    total_sales = cursor.fetchone()[0]

    cursor.execute("SELECT product_name, SUM(total_price) FROM Sales GROUP BY product_name")
    sales_by_product = cursor.fetchall()

    cursor.execute("SELECT product_name, SUM(quantity) FROM Sales GROUP BY product_name")
    quantity_sold_by_product = cursor.fetchall()

    cursor.execute("SELECT sale_date, SUM(total_price) FROM Sales GROUP BY sale_date")
    sales_by_date = cursor.fetchall()

    print(f"Total de Vendas: R${total_sales:.2f}")
    print("Vendas por Produto:")
    for product, total in sales_by_product:
        print(f"Produto: {product}, Total: R${total:.2f}")
    
    print("Quantidade Vendida por Produto:")
    for product, quantity in quantity_sold_by_product:
        print(f"Produto: {product}, Quantidade: {quantity}")

    print("Vendas por Data:")
    for date, total in sales_by_date:
        print(f"Data: {date}, Total: R${total:.2f}")

    conn.close()

schedule.every().day.at("10:00").do(generate_reports)

print("Pressione 'q' para encerrar a execução.")

while True:
    schedule.run_pending()
    time.sleep(1)
    if keyboard.is_pressed('q'):
        print("Encerrando a execução...")
        break 

print("Programa finalizado.")
