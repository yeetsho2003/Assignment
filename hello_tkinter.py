import tkinter as tk

root = tk.Tk()
root.title("Hello from Tkinter")
root.geometry("320x150")
label = tk.Label(root, text="Hello, Kuromi Library!")
label.pack(pady=18)
button = tk.Button(root, text="Click me ♡", command=lambda: label.config(text="Button clicked! ✨"))
button.pack()
root.mainloop()
