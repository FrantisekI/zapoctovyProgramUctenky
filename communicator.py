import copy
class Communicator:
    def __init__(self, db):
        self.db = db
    def pretty_print(self, store_info_tuple, assigned_products):
        store, date, total = store_info_tuple
        
        store_lines = [
            f"A | Store: {store}",
            f"B | Date: {date}",
            f"C | Total: {total}"
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
                f"{product['total_price']:.2f}",
                str(product['amount']),
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
            ai_indices = ', '.join(ai_rows)
            print(f"\nNote: Rows {ai_indices} need verification (assigned by AI).")

    def _get_source(self, flag):
        if flag == 10:
            return "DB"
        elif flag == 20:
            return "AI"
        elif flag == 21:
            return "AI (Not Found)"
        return "Unknown"
    def edit_receipt(self, store_info_tuple, assigned_products):
        edited_store = list(store_info_tuple)
        edited_products = copy.deepcopy(assigned_products)
        
        while True:
            self.pretty_print(tuple(edited_store), edited_products)
            choice = input("\nEnter item to edit (A-C/Number) or 'done': ").strip().lower()
            
            if choice == 'done':
                return tuple(edited_store), edited_products
            
            # Edit store information
            if choice in ['a', 'b', 'c']:
                field_names = ['Store name', 'Date', 'Total']
                idx = ord(choice) - ord('a')
                new_val = input(f"New {field_names[idx]}: ")
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
                product['total_price'] = float(input("New price: "))
            except ValueError:
                print("Invalid price!")
        elif choice == '3':
            try:
                product['amount'] = int(input("New amount: "))
            except ValueError:
                print("Invalid amount!")
        elif choice == '4':
            product['units'] = input("New units: ").strip()
        elif choice == '5':
            self._handle_class_edit(product)
        else:
            print("Invalid choice")

    def _handle_class_edit(self, product):
        while True:
            new_class = input("New class name: ").strip()
            result = self.assign_by_database(new_class)
            
            if result is None:  # Exact match found in DB
                product.update({'class': new_class, 'flag': 10})
                return
                
            # Handle possible matches
            _, possible_matches = result
            if possible_matches:
                print(f"Did you mean: {', '.join(possible_matches)}?")
                confirm = input("Is your class a subclass of these? (y/n): ").lower()
                if confirm == 'y':
                    print("Please use the parent class instead")
                    continue
                
            # If no matches or user confirms
            product.update({'class': new_class, 'flag': 21})
            return
