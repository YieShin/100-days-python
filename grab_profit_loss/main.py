# Sample list to store your records
records = []


# Function to add a new record
def add_record(date, income, fuel, toll, parking, maintenance, others):
    total_expenses = fuel + toll + parking + maintenance + others
    profit = income - total_expenses
    records.append({
        "Date": date,
        "Income": income,
        "Fuel": fuel,
        "Toll": toll,
        "Parking": parking,
        "Maintenance": maintenance,
        "Others": others,
        "Total Expenses": total_expenses,
        "Profit": profit
    })


# Function to show summary
def show_summary():
    print("\nDaily Summary:")
    for r in records:
        print(f"{r['Date']}: Income = RM{r['Income']}, Expenses = RM{r['Total Expenses']}, Profit = RM{r['Profit']}")

    total_income = sum(r["Income"] for r in records)
    total_expenses = sum(r["Total Expenses"] for r in records)
    total_profit = sum(r["Profit"] for r in records)

    print("\n--- Monthly Summary ---")
    print(f"Total Income: RM{total_income}")
    print(f"Total Expenses: RM{total_expenses}")
    print(f"Total Profit: RM{total_profit}")


# Example usage:
add_record("2025-06-08", income=280, fuel=50, toll=10, parking=5, maintenance=0, others=10)
add_record("2025-06-09", income=300, fuel=60, toll=8, parking=4, maintenance=20, others=0)

show_summary()
