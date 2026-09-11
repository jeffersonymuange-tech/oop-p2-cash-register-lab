#!/usr/bin/env python3


class CashRegister:
    '''Represents a cash register that tracks items, a running total,
    an optional discount, and a history of transactions.'''

    def __init__(self, discount=0):
        # discount is validated and stored via the property setter below
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        '''Discount must be an integer between 0 and 100 inclusive
        (percentage off the total). Falls back to 0 if invalid.'''
        if isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 100:
            self._discount = value
        else:
            print("Not valid discount")
            self._discount = 0

    def add_item(self, item, price, quantity=1):
        '''Adds `quantity` of `item` at `price` each to the register,
        updating the total, the items list, and transaction history.'''
        self.total += price * quantity
        self.items.extend([item] * quantity)
        self.previous_transactions.append({
            "item": item,
            "price": price,
            "quantity": quantity
        })

    def apply_discount(self):
        '''Applies the register's discount percentage to the current total.'''
        if self.discount == 0:
            print("There is no discount to apply.")
        else:
            self.total -= self.total * (self.discount / 100)
            print(f"After the discount, the total comes to ${self._format_price(self.total)}.")

    def void_last_transaction(self):
        '''Removes the most recently added transaction, subtracting its
        price from the total and removing its items from the items list.'''
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        last_transaction = self.previous_transactions.pop()
        price = last_transaction["price"]
        quantity = last_transaction["quantity"]

        self.total -= price * quantity
        if quantity > 0:
            self.items = self.items[:-quantity]

    @staticmethod
    def _format_price(value):
        '''Formats a numeric total, dropping a trailing ".0" for whole
        numbers (e.g. 800.0 -> "800") while keeping decimals otherwise.'''
        if value == int(value):
            return str(int(value))
        return str(value)