import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests

payload = {}
headers= {
  "apikey": "O86H631tBxLFWCtzNk63LeQGaSXqJpCX"
}


class ExpenseTrackerApp:
    """
    ExpenseTrackerApp class represents an expense tracking application.

    Attributes:
    - root: tkinter.Tk object, the main application window.
    - expenses_list: list, holds the list of expenses.
    - last_total_row_id: str, keeps track of the last total row added to the UI.
    - total_row_tag: str, tag for identifying the total row in the UI.

    Methods:
    - __init__(self, root): Initializes the ExpenseTrackerApp instance and creates the GUI.
    - create_widgets(self): Creates all the GUI elements for the expense tracker.
    - get_amount(self): Gets and validates the amount input from the user.
    - get_data(self, data_entry, data_name): Gets and validates data from entries.
    - validate_entry(self, entry, field_name): Validates data from combo boxes.
    - show_current_date(self, event=None): Displays the current date in the date entry.
    - calculate_total_expenses(self): Calculates the total expenses in USD.
    - add_expense(self): Handles adding expenses to the tracker and updating the UI.
    """

    def __init__(self, root):
        """
        Initialize the ExpenseTrackerApp.

        Parameters:
        - root: tkinter.Tk object, the main application window.
        """
        self.root = root
        self.root.title("Expenses Tracker")
        self.expenses_list = []
        self.last_total_row_id = None
        self.total_row_tag = 'total_row'

        self.create_widgets()

    def create_widgets(self):
        """
        Create GUI elements for the expense tracker.

        Creates labels, entry fields, buttons, dropdowns, and the Treeview for displaying expenses.
        Binds actions to GUI elements.
        """
        # Create labels and entries
        self.amount_label = tk.Label(self.root, text='Amount')
        self.currency_label = tk.Label(self.root, text='Currency')
        self.category_label = tk.Label(self.root, text='Category')
        self.payment_method_label = tk.Label(self.root, text='Payment Method')
        self.date_label = tk.Label(self.root, text='Date')

        self.amount_entry = tk.Entry(self.root)
        self.date_entry = tk.Entry(self.root)

        # Create buttons
        self.add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)

        # Create Treeview for displaying expenses
        self.cols = ('Amount', 'Currency', 'Category', 'Payment Method', 'Date')
        self.data_box = ttk.Treeview(self.root, columns=self.cols, show='headings')
        for col in self.cols:
            self.data_box.heading(col, text=col)

        # Bind date entry focus to show current date
        self.date_entry.bind("<FocusIn>", self.show_current_date)

        # Create dropdowns (Comboboxes)
        options_currency = ["USD", "EGP", "EUR"]
        self.combo_currency = ttk.Combobox(self.root, values=options_currency)

        options_category = ["life expenses", "electricity", "gas", "rental", "grocery", "savings", "education", "charity"]
        self.combo_category = ttk.Combobox(self.root, values=options_category)

        options_PM = ["Cash", "Credit Card", "Paypal"]
        self.combo_PM = ttk.Combobox(self.root, values=options_PM)

        # Place widgets in the grid
        self.amount_label.grid(row=0, column=0)
        self.currency_label.grid(row=1, column=0)
        self.category_label.grid(row=2, column=0)
        self.payment_method_label.grid(row=3, column=0)
        self.date_label.grid(row=4, column=0)

        self.amount_entry.grid(row=0, column=1)
        self.date_entry.grid(row=4, column=1)

        self.add_expense_button.grid(row=5, column=1)

        self.data_box.grid(row=6, column=0, columnspan=2)
        self.combo_currency.grid(row=1, column=1)
        self.combo_category.grid(row=2, column=1)
        self.combo_PM.grid(row=3, column=1)

    def get_amount(self):
        """
        Get and validate the amount entered by the user.

        Returns:
        - float: The validated amount entered by the user.
        """
        amount = self.amount_entry.get().strip()
        if not amount:
            messagebox.showinfo("Error", "This field cannot be empty")
            self.amount_entry.config(bg="red")
        else:
            try:
                amount = float(amount)
                self.amount_entry.config(bg="white")
            except ValueError:
                self.amount_entry.config(bg="red")
                messagebox.showinfo("Error", "Enter a numeric value")
                return  # إيقاف تنفيذ الدالة في حالة حدوث خطأ بالتحويل إلى رقم
        return amount

    def get_data(self, data_entry, data_name):
        """
        Get and validate data entered in the entry fields.

        Parameters:
        - data_entry: tk.Entry object, entry field to get data from.
        - data_name: str, name of the data field.

        Returns:
        - str: The validated data entered in the field.
        """
        data = data_entry.get().strip()
        if not data:
            messagebox.showinfo("Error", f"The {data_name} field cannot be empty")
            data_entry.config(bg="red")
        else:
            data_entry.config(bg="white")
        return data

    def validate_entry(self, entry, field_name):
        """
        Validate data from combo boxes.

        Parameters:
        - entry: ttk.Combobox object, combo box entry to validate.
        - field_name: str, name of the field.

        Returns:
        - str: The validated data from the combo box.
        """
        data = entry.get().strip()
        if not data:
            messagebox.showinfo("Error", f"The {field_name} field cannot be empty")
            style = ttk.Style()
            style.map('TCombobox', fieldbackground=[('readonly', 'red')])
        else:
            style = ttk.Style()
            style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        return data

    def show_current_date(self, event=None):
        """
        Display the current date in the date entry field.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, current_date)


    def calculate_total_expenses(self):
        """
        Calculate the total expenses in USD.

        Uses API to convert different currencies to USD and calculates the total.

        Returns:
        - float: The total expenses in USD.
        """
        sum_of_expenses = []
        for expense in self.expenses_list:
            amount = expense[0]
            initial_currency = expense[1]
            target_currency = 'USD'
            url = f"https://api.apilayer.com/fixer/convert?to={target_currency}&from={initial_currency}&amount={amount}"
            response = requests.request("GET", url, headers=headers, data=payload)
            status_code = response.status_code

            if status_code != 200:
                print("There is a problem, Please try again later.")
                exit()

            result = response.json()
            converted_amount = result['result']
            sum_of_expenses.append(converted_amount)

        total_amount = sum(sum_of_expenses)
        return total_amount

    def add_expense(self):
        """
        Add expense to the tracker and update the UI.

        Validates user inputs, adds expenses to the list, and updates the display.
        """
        am = self.get_amount()
        date = self.get_data(self.date_entry, "Date")
        currency = self.validate_entry(self.combo_currency, "Currency")
        category = self.validate_entry(self.combo_category, "Category")
        method = self.validate_entry(self.combo_PM, "Payment Method")

        if am and date and currency and category and method:
            if self.last_total_row_id:
                self.data_box.delete(self.last_total_row_id)

            self.expenses_list.append([am, currency, category, method, date])
            self.data_box.insert('', 'end', values=(am, currency, category, method, date))

            total_row_values = (self.calculate_total_expenses(), "USD", "", "", "")
            self.last_total_row_id = self.data_box.insert('', 'end', values=total_row_values, tags=self.total_row_tag)
            self.data_box.tag_configure(self.total_row_tag, background='Yellow')

def main():
    """
    Entry point of the application.
    Creates the main tkinter window and runs the Expense Tracker app.
    """
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
