import copy
from textAnalyzer.assign_by_database import assign_by_database
from datetime import datetime
import os
class Communicator:
    def __init__(self, db):
        self.db = db
    def get_image_path(self):
        image_path = input("Enter image path: ").strip().strip('"')
        os.makedirs("images", exist_ok=True)
        new_filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}{os.path.splitext(image_path)[1]}"
        new_path = os.path.join("images", new_filename)
        with open(image_path, 'rb') as src, open(new_path, 'wb') as dst:
            dst.write(src.read())
        
        print(f"Saved image to: {new_path}")
        return new_path

    
    def pretty_print(self, store_info_tuple, assigned_products):
        store, date, total = store_info_tuple
        
        store_lines = [
            f"A | Store: {store}",
            f"B | Date: {date}",
            f"C | Total: {total/100:.2f}"
        ]
        max_store_line_length = max(len(line) for line in store_lines)
        store_divider = '+' + '-' * (max_store_line_length + 2) + '+'
        print(store_divider)
        for line in store_lines:
            print(f"| {line.ljust(max_store_line_length)} |")
        print(store_divider)
        print()

        # Prepare product table data
        headers = ['No.', 'Name', 'Total Price', 'Amount', 'Units', 'Class', 'Flag']
        data_rows = []
        ai_rows = []
        
        for idx, product in enumerate(assigned_products, 1):
            print('product', product)
            source = self._get_source(product['flag'])
            if product['flag'] in [20, 21]:
                ai_rows.append(str(idx))
            
            # Extract class names from tuples and join with '/'
            if product['class'] is None:
                class_names = 'not Found'
            else:
                class_names = '/'.join(class_tuple[1] for class_tuple in product['class'])
            
            data_row = [
                f"{idx}.",
                product['name'],
                f"{product['total_price']/100:.2f}",
                f"{product['amount']/100:.2f}",
                product['units'],
                class_names,
                source
            ]
            data_rows.append(data_row)

        # Calculate column widths
        col_widths = [len(header) for header in headers]
        for row in data_rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Create table components
        divider = '+' + '+'.join(['-' * (w + 2) for w in col_widths]) + '+'
        header_row = '| ' + ' | '.join(
            [header.ljust(col_widths[i]) for i, header in enumerate(headers)]
        ) + ' |'

        # Print product table
        print(divider)
        print(header_row)
        print(divider)
        
        for row in data_rows:
            formatted_row = []
            for i, cell in enumerate(row):
                if i == 0:  # Right-align numbers
                    formatted_cell = cell.rjust(col_widths[i])
                else:
                    formatted_cell = str(cell).ljust(col_widths[i])
                formatted_row.append(formatted_cell)
            print('| ' + ' | '.join(formatted_row) + ' |')
        
        print(divider)

        # Print notes if there are AI-assigned rows
        if ai_rows:
            print("\nSource Legend:")
            print("DB = Assigned by database")
            print("AI = Assigned by AI")
            print("AI (Not Found) = Assigned by AI but not found in database")
            print("User = Assigned by user")
            ai_indices = ', '.join(ai_rows)
            print(f"\nNote: Rows {ai_indices} need verification (assigned by AI).")

    def _get_source(self, flag):
        if flag == 10:
            return "DB"
        elif flag == 20:
            return "AI"
        elif flag == 21:
            return "AI (Will Create New Class)"
        elif flag == 30:
            return "User (Existing Class)"
        elif flag == 31:
            return "User (New Class)"
        return "Unknown"
    
    def edit_receipt(self, store_info_tuple, assigned_products):
        edited_store = list(store_info_tuple)
        edited_products = copy.deepcopy(assigned_products)
        
        while True:
            self.pretty_print(tuple(edited_store), edited_products)
            choice = input("\nEnter item to edit (A-C/Number), '+' to add, '-' to remove, or 'done': ").strip().lower()
            
            if choice == 'done':
                # Check if all edited products have a class length of 1
                all_classes_single = all(len(product['class']) == 1 for product in edited_products if product['class'] is not None)
                if all_classes_single:
                    try:
                        _ = datetime.strptime(edited_store[1], "%d.%m.%Y").date()
                    except ValueError:
                        print("Invalid date format! Please use DD.MM.YYYY.")
                        continue
                    return tuple(edited_store), edited_products if edited_products is not None else []
                else:
                    print("All products must have exactly one class assigned.")
                    continue
            
            if choice == '+':
                self._add_new_product(edited_products)
                continue

            if choice == '-':
                product_num = input("Enter product number to remove: ").strip()
                try:
                    idx = int(product_num) - 1
                    if 0 <= idx < len(edited_products):
                        del edited_products[idx]
                    else:
                        print("Invalid product number!")
                except ValueError:
                    print("Invalid input!")
                continue
            
            # Edit store information
            if choice in ['a', 'b', 'c']:
                field_names = ['Store name', 'Date in format DD.MM.YYYY', 'Total']
                idx = ord(choice) - ord('a')
                new_val = input(f"New {field_names[idx]}: ")
                if idx == 1:
                    try:
                        _ = datetime.strptime(new_val , "%d.%m.%Y").date()
                    except ValueError:
                        print("Invalid date format! Please use DD.MM.YYYY.")
                        continue
                if idx == 2:
                    try:
                        int(float(new_val) * 100)
                    except ValueError:
                        print("Invalid price!")
                edited_store[idx] = new_val
                continue
            
            # Edit product
            try:
                product_num = int(choice)
                if not 1 <= product_num <= len(edited_products):
                    raise ValueError
            except ValueError:
                print("Invalid input")
                continue
            
            product = edited_products[product_num-1]
            self._edit_product(product, product_num)
            
    def _edit_product(self, product, product_num):
        print(f"\nEditing product {product_num}:")
        print("1. Name\n2. Price\n3. Amount\n4. Units\n5. Class")
        choice = input("Select field to edit: ")
        
        if choice == '1':
            product['name'] = input("New name: ").strip()
        elif choice == '2':
            try:
                product['total_price'] = int(float(input("New price: ")) * 100)
            except ValueError:
                print("Invalid price!")
        elif choice == '3':
            try:
                product['amount'] = int(float(input("New amount: ")) * 100)
            except ValueError:
                print("Invalid amount!")
        elif choice == '4':
            product['units'] = input("New units: ").strip()
        elif choice == '5':
            self._handle_class_edit(product)
        else:
            print("Invalid choice")

    def _add_new_product(self, products):
        new_product = {
            'name': input("Enter product name: ").strip(),
            'total_price': int(float(input("Enter price: ")) * 100),
            'amount': int(float(input("Enter amount: ")) * 100),
            'units': input("Enter units: ").strip(),
            'flag': 30,
            'class': None
        }
        
        # Handle class assignment
        self._handle_class_edit(new_product)
        products.append(new_product)

    def _handle_class_edit(self, product):
        while True:
            new_class = (0, input("New class name: ").strip())
            result = assign_by_database(new_class[1], self.db)
            
            if result is None:  # Exact match found in DB
                product.update({'class': {new_class}, 'flag': 31})
                return
                
            # Handle possible matches
            possible_matches = result
            if possible_matches:
                print(f"Did you mean: {', '.join(match[1] for match in possible_matches)}?")
                confirm = input("Is your class a subclass of these? (y/n): ").lower()
                if confirm == 'y':
                    if len(possible_matches[1]) == 1:
                        
                        product.update({'class': possible_matches[0], 'flag': 30})
                    else:
                        print("Please use the parent class instead")
                        continue
                
            # If no matches or user confirms
            product.update({'class': {new_class}, 'flag': 31})
            return
