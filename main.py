from inventory.inventory import Inventory
from inventory.product import Electronics, Grocery, Clothing
from pathlib import Path
import os
from datetime import datetime

def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    Path("data").mkdir(exist_ok=True)

def get_float_input(prompt: str) -> float:
    """Handle numeric input with commas"""
    while True:
        try:
            value = input(prompt).replace(',', '')
            return float(value)
        except ValueError:
            print("Error: Please enter a valid number (e.g., 80000 or 80,000)")

def display_menu():
    print("\nInventory Management System")
    print("1. Add Product")
    print("2. Sell Product")
    print("3. Restock Product")
    print("4. Search Products by Name")
    print("5. List Products by Type")
    print("6. List All Products")
    print("7. Remove Expired Groceries")
    print("8. Save Inventory to File")
    print("9. Load Inventory from File")
    print("10. Show Total Inventory Value")
    print("0. Exit")

def get_product_details():
    product_types = {
        "1": "Electronics",
        "2": "Grocery",
        "3": "Clothing"
    }
    
    print("\nSelect product type:")
    for num, ptype in product_types.items():
        print(f"{num}. {ptype}")
    
    while True:
        choice = input("Enter choice (1-3): ")
        if choice in product_types:
            break
        print("Invalid choice. Please try again.")
    
    common_details = {
        "product_id": input("Enter product ID: ").strip(),
        "name": input("Enter product name: ").strip(),
        "price": get_float_input("Enter price: "),
        "quantity_in_stock": int(input("Enter initial stock quantity: "))
    }
    
    if choice == "1":  # Electronics
        extra_details = {
            "warranty_years": int(input("Enter warranty years: ")),
            "brand": input("Enter brand: ").strip()
        }
        return Electronics(**common_details, **extra_details)
    elif choice == "2":  # Grocery
        while True:
            expiry_date = input("Enter expiry date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(expiry_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        extra_details = {"expiry_date": expiry_date}
        return Grocery(**common_details, **extra_details)
    elif choice == "3":  # Clothing
        extra_details = {
            "size": input("Enter size: ").strip(),
            "material": input("Enter material: ").strip()
        }
        return Clothing(**common_details, **extra_details)

def main():
    ensure_data_directory()
    inventory = Inventory.load_from_file()  # Try to load existing data
    
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        
        try:
            if choice == "1":  # Add Product
                product = get_product_details()
                inventory.add_product(product)
                print(f"Product {product.name} added successfully!")
            
            elif choice == "2":  # Sell Product
                product_id = input("Enter product ID to sell: ").strip()
                quantity = int(input("Enter quantity to sell: "))
                inventory.sell_product(product_id, quantity)
                print(f"Sold {quantity} units of product {product_id}")
            
            elif choice == "3":  # Restock Product
                product_id = input("Enter product ID to restock: ").strip()
                quantity = int(input("Enter quantity to restock: "))
                inventory.restock_product(product_id, quantity)
                print(f"Restocked {quantity} units to product {product_id}")
            
            elif choice == "4":  # Search by Name
                name = input("Enter product name to search: ").strip()
                products = inventory.search_by_name(name)
                print("\nFound Products:")
                for product in products:
                    print(product)
                print(f"Total found: {len(products)}")
            
            elif choice == "5":  # List by Type
                print("\n1. Electronics\n2. Grocery\n3. Clothing")
                type_choice = input("Enter type to list: ").strip()
                if type_choice == "1":
                    products = inventory.search_by_type(Electronics)
                elif type_choice == "2":
                    products = inventory.search_by_type(Grocery)
                elif type_choice == "3":
                    products = inventory.search_by_type(Clothing)
                else:
                    print("Invalid choice")
                    continue
                
                print("\nProducts:")
                for product in products:
                    print(product)
                print(f"Total found: {len(products)}")
            
            elif choice == "6":  # List All Products
                products = inventory.list_all_products()
                print("\nAll Products:")
                for product in products:
                    print(product)
                print(f"Total products: {len(products)}")
            
            elif choice == "7":  # Remove Expired Groceries
                count = inventory.remove_expired_products()
                print(f"Removed {count} expired grocery items")
            
            elif choice == "8":  # Save to File
                filename = input("Enter filename (default: data/inventory.json): ").strip() or "data/inventory.json"
                if inventory.save_to_file(filename):
                    print(f"Inventory saved to {filename}")
                else:
                    print("Failed to save inventory")
            
            elif choice == "9":  # Load from File
                filename = input("Enter filename (default: data/inventory.json): ").strip() or "data/inventory.json"
                inventory = Inventory.load_from_file(filename)
                print(f"Inventory loaded from {filename}")
            
            elif choice == "10":  # Total Inventory Value
                total = inventory.total_inventory_value()
                print(f"Total inventory value: ${total:,.2f}")
            
            elif choice == "0":  # Exit
                # Save before exiting
                inventory.save_to_file("data/inventory.json")
                print("Exiting program...")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except ValueError as e:
            print(f"Input error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()