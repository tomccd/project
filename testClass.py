import tkinter as tk
from tkinter import ttk

class NotebookContent(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height)
        self.master = master
        
        self.label = tk.Label(self, text="Treeview Content")
        self.label.pack()

        self.treeview = ttk.Treeview(self)
        self.treeview.pack(fill='both', expand=True)

class MainApplication(tk.Frame):
    def __init__(self, master, frame_width, frame_height):
        super().__init__(master, width=frame_width, height=frame_height)
        self.master = master
        self.pack(fill='both', expand=True)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        for i in range(3):
            notebook_content = NotebookContent(self.notebook, width=frame_width, height=frame_height)
            self.notebook.add(notebook_content, text=f"Notebook {i+1}")

# Tạo ra ứng dụng giao diện chính
def main():
    root = tk.Tk()
    frame_width = 300
    frame_height = 200
    app = MainApplication(root, frame_width, frame_height)
    root.mainloop()

if __name__ == "__main__":
    main()
