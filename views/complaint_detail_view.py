import tkinter as tk
from tkinter import ttk, messagebox


class ComplaintDetailView:
    """View แสดงรายละเอียดการร้องเรียน"""
    
    def __init__(self, parent, controller, complaint_id):
        self.controller = controller
        self.parent = parent
        self.complaint_id = complaint_id
        
        # ดึงข้อมูลการร้องเรียน
        self.complaint = self.controller.get_complaint_detail(complaint_id)
        
        if not self.complaint:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบการร้องเรียน")
            parent.destroy()
            return
        
        # สร้าง UI
        self.setup_ui()
    
    def setup_ui(self):
        """สร้าง UI สำหรับรายละเอียด"""
        # Top Frame สำหรับข้อมูลพื้นฐาน
        info_frame = ttk.LabelFrame(self.parent, text="ข้อมูลการร้องเรียน", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # แถวที่ 1: ID และร้านอาหาร
        stall_name = self.controller.get_stall_name(self.complaint['stall_id'])
        ttk.Label(info_frame, text=f"ID: {self.complaint['complaint_id']}").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Label(info_frame, text=f"ร้านอาหาร: {stall_name}").grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5
        )
        
        # แถวที่ 2: วันที่และสถานะ
        ttk.Label(info_frame, text=f"วันที่: {self.complaint['complaint_date']}").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Label(info_frame, text=f"สถานะ: {self.complaint['status']}").grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5
        )
        
        # แถวที่ 3: ประเด็นปัญหา
        ttk.Label(info_frame, text=f"ประเด็นปัญหา: {self.complaint['problem_type']}").grid(
            row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5
        )
        
        # Frame สำหรับรายละเอียดการร้องเรียน
        detail_frame = ttk.LabelFrame(self.parent, text="รายละเอียดการร้องเรียน", padding=10)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        detail_text = tk.Text(detail_frame, height=5, state=tk.DISABLED)
        detail_text.pack(fill=tk.BOTH, expand=True)
        
        detail_text.config(state=tk.NORMAL)
        detail_text.insert(1.0, self.complaint['complaint_description'])
        detail_text.config(state=tk.DISABLED)
        
        # Frame สำหรับการตอบกลับ
        responses_frame = ttk.LabelFrame(self.parent, text="การตอบกลับ", padding=10)
        responses_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ดึงการตอบกลับ
        responses = self.controller.get_complaint_responses(self.complaint_id)
        
        if responses:
            for response in responses:
                response_text = f"[{response['response_date']}] - {response['response_text']}"
                ttk.Label(
                    responses_frame,
                    text=response_text,
                    wraplength=600,
                    justify=tk.LEFT,
                    foreground="blue"
                ).pack(anchor=tk.W, pady=5)
        else:
            ttk.Label(responses_frame, text="ยังไม่มีการตอบกลับ", foreground="gray").pack(
                anchor=tk.W, pady=5
            )
        
        # Bottom Frame สำหรับปุ่ม
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # ปุ่มตอบกลับ (สามารถตอบกลับได้หลายครั้ง ไม่ว่าสถานะจะเป็นอะไร)
        ttk.Button(
            button_frame,
            text="ตอบกลับ",
            command=self.show_reply_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="ปิด",
            command=self.parent.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def show_reply_dialog(self):
        """แสดง Dialog สำหรับป้อนการตอบกลับ"""
        from views.reply_view import ReplyView
        
        reply_window = tk.Toplevel(self.parent)
        reply_window.title("ตอบกลับการร้องเรียน")
        reply_window.geometry("500x300")
        
        reply_view = ReplyView(
            reply_window,
            self.controller,
            self.complaint_id,
            callback=self.on_reply_submitted
        )
    
    def on_reply_submitted(self):
        """เก็บเมื่อการตอบกลับถูกส่ง"""
        messagebox.showinfo("สำเร็จ", "ส่งการตอบกลับเรียบร้อย")
        self.parent.destroy()
