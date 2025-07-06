MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "milk": 0,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

cash_in_hand = 0.0

# CONSTANTS
ESPRESSO = "espresso"
LATTE = "latte"
CAPPUCCINO = "cappuccino"
REPORT = "report"
INGREDIENTS = "ingredients"
COFFEE = "coffee"
WATER = "water"
MILK = "milk"
COST = "cost"
OFF = "off"


# FUNCTIONS
def add_cash(cost):
    return float(cash_in_hand + cost)


def show_report():
    """Return report of resources left."""
    return (f"Water: {resources[WATER]}ml\n"
            f"Milk: {resources[MILK]}ml\n"
            f"Coffee: {resources[COFFEE]}g\n"
            f"Money: ${cash_in_hand}")


# Coin types
PENNY = 0.01
DIME = 0.1
NICKLE = 0.05
QUARTER = 0.25

is_operating = True

while is_operating:
    # First input answer
    feedback = input("What would you like? (espresso/latte/cappuccino): ").lower()

    if feedback == ESPRESSO or feedback == LATTE or feedback == CAPPUCCINO:
        # MENU var
        menu_ingredient = MENU[feedback][INGREDIENTS]
        menu_cost = MENU[feedback][COST]
        water_usage = menu_ingredient[WATER]
        milk_usage = menu_ingredient[MILK]
        coffee_usage = menu_ingredient[COFFEE]

        # resources var
        water_stock = resources[WATER]
        milk_stock = resources[MILK]
        coffee_stock = resources[COFFEE]

        message = f"Here is your {feedback}. Enjoy!"

        # Check if stock is enough for making coffee
        if water_stock < water_usage:
            message = "Sorry there is not enough water"
        elif milk_stock < milk_usage:
            message = "Sorry there is not enough milk"
        elif coffee_stock < coffee_usage:
            message = "Sorry there is not enough coffee"

        if water_stock > water_usage and milk_stock > milk_usage and coffee_stock > coffee_usage:
            # Process coins.
            print("Please insert coins.")
            inserted_quarters = float(input("How many quarters?: ")) * QUARTER
            inserted_dimes = float(input("How many dimes?: ")) * DIME
            inserted_nickles = float(input("How many nickles?: ")) * NICKLE
            inserted_pennies = float(input("How many pennies?: ")) * PENNY

            inserted_sum = round(inserted_quarters + inserted_dimes + inserted_nickles + inserted_pennies, 2)

            if inserted_sum > menu_cost:
                # Enough money to pay
                if water_stock > water_usage and milk_stock > milk_usage and coffee_stock > coffee_usage:
                    # If stock is enough making coffee, deduct stock for making new coffee
                    resources[WATER] -= water_usage
                    resources[MILK] -= milk_usage
                    resources[COFFEE] -= coffee_usage
                    cash_in_hand = add_cash(menu_cost)
            else:
                # Not enough money to pay
                message = "Sorry that's not enough money. Money refunded"

        print(message)
    # Operator feedback
    elif feedback == REPORT:
        print(show_report())
    elif feedback == OFF:
        is_operating = False
