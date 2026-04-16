import tkinter as tk

# window creation
root = tk.Tk()

root.geometry("500x500")
root.title("Tkinter practice")

# Adding text/textbox
Label = tk.Label(root, text="Hello there", font =  ("Papyrus", 30))
Label.pack()

textbox = tk.Text(root)
textbox.insert("1.0", "Type here")
textbox.pack()

# Buttons
button = tk.Button(root, text="Click here")
button.pack(padx = 10, pady=5)

# Entry fields
entry_field = tk.Entry(root)
entry_field.pack()

root.mainloop()
