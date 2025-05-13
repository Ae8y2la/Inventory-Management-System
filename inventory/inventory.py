import json
from pathlib import Path
from datetime import datetime, date
from .product import Electronics, Grocery, Clothing
from .exceptions import InventoryError, InsufficientStockError, DuplicateProductError, InvalidProductDataError

class Inventory:
    def __init__(self):
        self._products = {}
    
    def add_product(self, product):
        if product.product_id in self._products:
            raise DuplicateProductError(product.product_id)
        self._products[product.product_id] = product
    
    def remove_product(self, product_id: str):
        if product_id not in self._products:
            raise KeyError(f"Product with ID {product_id} not found")
        del self._products[product_id]
    
    def search_by_name(self, name: str):
        return [product for product in self._products.values() if name.lower() in product.name.lower()]
    
    def search_by_type(self, product_type: type):
        return [product for product in self._products.values() if isinstance(product, product_type)]
    
    def list_all_products(self):
        return list(self._products.values())
    
    def sell_product(self, product_id: str, quantity: int):
        if product_id not in self._products:
            raise KeyError(f"Product with ID {product_id} not found")
        self._products[product_id].sell(quantity)
    
    def restock_product(self, product_id: str, quantity: int):
        if product_id not in self._products:
            raise KeyError(f"Product with ID {product_id} not found")
        self._products[product_id].restock(quantity)
    
    def total_inventory_value(self):
        return sum(product.get_total_value() for product in self._products.values())
    
    def remove_expired_products(self):
        expired_ids = [
            product_id for product_id, product in self._products.items() 
            if isinstance(product, Grocery) and product.is_expired()
        ]
        for product_id in expired_ids:
            del self._products[product_id]
        return len(expired_ids)
    
    def save_to_file(self, filename: str = "data/inventory.json"):
        """Save inventory to JSON file with automatic directory creation"""
        try:
            # Ensure directory exists
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "products": [product.to_dict() for product in self._products.values()]
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            
            return True
        except Exception as e:
            raise InventoryError(f"Failed to save inventory: {str(e)}")
    
    @classmethod
    def load_from_file(cls, filename: str = "data/inventory.json"):
        """Load inventory from JSON file with error handling"""
        inventory = cls()
        
        try:
            # Check if file exists first
            if not Path(filename).exists():
                return inventory
                
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for product_data in data.get("products", []):
                product_type = product_data.pop("type")
                
                try:
                    if product_type == "Electronics":
                        product = Electronics(**product_data)
                    elif product_type == "Grocery":
                        product = Grocery(**product_data)
                    elif product_type == "Clothing":
                        product = Clothing(**product_data)
                    else:
                        raise InvalidProductDataError(f"Unknown product type: {product_type}")
                    
                    inventory.add_product(product)
                except TypeError as e:
                    raise InvalidProductDataError(f"Missing required field: {str(e)}")
                except ValueError as e:
                    raise InvalidProductDataError(str(e))
            
        except json.JSONDecodeError:
            raise InvalidProductDataError("Invalid JSON format in inventory file")
        except Exception as e:
            raise InventoryError(f"Failed to load inventory: {str(e)}")
        
        return inventory