class Product:
    def __init__(self, name, unit, unit_cost, unit_price, quantity):
        self.name=name
        self.unit=unit
        self.unit_cost = unit_cost
        self.unit_price = unit_price
        self.quantity = quantity
    def __repr__(self):
      return f"name={self.name}, unit = {self.unit}, unit_cost={self.unit_cost}, unit_price={self.unit_price}, quantity={self.quantity}"
    