from abc import ABC, abstractmethod
from datetime import datetime, date
from .exceptions import InsufficientStockError

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock
    
    @property
    def product_id(self):
        return self._product_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            raise ValueError("Price must be positive")
        self._price = new_price
    
    @property
    def quantity_in_stock(self):
        return self._quantity_in_stock
    
    def restock(self, amount: int):
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        self._quantity_in_stock += amount
    
    def sell(self, quantity: int):
        if quantity <= 0:
            raise ValueError("Sale quantity must be positive")
        if quantity > self._quantity_in_stock:
            raise InsufficientStockError(self._quantity_in_stock, quantity)
        self._quantity_in_stock -= quantity
    
    def get_total_value(self):
        return self._price * self._quantity_in_stock
    
    @abstractmethod
    def __str__(self):
        return f"ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}, Stock: {self._quantity_in_stock}"
    
    @abstractmethod
    def to_dict(self):
        """Convert product to dictionary for serialization"""
        return {
            "type": self.__class__.__name__,
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock
        }

class Electronics(Product):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, warranty_years: int, brand: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._warranty_years = warranty_years
        self._brand = brand
    
    @property
    def warranty_years(self):
        return self._warranty_years
    
    @property
    def brand(self):
        return self._brand
    
    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}, Type: Electronics, Brand: {self._brand}, Warranty: {self._warranty_years} years"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "warranty_years": self._warranty_years,
            "brand": self._brand
        })
        return data

class Grocery(Product):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, expiry_date: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._expiry_date = expiry_date
    
    @property
    def expiry_date(self):
        return self._expiry_date
    
    def is_expired(self):
        expiry = datetime.strptime(self._expiry_date, "%Y-%m-%d").date()
        return expiry < date.today()
    
    def __str__(self):
        base_info = super().__str__()
        expired = " (Expired)" if self.is_expired() else ""
        return f"{base_info}, Type: Grocery, Expiry Date: {self._expiry_date}{expired}"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "expiry_date": self._expiry_date
        })
        return data

class Clothing(Product):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, size: str, material: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._size = size
        self._material = material
    
    @property
    def size(self):
        return self._size
    
    @property
    def material(self):
        return self._material
    
    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}, Type: Clothing, Size: {self._size}, Material: {self._material}"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "size": self._size,
            "material": self._material
        })
        return data