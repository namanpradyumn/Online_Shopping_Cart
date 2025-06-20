# Product Class
class Product:
    def __init__(self, product_id, name, price, quantity_available):
        if price < 0:
            raise ValueError("Price must be non-negative.")
        if quantity_available < 0:
            raise ValueError("Quantity must be non-negative.")
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_available = quantity_available

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def quantity_available(self):
        return self._quantity_available

    @quantity_available.setter
    def quantity_available(self, value):
        if value >= 0:
            self._quantity_available = value

    def decrease_quantity(self, amount):
        if amount <= self._quantity_available:
            self._quantity_available -= amount
            return True
        return False

    def increase_quantity(self, amount):
        self._quantity_available += amount

    def display_details(self):
        return f"ID: {self._product_id}, Name: {self._name}, Price: ₹{self._price:.2f}, Stock: {self._quantity_available}"

# CartItem Class
class CartItem:
    def __init__(self, product, quantity):
        self._product = product
        self._quantity = quantity

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value >= 0:
            self._quantity = value

    def calculate_subtotal(self):
        return self._product.price * self._quantity

    def __str__(self):
        return f"{self._product.name} x {self._quantity} = ₹{self.calculate_subtotal():.2f}"

# ShoppingCart Class
class ShoppingCart:
    def __init__(self):
        self._catalog = {}
        self._items = {}

    def display_products(self):
        if not self._catalog:
            print("No products available.")
            return
        print("\nAvailable Products:")
        for product in self._catalog.values():
            print(product.display_details())

    def input_positive_integer(self, prompt):
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
                return None
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

    def add_new_product(self):
        pid = input("Enter Product ID: ").strip()
        if not pid:
            print("Product ID cannot be empty.")
            return
        name = input("Enter Product Name: ").strip()
        if not name:
            print("Product name cannot be empty.")
            return
        try:
            price = float(input("Enter Price: "))
            quantity = int(input("Enter Quantity: "))
            if price < 0 or quantity < 0:
                raise ValueError
        except ValueError:
            print("Invalid price or quantity.")
            return
        try:
            self._catalog[pid] = Product(pid, name, price, quantity)
            print("Product added successfully.")
        except ValueError as e:
            print(e)

    def add_item(self, product_id, quantity):
        if product_id in self._catalog:
            product = self._catalog[product_id]
            if quantity > product.quantity_available:
                print(f"Only {product.quantity_available} units available.")
                return False
            if product.decrease_quantity(quantity):
                if product_id in self._items:
                    self._items[product_id].quantity += quantity
                else:
                    self._items[product_id] = CartItem(product, quantity)
                print("Item added to cart.")
                return True
        print("Invalid product ID or insufficient stock.")
        return False

    def remove_item(self, product_id):
        if product_id in self._items:
            confirm = input(f"Are you sure you want to remove {product_id}? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                return False
            item = self._items.pop(product_id)
            item.product.increase_quantity(item.quantity)
            print("Item removed from cart.")
            return True
        print("Item not found in cart.")
        return False

    def update_quantity(self, product_id, new_quantity):
        if product_id in self._items:
            item = self._items[product_id]
            diff = new_quantity - item.quantity
            if diff > 0:
                if item.product.quantity_available >= diff:
                    item.product.decrease_quantity(diff)
                    item.quantity = new_quantity
                    print("Quantity updated.")
                    return True
                else:
                    print(f"Only {item.product.quantity_available} additional items available.")
                    return False
            else:
                item.product.increase_quantity(-diff)
                item.quantity = new_quantity
                print("Quantity updated.")
                return True
        print("Item not found in cart.")
        return False

    def search_product_by_name(self, keyword):
        matches = [p for p in self._catalog.values() if keyword.lower() in p.name.lower()]
        if not matches:
            print("No matching products found.")
        else:
            print("Search Results:")
            for p in matches:
                print(p.display_details())

    def display_cart(self):
        if not self._items:
            print("Cart is empty.")
            return
        print("\nYour Cart:")
        total = 0
        for item in self._items.values():
            print(item)
            total += item.calculate_subtotal()
        print(f"Grand Total: ₹{total:.2f}")

    def run(self):
        while True:
            print("""
====================
1. View Products
2. Add New Product
3. Add Item to Cart
4. View Cart
5. Update Quantity in Cart
6. Remove Item from Cart
7. Search Product
8. Checkout (Dummy)
9. Exit
====================""")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.display_products()
            elif choice == "2":
                self.add_new_product()
            elif choice == "3":
                pid = input("Enter Product ID: ").strip()
                qty = self.input_positive_integer("Enter Quantity: ")
                if qty is not None:
                    self.add_item(pid, qty)
            elif choice == "4":
                self.display_cart()
            elif choice == "5":
                pid = input("Enter Product ID: ").strip()
                qty = self.input_positive_integer("Enter New Quantity: ")
                if qty is not None:
                    self.update_quantity(pid, qty)
            elif choice == "6":
                pid = input("Enter Product ID to Remove: ").strip()
                self.remove_item(pid)
            elif choice == "7":
                keyword = input("Enter keyword to search product name: ")
                self.search_product_by_name(keyword)
            elif choice == "8":
                self.display_cart()
                print("Thank you for shopping with us! (Simulated Checkout)")
                self._items.clear()
            elif choice == "9":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please select between 1-9.")

# Entry Point
if __name__ == "__main__":
    try:
        cart = ShoppingCart()
        cart.run()
    except KeyboardInterrupt:
        print("\nExiting due to user interruption. Goodbye!")

