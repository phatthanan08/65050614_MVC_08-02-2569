import tkinter as tk
from tkinter import ttk
from views.complaint_list_view import ComplaintListView
from views.restaurant_view import RestaurantView


class MainWindow:
    """หน้าหลักที่บรรจุแท็บต่างๆ"""
    
    def __init__(self, root: tk.Tk, controller):
        self.root = root
        self.controller = controller
        self.root.title("ระบบติดตามการร้องเรียนคุณภาพอาหาร")
        self.root.geometry("1000x600")
        
        # สร้างเมนู
        self.setup_menu()
        
        # สร้าง Notebook (Tab)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: รายการการร้องเรียน
        self.complaint_list_view = ComplaintListView(
            self.notebook, self.controller
        )
        self.notebook.add(
            self.complaint_list_view.frame, 
            text="รายการร้องเรียน"
        )
        
        # Tab 2: ร้านอาหารและโรงอาหาร
        self.restaurant_view = RestaurantView(
            self.notebook, self.controller
        )
        self.notebook.add(
            self.restaurant_view.frame,
            text="ร้านอาหาร"
        )
    
    def setup_menu(self):
        """สร้างเมนูหลัก"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ไฟล์", menu=file_menu)
        file_menu.add_command(label="ออก", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ช่วยเหลือ", menu=help_menu)
        help_menu.add_command(label="เกี่ยวกับ", command=self.show_about)
    
    def show_about(self):
        """แสดง About Dialog"""
        from tkinter import messagebox
        messagebox.showinfo(
            "เกี่ยวกับ",
            "ระบบติดตามการร้องเรียนคุณภาพอาหาร\nเวอร์ชัน 1.0\n\nMVC Design Pattern"
        )
    
    def run(self):
        """เรียกใช้หน้าต่างหลัก"""
        self.root.mainloop()
