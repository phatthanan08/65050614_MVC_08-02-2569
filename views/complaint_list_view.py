import tkinter as tk
from tkinter import ttk, messagebox
from views.complaint_detail_view import ComplaintDetailView


class ComplaintListView:
    """View แสดงรายการการร้องเรียนทั้งหมด (เรียงตามวันที่)"""
    
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        self.current_selected_complaint = None
        
        # สร้างเฟรมหลัก
        self.frame = ttk.Frame(parent)
        
        # สร้าง Toolbar
        self.setup_toolbar()
        
        # สร้าง Main Frame สำหรับตาราง
        self.setup_table()
        
        # ลงทะเบียน callback
        self.controller.register_callback('complaints_updated', self.refresh_table)
    
    def setup_toolbar(self):
        """สร้าง toolbar ด้านบน"""
        toolbar_frame = ttk.Frame(self.frame)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # ป้ายกำกับสำหรับตัวกรอง
        ttk.Label(toolbar_frame, text="สถานะ:").pack(side=tk.LEFT, padx=5)
        
        # Combobox สำหรับเลือกสถานะ
        self.status_var = tk.StringVar(value="ทั้งหมด")
        self.status_combo = ttk.Combobox(
            toolbar_frame,
            textvariable=self.status_var,
            values=["ทั้งหมด", "รอดำเนินการ", "ดำเนินการแล้ว"],
            state="readonly",
            width=15
        )
        self.status_combo.pack(side=tk.LEFT, padx=5)
        self.status_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())
        
        # ปุ่ม Refresh
        ttk.Button(toolbar_frame, text="รีเฟรช", command=self.refresh_table).pack(side=tk.LEFT, padx=5)
    
    def setup_table(self):
        """สร้างตารางแสดงการร้องเรียน"""
        # สร้าง Frame สำหรับตาราง
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # สร้าง Treeview (ตาราง)
        columns = ('ID', 'ร้านอาหาร', 'วันที่', 'ประเด็นปัญหา', 'สถานะ')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=15,
            show='headings'
        )
        
        # กำหนดหัวตาราง
        self.tree.column('ID', width=60, anchor=tk.CENTER)
        self.tree.column('ร้านอาหาร', width=150, anchor=tk.W)
        self.tree.column('วันที่', width=100, anchor=tk.CENTER)
        self.tree.column('ประเด็นปัญหา', width=150, anchor=tk.W)
        self.tree.column('สถานะ', width=100, anchor=tk.CENTER)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('ร้านอาหาร', text='ร้านอาหาร')
        self.tree.heading('วันที่', text='วันที่')
        self.tree.heading('ประเด็นปัญหา', text='ประเด็นปัญหา')
        self.tree.heading('สถานะ', text='สถานะ')
        
        # ผูก Double-Click event
        self.tree.bind('<Double-1>', self.on_complaint_selected)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # สร้าง Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Bottom Frame สำหรับปุ่ม
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="ดูรายละเอียด",
            command=self.show_detail
        ).pack(side=tk.LEFT, padx=5)
        
        # โหลดข้อมูลครั้งแรก
        self.refresh_table()
    
    def refresh_table(self):
        """อัปเดตตารางด้วยข้อมูลล่าสุด"""
        # ลบข้อมูลเก่า
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # ดึงข้อมูลตามสถานะที่เลือก
        status = self.status_var.get()
        if status == "ทั้งหมด":
            complaints = self.controller.get_all_complaints_sorted()
        else:
            complaints = self.controller.get_complaints_by_status(status)
        
        # เพิ่มข้อมูลลงตาราง
        for complaint in complaints:
            stall_name = self.controller.get_stall_name(complaint['stall_id'])
            self.tree.insert('', tk.END, values=(
                complaint['complaint_id'],
                stall_name,
                complaint['complaint_date'],
                complaint['problem_type'],
                complaint['status']
            ))
    
    def on_complaint_selected(self, event):
        """เมื่อผู้ใช้คลิกที่แถว"""
        self.show_detail()
    
    def show_detail(self):
        """แสดงรายละเอียดของการร้องเรียนที่เลือก"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกการร้องเรียน")
            return
        
        # ดึง ID จากแถวที่เลือก
        item = selection[0]
        values = self.tree.item(item, 'values')
        complaint_id = values[0]
        
        # สร้าง Top-level Window สำหรับรายละเอียด
        detail_window = tk.Toplevel(self.parent)
        detail_window.title(f"รายละเอียดการร้องเรียน {complaint_id}")
        detail_window.geometry("700x500")
        
        # สร้าง ComplaintDetailView ในหน้าต่างใหม่
        detail_view = ComplaintDetailView(detail_window, self.controller, complaint_id)
