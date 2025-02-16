import csv
import os
import time

class Product:
    def __init__(self, name, price, type, stock):
        self.name = name
        self.price = price
        self.type = type
        self.stock = stock

class ProductManager:
    filename = "pccom.csv"
    header = ["name", "price", "type", "stock"]

    def __init__(self):
        self.init_file()

    def init_file(self):
        if not os.path.isfile(self.filename):
            with open(self.filename, "w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.header)
                writer.writeheader()

    def add_product(self, product):
        with open(self.filename, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header)
            writer.writerow(product.__dict__)

    def get_all_products(self):
        with open(self.filename, "r", newline="") as csv_file:
            if os.stat(self.filename).st_size == 0:
                return []
            return list(csv.DictReader(csv_file))

    def update_product(self, index, updated_product):
        products = self.get_all_products()
        products[index] = updated_product.__dict__
        self._write_all_products(products)

    def delete_product(self, index):
        products = self.get_all_products()
        del products[index]
        self._write_all_products(products)

    def delete_all_products(self):
        with open(self.filename, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header)
            writer.writeheader()

    def _write_all_products(self, products):
        with open(self.filename, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header)
            writer.writeheader()
            writer.writerows(products)

class Menu:
    def __init__(self):
        self.product_manager = ProductManager()

    def display_menu(self):
        while True:
            print("Bienvenido a PCCOM!")
            print("1. Afegir producte")
            print("2. Consultar producte")
            print("3. Actualizar producte")
            print("4. Borrar producte")
            print("5. Mostrar productes")
            print("6. Calcular venta total")
            print("7. Calcular venta per producte")
            print("9. Tipo de producte")
            print("10. Actualizar stock de un producte")
            print("11. Esborrar tots els productes")
            print("0. Sortir")
            option = input("Selecciona una opció: ")

            if option == "0":
                print("Sortint...")
                time.sleep(2)
                break
            self.menu_option(option)

    def menu_option(self, option):
        os.system("cls" if os.name == "nt" else "clear")
        if option == "1":
            self.add_product()
        elif option == "2":
            self.view_product()
        elif option == "3":
            self.update_product()
        elif option == "4":
            self.delete_product()
        elif option == "5":
            self.show_products()
        elif option == "6":
            self.calculate_total_sale()
        elif option == "7":
            self.calculate_product_sale()
        elif option == "9":
            self.product_type()
        elif option == "10":
            self.update_stock()
        elif option == "11":
            self.delete_all_products()
        else:
            print("Opció no valida.")
        print("Tornant al menú...")
        time.sleep(2)

    def add_product(self):
        name = input("Introdueix el nom del producte: ")
        price = int(input("Introdueix el preu del producte, ej (45): "))
        type = input("Introdueix el tipus del producte, ej (keyboard,mouse): ")
        stock = int(input("Introdueix el stock del producte,ej (6): "))
        product = Product(name, price, type, stock)
        self.product_manager.add_product(product)

    def view_product(self):
        products = self.product_manager.get_all_products()
        self.render_csv_search_options(products)
        selected = int(input("Quin vols seleccionar? (Selecciona el número): "))
        selected_product = products[selected]
        print(f"Nom: {selected_product['name']}")
        print(f"Preu: {selected_product['price']}")
        print(f"Tipus: {selected_product['type']}")
        print(f"Stock: {selected_product['stock']}")
        print("\n\n")

    def render_csv_search_options(self, products):
        for index, row in enumerate(products):
            print(f"{index}: {row['name']}")

    def update_product(self):
        products = self.product_manager.get_all_products()
        if not products:
            print("No hi ha productes en l'inventari.")
            time.sleep(1)
            return
        self.render_csv_search_options(products)
        selected = int(input("¿Qué producto quieres modificar? (Selecciona el número): "))
        selected_product = products[selected]
        name = input(f"Introdueix el nou nom del producte ({selected_product['name']}): ") or selected_product['name']
        price = input(f"Introdueix el nou preu del producte ({selected_product['price']}): ") or selected_product['price']
        type = input(f"Introdueix el nou tipus del producte ({selected_product['type']}): ") or selected_product['type']
        stock = input(f"Introduce el nuevo stock del producte ({selected_product['stock']}): ") or selected_product['stock']
        updated_product = Product(name, price, type, stock)
        self.product_manager.update_product(selected, updated_product)
        print("Producte actualitzat amb éxito.\n")

    def delete_product(self):
        products = self.product_manager.get_all_products()
        self.render_csv_search_options(products)
        selected = int(input("Quin vols eliminar? (Selecciona el número): "))
        self.product_manager.delete_product(selected)
        print("Producte eliminat.\n")

    def show_products(self):
        products = self.product_manager.get_all_products()
        print(f"{'Producte':<20} {'Preu':<10} {'Tipus':<15} {'Stock'}")
        print("-" * 50)
        for row in products:
            print(f"{row['name']:<20} {row['price']:<10} {row['type']:<15} {row['stock']}")
        print("\n")

    def calculate_total_sale(self):
        total = 0
        products = self.product_manager.get_all_products()
        for row in products:
            total += float(row["price"]) * int(row["stock"])
        print(f"La venta total de tots els productes és: {total}€\n")

    def calculate_product_sale(self):
        products = self.product_manager.get_all_products()
        self.render_csv_search_options(products)
        selected = int(input("Selecciona el nombre del producte per calcular la venta: "))
        selected_product = products[selected]
        venta = float(selected_product["price"]) * int(selected_product["stock"])
        print(f"La venta total del producte {selected_product['name']} és: {venta}€\n")

    def update_stock(self):
        products = self.product_manager.get_all_products()
        if not products:
            print("No hi ha productes en l'inventari.")
            time.sleep(1)
            return
        self.render_csv_search_options(products)
        selected = int(input("Quin producte vols actualitzar el stock? (Selecciona el número): "))
        new_stock = int(input("Introdueix el nou stock: "))
        selected_product = products[selected]
        selected_product["stock"] = str(new_stock)
        updated_product = Product(selected_product["name"], selected_product["price"], selected_product["type"], selected_product["stock"])
        self.product_manager.update_product(selected, updated_product)
        print(f"Stock del producte '{selected_product['name']}' actualitzat a {new_stock}.\n")

    def product_type(self):
        products = self.product_manager.get_all_products()
        if not products:
            print("No hi ha productes en l'inventari. Tornant al menú...")
            time.sleep(1)
            return
        tipo = input("Introdueix el tipus de producte para ver tots los productes de aquest tipus: ")
        print(f"Tipus de producte'{tipo}':")
        found = False
        for row in products:
            if row["type"].lower() == tipo.lower():
                print(f"- {row['name']} (Precio: {row['price']}€, Stock: {row['stock']})")
                found = True
        if not found:
            print(f"No hi ha aquest tipus de producte '{tipo}'.")
        print("\n")

    def delete_all_products(self):
        confirm = input("Estàs segur que vols esborrar tots els productes? (si/no): ")
        if confirm.lower() == "si":
            self.product_manager.delete_all_products()
            print("Tots els productes han estat esborrats.")


menu = Menu()
menu.display_menu()
