import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import requests 

payload = {}
headers= {
  "apikey": "O86H631tBxLFWCtzNk63LeQGaSXqJpCX"
}

expensesList =[]
showList =[]
# getting the data and validating it
def get_amount():
    amount = amount_entry.get().strip()  # Get entry text and remove leading/trailing spaces
    if not amount:
        messagebox.showinfo("Error", "This field cannot be empty")
        amount_entry.config(bg="red")
    else:
        try:
            amount = float(amount)
            amount_entry.config(bg="white")
        except ValueError:
            amount_entry.config(bg="red")
            messagebox.showinfo("Error", "Enter a numeric value")
             # إيقاف تنفيذ الدالة في حالة حدوث خطأ بالتحويل إلى رقم
            return #  للحفاظ على البرنامج من ان يتم ادخال قيم غير عدديه و بالتالي يتوقف عن العمل
        
    return amount        

# داله للتحقق من انه ال entery بتاع tk مش فاضي 
# انا كنت عاملها لكل الخانات بس ال combo  ما نفعش معاها 
# هي حالا بتشيك على خانه التاريخ فقط بس هسيبها بحث ممكن استخدمها بعدين        
def get_data(data_entry, data_name):
    data = data_entry.get().strip()  # Get entry text and remove leading/trailing spaces
    if not data:
        messagebox.showinfo("Error", f"The {data_name} field cannot be empty")
        data_entry.config(bg="red")  # Change background color to red for the empty field
    else:
        data_entry.config(bg="white")  # Change background color back to default for a filled field
    return data    

# داله بتvalidate انه ال combo قيمته مش فاضيه
def validate_entry(entry, field_name):
        data = entry.get().strip()
        if not data:
            messagebox.showinfo("Error", f"The {field_name} field cannot be empty")
            style = ttk.Style()
            style.map('TCombobox', fieldbackground=[('readonly', 'red')])
        else:
            style = ttk.Style()
            style.map('TCombobox', fieldbackground=[('readonly', 'white')])   
        return data      
  
# داله لادخال قيمة التاريخ تلقائيا
def show_current_date(event=None):
    current_date = datetime.now().strftime("%Y-%m-%d")  # تنسيق التاريخ إلى YYYY-MM-DD
    date_entry.delete(0, tk.END)  # مسح المحتوى الحالي في الحقل
    date_entry.insert(0, current_date)  # إدراج التاريخ الحالي في الحقل
    
# داله لتحويل ا لنفقات الى قيمتها بالدولار و ايجاد مجموعها     
def calculate_total_expenses():
    sum_of_expenses = []
    for expense in expensesList:
        amount = expense[0]
        initial_currency = expense[1]
        target_currency = 'USD'
        url = f"https://api.apilayer.com/fixer/convert?to={target_currency}&from={initial_currency}&amount={amount}"
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code

        if status_code != 200:
            print("There is a problem,Please try again later.")
            exit()

        result = response.json()   
        converted_amount = result['result']
        sum_of_expenses.append(converted_amount)

    total_amount = sum(sum_of_expenses)
    return total_amount

# حافظ على مؤشر للصف الأخير الذي تم إضافته للجدول
last_total_row_id = None
total_row_tag = 'total_row'  # علامة خاصة بالصف الذي يعرض مجموع النفقات

def add_expense():
    global last_total_row_id
    
    am = get_amount()
    date = get_data(date_entry, "Date")
    currency = validate_entry(combo_currency, "Currency")
    category = validate_entry(combo_category, "Category")
    method = validate_entry(combo_PM, "Payment Method")

    #calculate_total_expenses(am,currency)

    if am and date and currency and category and method:
        # حذف الصف القديم لمجموع النفقات إذا كان موجوداً
        if last_total_row_id:
            dataBox.delete(last_total_row_id)

        # إضافة الصف الجديد للنفقات
        expensesList.append([am, currency, category, method, date])
        dataBox.insert('', 'end', values=(am, currency, category, method, date))

        # إضافة الصف الجديد لمجموع النفقات
        total_row_values = (calculate_total_expenses(), "USD", "", "", "")
        last_total_row_id = dataBox.insert('', 'end', values=total_row_values, tags=total_row_tag)
        dataBox.tag_configure(total_row_tag, background='Yellow')  # تغيير لون الصف
        

 

# Create the main window
root = tk.Tk()
root.title("Expenses Tracker")  # Set window title

# Create entry Form
# Create widgets
amount_label =tk.Label(root, text='Amount' )
currency_label =tk.Label(root, text='Currency' )
category_label =tk.Label(root, text='Category' )
payment_method_label =tk.Label(root, text='Payment Method' )
date_label =tk.Label(root, text='Date' )

amount_entry =tk.Entry(root,  )
date_entry =tk.Entry(root)
# ربط حدث التركيز بالدالة
date_entry.bind("<FocusIn>", show_current_date)


# زر لحفظ البيانات
add_expense_button = tk.Button(root, text="Add expense", command=add_expense)
add_expense_button.grid(row=5, column=1)

# جدول عرض النفقات
cols = ('Amount', 'Currency', 'Category','Payment Method','Date')
dataBox = ttk.Treeview(root, columns=cols, show='headings')
# set column headings
for col in cols:
	dataBox.heading(col, text=col)   
     
# تخصيص مظهر الجدول باستخدام CSS
style = ttk.Style()
style.theme_use("alt")  # يمكن استخدام أي من الثيمات المتاحة في tkinter: "clam", "alt", "default", "classic"
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#FFFFFF")
style.map("Treeview", background=[('selected', '#347083')])      
dataBox.grid(row=6, column=0, columnspan=2)

 

# Place widgets
amount_label.grid(row=0, column=0)
currency_label.grid(row=1, column=0)
category_label.grid(row=2, column=0)
payment_method_label.grid(row=3, column=0)
date_label.grid(row=4, column=0)

amount_entry.grid(row=0, column=1)
date_entry.grid(row=4, column=1)


# القوائم المنسدلة
# 1- for currency
options_currency = ["USD", "EGP", "EUR",]
combo_currency = ttk.Combobox(root, values=options_currency)
combo_currency.grid(row=1, column=1)
#2 - for Category
options_category = ["life expenses", "electricity", "gas", "rental", "grocery", "savings", "education", "charity"]
combo_category = ttk.Combobox(root, values=options_category)
combo_category.grid(row=2, column=1)
# 3- for Paymet method
options_PM = ["Cash", "Credit" "Card", "Paypal",]
combo_PM = ttk.Combobox(root, values=options_PM)
combo_PM.grid(row=3, column=1)


# Run the main loop
root.mainloop()
