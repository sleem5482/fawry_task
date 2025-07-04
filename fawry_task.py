from datetime import datetime, timedelta

class Product:
    '''the products class contained name, price quantity,expired default value is true ,requires_shipping default value is false if you need or not and weighy default =0'''
    def __init__(self, name, price, quantity, expires=False, requires_shipping=False, weight=0):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.expires = expires
        self.expiry_date = datetime.now() + timedelta(days=30) if expires else None # work the count before call the object
        self.requires_shipping = requires_shipping
        self.weight = weight if requires_shipping else 0

class Customer:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

class Cart:
    def __init__(self):
        self.items = {}
    
    def add(self, product, quantity):
        if product.quantity < quantity:
            raise ValueError(f"Not enough stock for {product.name}")# if not found enough quantity in the product object
        if product.expires and product.expiry_date < datetime.now():
            raise ValueError(f"{product.name} has expired") # if the product can expire and it expired
        
        if product in self.items:
            self.items[product] += quantity # if find it increase the quantity 
        else:
            self.items[product] = quantity # esle add to items dectionary
    
    def remove(self, product, quantity=None):
        if product not in self.items: # if the product not in items return null
            return
        
        if quantity is None or quantity >= self.items[product]:
            del self.items[product] # delete all
        else:
            self.items[product] -= quantity # else give me the number of quantity which delete it 

class ShippingService:
    @staticmethod # this is decorator to this func
    def ship_items(items):
        print("\n Shipment notice ")
        total_weight = 0
        for item in items:
            print(f"{item['quantity']}x {item['name']}\t{item['weight']}g")
            total_weight += item['weight'] * item['quantity']
        print(f"Total package weight {total_weight/1000:.1f}kg")

def checkout(customer, cart):
    if not cart.items:
        raise ValueError("Cart is empty")
    
    subtotal = sum(product.price * quantity for product, quantity in cart.items.items()) # collect all price 
    shipping_fee = sum(10 for product in cart.items if product.requires_shipping) * 10  # 10 per shippable item
    total = subtotal + shipping_fee
    
    if customer.balance < total: # if no find more balance raise error
        raise ValueError("Insufficient balance")
    
    # Prepare shipping items
    shipping_items = []
    for product, quantity in cart.items.items(): # items() in python to create a tuple from the dictionary
        if product.requires_shipping:
            shipping_items.append({
                'name': product.name,
                'weight': product.weight,
                'quantity': quantity
            })
    
    if shipping_items:
        ShippingService.ship_items(shipping_items)
    
    # Print receipt
    print("\n Checkout receipt ")
    for product, quantity in cart.items.items():
        print(f"{quantity}x {product.name} \t{product.price * quantity}")
    print("---"*10)
    print(f"Subtotal \t{subtotal}")
    print(f"Shipping \t{shipping_fee}")
    print(f"Amount \t{total}")
    print(f"Remaining balance: {customer.balance - total}")
    
    # Update stock and customer balance
    for product, quantity in cart.items.items():
        product.quantity -= quantity
    customer.balance -= total # this is more from me
    

# Example usage
if __name__ == "__main__":
    # Create products
    cheese = Product("Cheese", 100, 10, expires=True, requires_shipping=True, weight=200)
    tv = Product("TV", 5000, 5, requires_shipping=True, weight=1000)
    phone = Product("Phone", 5000, 1000)
    
    # Create customer
    customer = Customer("Ahmed", 15000)
    
    # Create cart and add items
    cart = Cart()
    cart.add(cheese, 2)
    cart.add(tv, 1) # if this three error because no more efficient 3*5000 = 15000 all balace on me
    cart.add(phone, 1)
    
    # Checkout
    checkout(customer, cart)