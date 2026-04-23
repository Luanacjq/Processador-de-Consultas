from ui.app import App
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("My Application")
    root.geometry("400x300")

    app = App(root)

    root.mainloop()