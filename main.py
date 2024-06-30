import traceback
from doctest import UnexpectedException
from typing import List

from bullet import Bullet, colors, utils


# class to store items
class PurchaseItem(object):
    def __init__(self, option):
        self.price = option.p
        self.name = str(option)

    # function to print name
    def __str__(self):
        return self.name

    # function to get price of item
    def get_price(self):
        return self.price
    
# function to calculate total amount of order
def get_total_order_amount(order: List[PurchaseItem]):
    if len(order) <= 0:
        raise TypeError("You need to order something before proceeding.")
    total_amount = 0
    # loop over th list and add total of the object to total_amount variable
    for i in order:
        total_amount += i.get_price()
    # return error if total amount is not a valide positive value.
    if total_amount <= 0:
        raise ValueError("Amount of the order must have valid price.")
    # return the total amount of the order
    return total_amount
    """
    The total cost of all the items ordered
    """

# function to calculate how much service charge will be applied 
def get_service_charge(order: List[PurchaseItem]):
    """
    For every Rs. 100, the service charge amount should increase by 1% of order amount, upto a max of 20%
    Eg:
        Order Amount = 80, Service Charge = 0
        Order Amount = 150, Service Charge = 1.5
        Order Amount = 800, Service Charge = 64
        Order Amount = 1500, Service Charge = 225
        Order Amount = 3000, Service Charge = 600
    """

    total_amount = 0
    service_charge = 0
    for i in order:
        total_amount += i.get_price()
    # calculate percentage of service charge on total_amount based on per 100 
    # service charge %
    service_charge_percent = total_amount / 100
    # check the charge percentage.
    if service_charge_percent > 20:
        service_charge_percent = 20
    if service_charge_percent < 1:
        service_charge_percent = 0
    # calculate total service charge
    service_charge = total_amount * service_charge_percent / 100
    return service_charge



class Option(object):
    def __init__(self, n=None, pu=None, p=None, d=None):
        self.p = p
        self.n = n
        self.pu = pu
        if d:
            self.n = d.get("name")
            self.p = d.get("price")
        if self.p == None:
            self.p = 0
        if self.n == None:
            raise AttributeError
        self.pu = self.pu if self.pu else "Rs."

    def __str__(self):
        return f"{str(self.n)} {str(self.pu) + ' ' + str(self.p) if self.p else ''}"

    def __len__(self):
        return len(self.__str__())


# ITEM'S and BEVERAGE'S
MCDONALDS_FOOD_OPTIONS = [
    Option(d={"name": "Veg Burger", "price": 115.00}),
    Option(d={"name": "Veg Wrap", "price": 130.00}),
    Option(d={"name": "Veg Happy Meal", "price": 215.00}),
    Option(d={"name": "Chicken Burger", "price": 175.00}),
    Option(d={"name": "Chicken Wrap", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]

MCDONALDS_BEVERAGES_OPTIONS = [
    Option(d={"name": "Sprite (M)", "price": 115.00}),
    Option(d={"name": "Sprite (L)", "price": 130.00}),
    Option(d={"name": "Mango Smoothie", "price": 215.00}),
    Option(d={"name": "Chocolate Smoothie", "price": 175.00}),
    Option(d={"name": "Chocolate Smoothie w/ Icecream", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]


def get_option_from_result(result, options):
    for option in options:
        if str(option) == result:
            return option
    raise UnexpectedException

# main function to calculate order and print it on the console.
def print_order(order): 
    try:
        # calculate total amount of the order
        total_amount = get_total_order_amount(order)
    except:
        traceback.print_exc()
        total_amount = "ERROR"
    # calculate service charge based on the total amount.
    service_charge = "ERROR"
    if total_amount != "ERROR":
        try:
            service_charge = get_service_charge(order)
        except:
            traceback.print_exc()
            service_charge = "ERROR"
    # print charges on console.
    utils.cprint(
        "Final Order", color=colors.foreground["green"], on=colors.background["yellow"]
    )
    for i, item in enumerate(order):
        utils.cprint(
            f"{i+1}. {item.name}",
            color=colors.foreground["yellow"],
            on=colors.background["green"],
        )

    utils.cprint(
        f"Order Amount: {str(total_amount)}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )
    utils.cprint(
        f"Service Charge: {str(service_charge)}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )
    utils.cprint(
        f"Final Amount: {str(total_amount + service_charge) if isinstance(total_amount, (int, float)) and isinstance(service_charge, (int, float)) else 'ERROR'}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )

# Showing welcome line's
print()
utils.cprint(
    "Welcome to McDonalds on your shell :)",
    color=colors.foreground["blue"],
    on=colors.background["white"],
)
utils.cprint(
    "Here you can place your order        ",
    color=colors.foreground["blue"],
    on=colors.background["white"],
)
utils.cprint(
    "And then we will show you your bill  ",
    color=colors.foreground["blue"],
    on=colors.background["white"],
)
print()
# list to store selected items.
order = []

# loop's for showing options and beverage.
while True:
    options = list(map(lambda x: str(x), MCDONALDS_FOOD_OPTIONS))
    bullet = Bullet(prompt="Add an item", choices=options, bullet="=> ")
    result = bullet.launch()
    utils.clearConsoleUp(7)
    option = get_option_from_result(result, MCDONALDS_FOOD_OPTIONS)
    if result == str(MCDONALDS_FOOD_OPTIONS[-1]):
        break
    order.append(PurchaseItem(option))
    utils.cprint(
        f"{result} is added to your order", on=colors.background["green"], end="\n"
    )

while True:
    options = list(map(lambda x: str(x), MCDONALDS_BEVERAGES_OPTIONS))
    bullet = Bullet(prompt="Add a beverage", choices=options, bullet="=> ")
    result = bullet.launch()
    utils.clearConsoleUp(7)
    option = get_option_from_result(result, MCDONALDS_BEVERAGES_OPTIONS)
    if result == str(MCDONALDS_BEVERAGES_OPTIONS[-1]):
        break
    order.append(PurchaseItem(option))
    utils.cprint(
        f"{result} is added to your order", on=colors.background["green"], end="\n"
    )

utils.clearConsoleUp(1)
print()
print_order(order)
