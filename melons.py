"""Classes for melon orders."""
import random

import datetime


class TooManyMelonsError(ValueError):
    """More than 100 melons is bad!!"""
     def __init__(self):
         super(TooManyMelonsError, self).__init__("No more than 100 melons!")


class AbstractMelonOrder(object):
    """An abstract base class that other Melon Orders inherit from."""
    def __init__(self, species, qty, order_type, tax):
        self.species = species

        if qty > 100:
            raise TooManyMelonsError()
        self.qty = qty
      
        self.shipped = False
        self.order_type = order_type
        self.tax = tax

    def get_total(self):
        """Calculate price, including tax."""
        base_price = self.get_base_price()

        total = (1 + self.tax) * self.qty * base_price

        return total

    def get_base_price(self):
        """ Calculates base price based on rush hour"""
        base_price = random.randint(5, 9)

        if (datetime.datetime.today().weekday() in range(0, 5)
                and datetime.datetime.today().hour in range(8, 13)):
            base_price += self.qty * 4

        if self.species == "Christmas":
            base_price = base_price * 1.5

        return base_price

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True

class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    def __init__(self, species, qty):
        """Initialize melon order attributes."""
        super(DomesticMelonOrder, self).__init__(species, qty, "domestic", 0.08)


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""
        super(InternationalMelonOrder, self).__init__(species, qty, "international", 0.17)
        self.country_code = country_code


    def get_total(self):
        """ Calculates international fee for oders less than 10 melons"""
        if self.qty > 10:
            return super(InternationalMelonOrder, self).get_total()
        else:
            return super(InternationalMelonOrder, self).get_total() + 3

    def get_country_code(self):
        """Return the country code."""

        return self.country_code

class GovernmentMelonOrder(AbstractMelonOrder):
    """No tax on government melons"""
    def __init__(self, species, qty):
        super(GovernmentMelonOrder, self).__init__(species, qty, "government", 0)
        self.passed_inspection = False

    def mark_inspection(self, passed):
        """Sets inspection passed state"""
        self.passed_inspection = passed
