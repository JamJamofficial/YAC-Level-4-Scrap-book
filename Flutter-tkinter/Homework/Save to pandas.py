import pandas as pd
import tkinter as tk
from tkinter import messagebox

# save data
def save_data():
    first_name = entry_first.get()
    middle_name = entry_middle.get()
    last_name = entry_last.get()
    age = entry_age.get()
    phone = entry_phone.get()
    address = entry_address.get()
    hobby = entry_hobby.get()

    if not all([first_name, last_name, age, phone, address, hobby]):
        messagebox.showwarning("Warning", "Please fill in all required fields.")
        return

    # Create dataframe
    df = pd.DataFrame([{
        "First Name": first_name,
        "Middle Name": middle_name,
        "Last Name": last_name,
        "Age": age,
        "Phone Number": phone,
        "Address": address,
        "Hobby": hobby
    }])

    # Add to CSV file
    try:
        df.to_csv("users.csv", mode='a', index=False, header=not pd.io.common.file_exists("users.csv"))
        messagebox.showinfo("Success", "Data saved successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")

root = tk.Tk()
root.title("Save to pandas")
root.geometry("350x400")

# Labels 
tk.Label(root, text="First Name").pack()
entry_first = tk.Entry(root)
entry_first.pack()

tk.Label(root, text="Middle Name").pack()
entry_middle = tk.Entry(root)
entry_middle.pack()

tk.Label(root, text="Last Name").pack()
entry_last = tk.Entry(root)
entry_last.pack()

tk.Label(root, text="Age").pack()
entry_age = tk.Entry(root)
entry_age.pack()

tk.Label(root, text="Phone Number").pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

tk.Label(root, text="Address").pack()
entry_address = tk.Entry(root)
entry_address.pack()

tk.Label(root, text="Hobby").pack()
entry_hobby = tk.Entry(root)
entry_hobby.pack()

tk.Button(root, text="Save to CSV", command=save_data, bg="green", fg="white").pack(pady=10)

root.mainloop()
