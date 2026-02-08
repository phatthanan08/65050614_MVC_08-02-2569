import tkinter as tk
from tkinter import ttk


class RestaurantView:
    """View แสดงข้อมูลร้านอาหารและจำนวนการร้องเรียน"""
    
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        
        # สร้างเฟรมหลัก
        self.frame = ttk.Frame(parent)
        
        # สร้าง Notebook สำหรับแยก Tab
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: ร้านอาหาร
        self.setup_stalls_tab()
        
        # Tab 2: โรงอาหาร
        self.setup_canteens_tab()
        
        # ลงทะเบียน callback
        self.controller.register_callback('complaints_updated', self.refresh_all)
    
    def setup_stalls_tab(self):
        """สร้าง Tab สำหรับร้านอาหาร"""
        stall_frame = ttk.Frame(self.notebook)
        self.notebook.add(stall_frame, text="ร้านอาหาร")
        
        # Toolbar
        toolbar = ttk.Frame(stall_frame)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        ttk.Button(toolbar, text="รีเฟรช", command=self.refresh_stalls).pack(side=tk.LEFT, padx=5)
        
        # Table Frame
        table_frame = ttk.Frame(stall_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview สำหรับร้านอาหาร
        columns = ('ID', 'ร้านอาหาร', 'จำนวนร้องเรียน', 'รอดำเนินการ', 'ดำเนินการแล้ว')
        self.stall_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # กำหนดหัวตาราง
        self.stall_tree.column('ID', width=50, anchor=tk.CENTER)
        self.stall_tree.column('ร้านอาหาร', width=200, anchor=tk.W)
        self.stall_tree.column('จำนวนร้องเรียน', width=100, anchor=tk.CENTER)
        self.stall_tree.column('รอดำเนินการ', width=100, anchor=tk.CENTER)
        self.stall_tree.column('ดำเนินการแล้ว', width=100, anchor=tk.CENTER)
        
        for col in columns:
            self.stall_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.stall_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stall_tree.configure(yscroll=scrollbar.set)
        self.stall_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind click event
        self.stall_tree.bind('<Button-1>', self.on_stall_selected)
        
        self.refresh_stalls()
    
    def setup_canteens_tab(self):
        """สร้าง Tab สำหรับโรงอาหาร"""
        canteen_frame = ttk.Frame(self.notebook)
        self.notebook.add(canteen_frame, text="โรงอาหาร")
        
        # Toolbar
        toolbar = ttk.Frame(canteen_frame)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        ttk.Button(toolbar, text="รีเฟรช", command=self.refresh_canteens).pack(side=tk.LEFT, padx=5)
        
        # Table Frame
        table_frame = ttk.Frame(canteen_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview สำหรับโรงอาหาร
        columns = ('ID', 'โรงอาหาร', 'ตำแหน่ง', 'จำนวนร้องเรียน')
        self.canteen_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # กำหนดหัวตาราง
        self.canteen_tree.column('ID', width=60, anchor=tk.CENTER)
        self.canteen_tree.column('โรงอาหาร', width=200, anchor=tk.W)
        self.canteen_tree.column('ตำแหน่ง', width=200, anchor=tk.W)
        self.canteen_tree.column('จำนวนร้องเรียน', width=120, anchor=tk.CENTER)
        
        for col in columns:
            self.canteen_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.canteen_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canteen_tree.configure(yscroll=scrollbar.set)
        self.canteen_tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_canteens()
    
    def refresh_stalls(self):
        """อัปเดตตารางร้านอาหาร"""
        for item in self.stall_tree.get_children():
            self.stall_tree.delete(item)
        
        stalls = self.controller.get_stall_summary()
        
        for stall in stalls:
            self.stall_tree.insert('', tk.END, values=(
                stall['stall_id'],
                stall['stall_name'],
                stall['complaint_count'],
                stall['status_count']['รอดำเนินการ'],
                stall['status_count']['ดำเนินการแล้ว']
            ))
    
    def refresh_canteens(self):
        """อัปเดตตารางโรงอาหาร"""
        for item in self.canteen_tree.get_children():
            self.canteen_tree.delete(item)
        
        canteens = self.controller.get_canteen_summary()
        
        for canteen in canteens:
            self.canteen_tree.insert('', tk.END, values=(
                canteen['canteen_id'],
                canteen['canteen_name'],
                canteen['location'],
                canteen['complaint_count']
            ))
    
    def refresh_all(self):
        """รีเฟรชทุกตาราง"""
        self.refresh_stalls()
        self.refresh_canteens()
    
    def on_stall_selected(self, event):
        """เมื่อเลือกร้านอาหาร"""
        selection = self.stall_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.stall_tree.item(item, 'values')
        stall_id = values[0]
        stall_name = values[1]
        
        # สร้างหน้าต่างแสดงรายละเอียด
        detail_window = tk.Toplevel(self.parent)
        detail_window.title(f"การร้องเรียนของ {stall_name}")
        detail_window.geometry("700x400")
        
        # แสดงรายการการร้องเรียน
        columns = ('ID', 'วันที่', 'ประเด็นปัญหา', 'สถานะ')
        tree = ttk.Treeview(detail_window, columns=columns, show='headings')
        
        tree.column('ID', width=60, anchor=tk.CENTER)
        tree.column('วันที่', width=100, anchor=tk.CENTER)
        tree.column('ประเด็นปัญหา', width=250, anchor=tk.W)
        tree.column('สถานะ', width=120, anchor=tk.CENTER)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ดึงการร้องเรียน
        complaints = self.controller.get_complaints_by_stall(stall_id)
        
        for complaint in complaints:
            tree.insert('', tk.END, values=(
                complaint['complaint_id'],
                complaint['complaint_date'],
                complaint['problem_type'],
                complaint['status']
            ))
