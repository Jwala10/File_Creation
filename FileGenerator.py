import tkinter as tk 
from tkinter import ttk, messagebox
import random
import datetime
import os
from tkinter import Tk, Frame 
from tkinter import ttk 
from ttkthemes import ThemedTk

# Function to generate random alphanumeric string of a given length
def generate_random_string(length):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

# Function to pad numeric fields with leading zeroes
def pad_numeric_field(value, length):
    return str(value).zfill(length)

# Function to pad alphanumeric fields with spaces
def pad_alphanumeric_field(value, length):
    return value.ljust(length)

# Function to generate the files
def generate_files():
    try:
        print("Generating files...")
        
        # Fetch user inputs
        product = product_var.get()
        num_files = int(num_files_var.get())
        sponsor_shortcode = sponsor_shortcode_var.get()
        txns_in_each_file = int(txns_in_each_file_var.get())
        username = pad_alphanumeric_field(username_var.get(), 40)
        user_defined_limit = user_defined_limit_var.get()

        if user_defined_limit:
            user_defined_limit = pad_numeric_field(user_defined_limit, 13)
        else:
            user_defined_limit = ' ' * 13

        total_amount = pad_numeric_field(total_amount_var.get(), 13)
        settlement_date = settlement_date_var.get()
        if len(settlement_date) != 8:
            raise ValueError("Settlement Date must be 8 digits (DDMMYYYY)")
        HDR_user_number = pad_numeric_field(header_user_number_var.get(), 18)
        HDR_sponsor_bank_code = pad_numeric_field(header_sponsor_bank_code_var.get(), 11)

        user_bank_account_number = user_bank_account_number_var.get()
        if user_bank_account_number:
            user_bank_account_number = pad_numeric_field(user_bank_account_number, 35)
        else:
            user_bank_account_number = ' ' * 35

        total_items = pad_numeric_field(txns_in_each_file, 9)
        
        # Generate a random User Reference
        user_reference = generate_random_string(18)
        
        # Create Header
        header = (
            f"{'23' if product == 'ACH-CR' else '56'}{' ' * 7}{username}{' ' * 14}{' ' * 9}{' ' * 9}{' ' * 15}{' ' * 3}"
            f"{user_defined_limit}{total_amount}{settlement_date}{' ' * 10}{' ' * 10}{' ' * 3}{HDR_user_number}{user_reference}"
            f"{HDR_sponsor_bank_code}{user_bank_account_number}{total_items}{' ' * 2}{' ' * 57}"
        )
        
        #if len(header) != 306:
            #raise ValueError("Field lengths are not matching. Header length must be 306 characters.")
        
        # Directory path where files will be saved
        directory = os.path.join(os.getcwd(), "generated_files")
        if not os.path.exists(directory):
            os.makedirs(directory)
        print(f"Directory created at {directory}")

        for i in range(num_files):
            filename = f"{product}-{sponsor_shortcode}-{sponsor_shortcode}Maker-{datetime.datetime.now().strftime('%d%m%Y')}-{random.randint(100000, 999999)}-INP.txt"
            filepath = os.path.join(directory, filename)
            print(f"Creating file at {filepath}")

            with open(filepath, "w") as file:
                file.write(header + "\n")
                
                # Generate records
                records = generate_records(product, txns_in_each_file, total_amount)
                for record in records:
                    file.write(record + "\n")

        messagebox.showinfo("Success", f"{num_files} files generated successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        print(f"Error occurred: {e}")

def generate_records(product, total_items, total_amount):
    records = []
    
    # User inputs for dynamic fields
    #destination_account_types = destination_account_type_var.get().split(',')
    #destination_account_types = list(set(destination_account_types))  # Unique values
    #if len(destination_account_types) > 2:
        #raise ValueError("Invalid length for Destination Account Type. Must be 2 or fewer digits.")


    destination_account_types = destination_account_type_var.get().split(',')
    destination_account_types = list(set(destination_account_types))  # Unique values
    if any(len(num) > 2 for num in destination_account_types):
        raise ValueError("Invalid length for account type. Must be 2 digits.")





    beneficiary_names = beneficiary_account_holder_name_var.get().split(',')
    if any(len(name) > 40 for name in beneficiary_names):
        raise ValueError("Invalid length for Beneficiary Account Holder's Name. Must be 40 characters or fewer.")
    
    destination_bank_codes = destination_bank_code_var.get().split(',')
    destination_bank_codes = list(set (destination_bank_codes))  # Unique values
    if any(len(code) > 11 for code in destination_bank_codes):
        raise ValueError("Invalid length for Destination Bank Code. Must be 11 characters or fewer.")
    
    beneficiary_account_numbers = beneficiary_account_number_var.get().split(',')
    beneficiary_account_numbers = list(set(beneficiary_account_numbers))  # Unique values
    if any(len(num) > 35 for num in beneficiary_account_numbers):
        raise ValueError("Invalid length for Beneficiary Account Number. Must be 35 digits or fewer.")
    
    sponsor_bank_codes = sponsor_bank_code_var.get().split(',')
    sponsor_bank_codes = list(set(sponsor_bank_codes))  # Unique values
    if any(len(code) > 11 for code in sponsor_bank_codes):
        raise ValueError("Invalid length for Sponsor Bank Code. Must be 11 characters or fewer.")
    
    user_numbers = user_number_var.get().split(',')
    user_numbers = list(set(user_numbers))  # Unique values
    if any(len(num) > 18 for num in user_numbers):
        raise ValueError("Invalid length for User Number. Must be 18 characters or fewer.")
    

    product_types = product_categories_var.get().split(',')
    product_types = list(set(product_types))  # Unique values
    if any(len(num) > 3 for num in product_types):
        raise ValueError("Invalid length for category. Must be 3 characters or fewer.")
    


    
    umrn_numbers = umrn_var.get().split(',')
    umrn_numbers = list(set(umrn_numbers))  # Unique values
    if any(len(num) > 20 for num in umrn_numbers):
        raise ValueError("Invalid length for UMRN Number. Must be 20 characters or fewer.")
    

    
    for _ in range(total_items):
        # Generate random values for fields
        ach_transaction_code = '12' if product == 'ACH-CR' else '67'
        control = ' ' * 9
        destination_account_type = random.choice(destination_account_types).zfill(2)
        lodger_folio_number = ' ' * 3
        control2 = ' ' * 15
        beneficiary_account_holder_name = random.choice(beneficiary_names).ljust(40)
        control3 = ' ' * 9
        control4 = ' ' * 7
        user_defined_narration = ' ' * 20
        control5 = ' ' * 13
        amount = str(int(total_amount) // total_items).zfill(13) if equal_amount_var.get() else str(random.randint(1, int(total_amount))).zfill(13)
        ach_item_seq_no = ' ' * 10
        checksum = ' ' * 10
        control6 = ' ' * 1
        reason_code = ' ' * 2
        destination_bank_code = random.choice(destination_bank_codes).zfill(11)
        beneficiary_account_number = random.choice(beneficiary_account_numbers).zfill(35)
        sponsor_bank_code = random.choice(sponsor_bank_codes).zfill(11)
        user_number = random.choice(user_numbers).zfill(18)
        txn_reference = generate_random_string(30)
        product_type = random.choice(product_types).zfill(3)
        Aadhaar_number= ' ' * 15
        umrn_number = random.choice(umrn_numbers).ljust(20) if product == 'ACH-DR' else ' ' * 20
        filler = ' ' * 7
        
        record = (
            f"{ach_transaction_code}{control}{destination_account_type}{lodger_folio_number}{control2}{beneficiary_account_holder_name}{control3}{control4}{user_defined_narration}{control5}{amount}{ach_item_seq_no}{checksum}{control6}{reason_code}{destination_bank_code}{beneficiary_account_number}{sponsor_bank_code}{user_number}{txn_reference}{product_type}{Aadhaar_number}{umrn_number}{filler}"
        )
        
        records.append(record)
    
    return records

# Clear fields
def clear_fields():
    for widget in file_frame.winfo_children() + header_frame.winfo_children() + record_frame.winfo_children():
        if isinstance(widget, ttk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, ttk.Combobox):
            widget.set('')
        elif isinstance(widget, tk.Checkbutton):
             widget.deselect()

# Create the main window
root = tk.Tk()
#root = ThemedTk(theme="equilux")
root.title("INP Files Generator")
root.wm_attributes('-fullscreen', True)

# Apply a background color
root.configure(bg='#F0F0F0')  # Light grey background
#root.configure(bg='#FFD1DC')

# Center all the widgets
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Styling
style = ttk.Style()
style.configure("TLabel", foreground="#333333", font=("Arial", 12, "bold"))  # Dark grey text
style.configure("TEntry", font=("Arial",  12), fieldbackground="#FFFFFF", foreground="black")  # White entry background
style.configure("TCombobox", font=("Arial", 12), fieldbackground="#FFFFFF", foreground="black")  # White combobox background
style.configure("TButton", font=("Arial", 12, "bold"))  # Button font

# File fields section
file_canvas = tk.Canvas(root, width=580, height=150)
file_canvas.grid(row=0, column=0, padx=20, pady=10, sticky='ew')

file_scrollbar = tk.Scrollbar(root, orient="vertical", command=file_canvas.yview)
file_scrollbar.grid(row=0, column=1, sticky='ns')

file_canvas.configure(yscrollcommand=file_scrollbar.set)

file_frame = ttk.Frame(file_canvas)
file_canvas.create_window((0, 0), window=file_frame, anchor='nw')

ttk.Label(file_frame, text="Product:", background="#E0FFFF").grid(row=0, column=0, padx=5, pady=5, sticky='w')
#ttk.Label(file_frame, text="Product:", background="#FFFFE0").grid(row=0, column=0, padx=5, pady=5, sticky='w')
product_var = tk.StringVar()
product_dropdown = ttk.Combobox(file_frame, textvariable=product_var, state="readonly")
product_dropdown['values'] = ("ACH-CR", "ACH-DR")
product_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(file_frame, text="No. of Files: *", foreground="red", background="#E0FFFF").grid(row=1, column=0, padx=5, pady=5, sticky='w')
num_files_var = tk.StringVar()
ttk.Entry(file_frame, textvariable=num_files_var).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(file_frame, text="Sponsor Shortcode: *", foreground="red", background="#E0FFFF").grid(row=2, column=0, padx=5, pady=5, sticky='w')
sponsor_shortcode_var = tk.StringVar()
ttk.Entry(file_frame, textvariable=sponsor_shortcode_var).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(file_frame, text="Txns in Each File: *", foreground="red", background="#E0FFFF").grid(row=3, column=0, padx=5, pady=5, sticky='w')
txns_in_each_file_var = tk.StringVar()
ttk.Entry(file_frame, textvariable=txns_in_each_file_var).grid(row=3, column=1, padx=5, pady=5, sticky='ew')

from tkinter import Checkbutton, IntVar

# Add a variable to track the state of the toggle
equal_amount_var = IntVar()

# Add the Equal Amount label
equal_amount_label = ttk.Label(file_frame, text="Equal Amount:", background="#E0FFFF")
equal_amount_label.grid(row=4, column= 0, padx=5, pady=5, sticky='w')

# Create the toggle switch
equal_amount_toggle = Checkbutton(file_frame, text="On/Off", variable=equal_amount_var, background="#E0FFFF", selectcolor="green", indicatoron=False, relief="solid", borderwidth=2)
equal_amount_toggle.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

# Update the scroll region
file_frame.update_idletasks()
file_canvas.configure(scrollregion=file_canvas.bbox("all"))

# Header fields section
header_canvas = tk.Canvas(root, width=580, height=200)
header_canvas.grid(row=1, column=0, padx=20, pady=10, sticky='ew')

header_scrollbar = tk.Scrollbar(root, orient="vertical", command=header_canvas.yview)
header_scrollbar.grid(row=1, column=1, sticky='ns')

header_canvas.configure(yscrollcommand=header_scrollbar.set)

header_frame = ttk.Frame(header_canvas)
header_canvas.create_window((0, 0), window=header_frame, anchor='nw')

ttk.Label(header_frame, text="User Name: *", foreground="red", background="#E0FFFF").grid(row=0, column=0, padx=5, pady=5, sticky='w')
username_var = tk.StringVar()
ttk.Entry(header_frame, textvariable=username_var).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(header_frame, text="User Defined Limit:", background="#E0FFFF").grid(row=1, column=0, padx=5, pady=5, sticky='w')
user_defined_limit_var = tk.StringVar()
ttk.Entry(header_frame, textvariable=user_defined_limit_var).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(header_frame, text="Total Amount: *", foreground="red", background="#E0FFFF").grid(row=2, column=0, padx=5, pady=5, sticky='w')
total_amount_var = tk.StringVar()
ttk.Entry(header_frame, textvariable=total_amount_var).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(header_frame, text="Settlement Date: *", foreground="red", background="#E0FFFF").grid(row=3, column=0, padx=5, pady=5, sticky='w')
settlement_date_var = tk.StringVar()
ttk.Entry(header_frame, textvariable=settlement_date_var).grid(row=3, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(header_frame, text="UserNumber: *", foreground="red", background="#E0FFFF").grid(row=4, column=0, padx=5, pady=5, sticky='w')
header_user_number_var = tk.StringVar()
ttk.Entry(header_frame, textvariable=header_user_number_var).grid(row=4, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(header_frame, text="SponsorCode: *", foreground="red", background="#E0FFFF").grid(row=5, column=0, padx=5, pady=5, sticky='w')
header_sponsor_bank_code_var = tk.StringVar()
ttk.Entry(header_frame, textvariable=header_sponsor_bank_code_var).grid(row=5, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(header_frame, text="User Bank Account Number:", background="#E0FFFF").grid(row=6, column=0, padx=5, pady=5, sticky='w')
user_bank_account_number_var = tk.StringVar()
ttk.Entry(header_frame, textvariable=user_bank_account_number_var).grid(row=6, column=1,)

# Update the scroll region
header_frame.update_idletasks()
header_canvas.configure(scrollregion=header_canvas.bbox("all"))

# Record fields section
record_canvas = tk.Canvas(root, width=580, height=250)
record_canvas.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

record_scrollbar = tk.Scrollbar(root, orient="vertical", command=record_canvas.yview)
record_scrollbar.grid(row=2, column=1, sticky='ns')

record_canvas.configure(yscrollcommand=record_scrollbar.set)

record_frame = ttk.Frame(record_canvas)
record_canvas.create_window((0, 0), window=record_frame, anchor='nw')

ttk.Label(record_frame, text="Destination AccountTypes: *", background="#E0FFFF").grid(row=0, column=0, padx=5, pady=5, sticky='w')
destination_account_type_var = tk.StringVar()
#ttk.Entry(record_frame, text variable=destination_account_type_var).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
ttk.Entry(record_frame, textvariable=destination_account_type_var).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
ttk.Label(record_frame, text="Beneficiary Names: *", foreground="red", background="#E0FFFF").grid(row=1, column=0, padx=5, pady=5, sticky='w')
beneficiary_account_holder_name_var = tk.StringVar()
ttk.Entry(record_frame, textvariable=beneficiary_account_holder_name_var).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(record_frame, text="Destination Bank Code: *", foreground="red", background="#E0FFFF").grid(row=2, column=0, padx=5, pady=5, sticky='w')
destination_bank_code_var = tk.StringVar()
ttk.Entry(record_frame, textvariable=destination_bank_code_var).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(record_frame, text="Beneficiary Account Number: *", foreground="red", background="#E0FFFF").grid(row=3, column=0, padx=5, pady=5, sticky='w')
beneficiary_account_number_var = tk.StringVar()
ttk.Entry(record_frame, textvariable=beneficiary_account_number_var).grid(row=3, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(record_frame, text="Sponsor Bank Codes: *", foreground="red", background="#E0FFFF").grid(row=4, column=0, padx=5, pady=5, sticky='w')
sponsor_bank_code_var = tk.StringVar()
ttk.Entry(record_frame, textvariable=sponsor_bank_code_var).grid(row=4, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(record_frame, text="UserNumbers: *", foreground="red", background="#E0FFFF").grid(row=5, column=0, padx=5, pady=5, sticky='w')
user_number_var = tk.StringVar()
ttk.Entry(record_frame, textvariable=user_number_var).grid(row=5, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(record_frame, text="UMRN: ", foreground="red", background="#E0FFFF").grid(row=6, column=0, padx=5, pady=5, sticky='w')
umrn_var = tk.StringVar()
ttk.Entry(record_frame, textvariable=umrn_var).grid(row=6, column=1, padx=5, pady=5, sticky='ew')

ttk.Label(record_frame, text="Product Category: *", foreground="red", background="#E0FFFF").grid(row=7, column=0, padx= 5, pady=5, sticky='w')
product_categories_var = tk.StringVar()
ttk.Entry(record_frame, textvariable=product_categories_var).grid(row=7, column=1, padx=5, pady=5, sticky='ew')

# Update the scroll region
record_frame.update_idletasks()
record_canvas.configure(scrollregion=record_canvas.bbox("all"))




# Set up the main window 
button_frame = tk.Frame(root) 
button_frame.grid(row=4, column=0, pady=20)

# Define custom styles 
style = ttk.Style() 
style.configure("Green.TButton", foreground="Green", background="#28a745", font=("Arial", 14, "bold")) 
style.configure("Red.TButton", foreground="Red", background="#dc3545", font=("Arial", 14, "bold")) 
style.map("Green.TButton", background=[('active', '#218838'), ('disabled', '#6c757d')]) 
style.map("Red.TButton", background=[('active', '#c82333'), ('disabled', '#6c757d')])



# Add the generate button with the new style and emoji 
generate_button = ttk.Button(button_frame, text="🚀 Generate Files", command=generate_files, style="Green.TButton") 
generate_button.grid(row=0, column=0, padx=10, pady=10)

# Add the clear button with the new style and emoji 
clear_button = ttk.Button(button_frame, text="🧹 Clear", command=clear_fields, style="Red.TButton") 
clear_button.grid(row=0, column=1, padx=10, pady=10)



# Start the GUI event loop
print("Starting the GUI event loop...")
root.mainloop()
print("Script ended")
