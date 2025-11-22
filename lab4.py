class Restaurant:
    def __init__(self, name):
        """Initialize restaurant with a name, empty menu prices, and empty orders."""
        self.name = name
        self.menu_prices = {} 
        self.orders = {}       

    def set_price(self, item_name, price):
        """Add or update the price of a menu item."""
        self.menu_prices[item_name] = price

    def add_order(self, order_id, customer_name):
        """Create a new order with the given ID and customer name."""
        if order_id not in self.orders:
            self.orders[order_id] = (customer_name, {})

    def add_item_to_order(self, order_id, item_name, quantity):
        """Add or increase the quantity of an item in an existing order."""
        if order_id in self.orders:
            customer_name, items_dict = self.orders[order_id]
            if item_name in items_dict:
                items_dict[item_name] += quantity
            else:
                items_dict[item_name] = quantity
            self.orders[order_id] = (customer_name, items_dict)

    def update_item_quantity(self, order_id, item_name, quantity):
        """Update the quantity of an item in an order. Remove if quantity <= 0."""
        if order_id in self.orders:
            customer_name, items_dict = self.orders[order_id]
            if quantity <= 0:
                items_dict.pop(item_name, None)
            else:
                items_dict[item_name] = quantity
            self.orders[order_id] = (customer_name, items_dict)

    def remove_order(self, order_id):
        """Remove an order completely if it exists."""
        self.orders.pop(order_id, None)

    def list_orders(self):
        """Return a list of (order_id, customer_name) tuples for all active orders."""
        return [(order_id, data[0]) for order_id, data in self.orders.items()]

    def list_order_items(self, order_id):
        """Return a list of (item_name, quantity) tuples for all items in a given order."""
        if order_id in self.orders:
            _, items_dict = self.orders[order_id]
            return list(items_dict.items())
        return []

    def calculate_order_total(self, order_id):
        """Calculate and return the total cost of an order."""
        total = 0.0
        if order_id in self.orders:
            _, items_dict = self.orders[order_id]
            for item, qty in items_dict.items():
                price = self.menu_prices.get(item, 0.0)
                total += price * qty
        return total



if __name__ == "__main__":

    my_restaurant = Restaurant("Burger Palace")

 
    my_restaurant.set_price("burger", 3.99)
    my_restaurant.set_price("fries", 2.99)
    my_restaurant.set_price("soda", 1.99)
    my_restaurant.set_price("salad", 4.99)


    my_restaurant.add_order(101, "Sabrina Carpenter")
    my_restaurant.add_order(102, "Saja Boys")


    my_restaurant.add_item_to_order(101, "burger", 2)
    my_restaurant.add_item_to_order(101, "soda", 1)

    my_restaurant.add_item_to_order(102, "fries", 3)
    my_restaurant.add_item_to_order(102, "salad", 2)


    my_restaurant.update_item_quantity(101, "soda", 2)
    my_restaurant.update_item_quantity(102, "salad", 1)

 
    print("Active Orders:")
    for order in my_restaurant.list_orders():
        print(order)


    print("\nItems in Order 101:")
    for item in my_restaurant.list_order_items(101):
        print(item)

  
    total_101 = my_restaurant.calculate_order_total(101)
    print(f"\nTotal cost of Order 101: ${total_101:.2f}")

    my_restaurant.remove_order(102)

    print("\nUpdated Active Orders:")
    for order in my_restaurant.list_orders():
        print(order)
