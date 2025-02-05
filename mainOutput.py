from additionalClassForOutput import ShoppingAnalytics, TimeFrame
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import re
from database_conn import Database


def parse_time_input(time_input: str) -> Tuple[int, TimeFrame]:
    """Parse time input string like '3 months' into value and unit"""
    match = re.match(r'(\d+)\s+(\w+)', time_input.strip())
    if not match:
        raise ValueError("Invalid time format. Use format like '3 months' or '1 year'")
    
    value, unit = match.groups()
    # Handle plural forms
    unit = unit.rstrip('s').lower()
    print(int(value), TimeFrame.from_string(unit))
    return int(value), TimeFrame.from_string(unit)


def handle_user_input(analytics: ShoppingAnalytics) -> bool:
    """Handle user input and return whether to continue"""
    print("\nWhat would you like to know? (or type 'done' to exit)")
    print("1. How much have I spent in last [time period]?")
    print("2. How much have I spent on [product] in last [time period]?")
    print("3. How much have I spent in [shop] in last [time period]?")
    print("4. Where did I shop the most in last [time period]?")
    print("5. What product cost me the most in last [time period]?")
    print("6. What's the average price for [product]?")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice.lower() == 'done':
        return False
        
    try:
        if choice == '1':
            time_input = input("Enter time period (e.g., '3 months'): ")
            value, unit = parse_time_input(time_input)
            total = analytics.get_total_spending(value, unit)
            print(f"\nTotal spending in last {value} {unit.value}: {total:.2f}Kč")

        elif choice == '2':
            product = input("Enter product name: ")
            time_input = input("Enter time period in days, weeks, months or years (e.g., '3 months'): ")
            value, unit = parse_time_input(time_input)
            stats = analytics.get_product_spending(product, value, unit)
            if stats:
                print(f"\nSpending on {product} in last {value} {unit.value}:")
                print(f"Total spent: {stats.total_spent:.2f} Kč")
                print(f"Amount bought: {stats.item_count:.2f}")
                print(f"Average price: {stats.avg_price:.2f} Kč")
            else:
                print(f"\nNo purchases of {product} found in that period")

        elif choice == '3':
            shop_id = int(input("Enter shop ID: "))
            time_input = input("Enter time period (e.g., '3 months'): ")
            value, unit = parse_time_input(time_input)
            stats = analytics.get_shop_spending(shop_id, value, unit)
            if stats:
                print(f"\nSpending in shop {shop_id} in last {value} {unit.value}:")
                print(f"Total spent: {stats.total_spent:.2f} Kč")
                print(f"Number of visits: {stats.item_count}")
                print(f"Average spending per visit: {stats.avg_price:.2f} Kč")
            else:
                print(f"\nNo visits to shop {shop_id} found in that period")

        elif choice == '4':
            time_input = input("Enter time period (e.g., '3 months'): ")
            value, unit = parse_time_input(time_input)
            result = analytics.get_most_visited_shop(value, unit)
            if result:
                shop_id, name, visits = result
                print(f"\nMost visited shop in last {value} {unit.value}:")
                print(f"Shop: {name} (ID: {shop_id})")
                print(f"Number of visits: {visits}")
            else:
                print("\nNo shop visits found in that period")

        elif choice == '5':
            time_input = input("Enter time period (e.g., '3 months'): ")
            value, unit = parse_time_input(time_input)
            result = analytics.get_most_expensive_product(value, unit)
            if result:
                print(f"\nMost expensive product in last {value} {unit.value}:")
                print(f"Product: {result[0]}")
                print(f"Total cost: {result[1]:.2f} Kč")
                print(f"Total quantity: {result[2]/100:.2f}")
                print(f"Number of purchases: {result[3]}")
            else:
                print("\nNo purchases found in that period")

        elif choice == '6':
            product = input("Enter product name: ")
            stats = analytics.get_product_price_stats(product)
            if stats:
                print(f"\nPrice statistics for {product}:")
                print(f"Minimum price: {stats[0]:.2f} Kč")
                print(f"Maximum price: {stats[1]:.2f} Kč")
                print(f"Average price: {stats[2]:.2f} Kč")
                print(f"Total amount bought: {stats[3]:.2f}")
                print(f"Available in {stats[4]} shops")
            else:
                print(f"\nNo data found for {product}")

        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")

    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    
    return True


def main():
    """Main function to run the shopping analytics CLI"""
    print("Welcome to Shopping Analytics!")
    print("You can analyze your shopping history here.")
    
    db = Database()
    analytics = ShoppingAnalytics(db)
    
    while handle_user_input(analytics):
        pass
    
    print("\nThank you for using Shopping Analytics!")


if __name__ == "__main__":
    main()