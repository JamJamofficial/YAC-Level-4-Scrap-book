import tkinter as tk
from tkinter import ttk

def create_fruit_widget():
    """Fruity Fruits"""

    # Define the list of fruits
    fruits = [
        "Apple", "Banana", "Orange", "Grape", "Strawberry",
        "Mango", "Pineapple", "Watermelon", "Kiwi", "Peach"
    ]

    # Create the main window
    root = tk.Tk()
    root.title("Fruity fruits")

    # Create a canvas 
    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar 
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame to hold the fruit labels
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Fill the frame with fruit labels
    for i in range(100): # Repeat the list 100 times
        for fruit in fruits:
            label = tk.Label(frame, text=fruit)
            label.pack(pady=5)

    root.mainloop()

# Run the widget
create_fruit_widget()
