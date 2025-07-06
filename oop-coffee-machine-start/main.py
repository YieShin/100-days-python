from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

is_on = True

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

while is_on:
    # ANGELA's SOLUTION
    options = menu.get_items()
    choice = input(f"What would you like? ({options}): ")
    if choice == "off":
        is_on = False
    elif choice == "report":
        coffee_maker.report()
        money_machine.report()
    else:
        drink = menu.find_drink(choice)
        if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
            coffee_maker.make_coffee(drink)
    # SHIN's SOLUTION
    # choice = input(f"What would you like? ({menu.get_items()}): ")
    #
    # menu_choice = menu.find_drink(choice)
    # if choice == "off":
    #     is_on = False
    # elif choice == "report":
    #     coffee_maker.report()
    #     money_machine.report()
    # elif menu_choice:
    #     if coffee_maker.is_resource_sufficient(menu_choice):
    #         if money_machine.make_payment(menu_choice.cost):
    #             coffee_maker.make_coffee(menu_choice)
