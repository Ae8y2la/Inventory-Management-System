class InventoryError(Exception):
    """Base class for inventory-related exceptions"""
    pass

class InsufficientStockError(InventoryError):
    def __init__(self, available: int, requested: int):
        super().__init__(f"Insufficient stock. Available: {available}, Requested: {requested}")
        self.available = available
        self.requested = requested

class DuplicateProductError(InventoryError):
    def __init__(self, product_id: str):
        super().__init__(f"Product with ID {product_id} already exists in inventory")

class InvalidProductDataError(InventoryError):
    def __init__(self, message: str):
        super().__init__(f"Invalid product data: {message}")