import tkinter as tk
from tkinter import ttk, messagebox


class ReplyView:
    """View สำหรับป้อนการตอบกลับการร้องเรียน"""
    
    def __init__(self, parent, controller, complaint_id, callback=None):
        self.controller = controller
        self.parent = parent
        self.complaint_id = complaint_id
        self.callback = callback
        
        # สร้าง UI
        self.setup_ui()
    
    def setup_ui(self):
        """สร้าง UI สำหรับตอบกลับ"""
        # Title Frame
        title_frame = ttk.Frame(self.parent)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            title_frame,
            text=f"ป้อนการตอบกลับสำหรับการร้องเรียน ID: {self.complaint_id}",
            font=('TkDefaultFont', 11, 'bold')
        ).pack(anchor=tk.W)
        
        # Text Frame
        text_frame = ttk.LabelFrame(self.parent, text="ข้อความตอบกลับ", padding=10)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Text Widget
        self.text_widget = tk.Text(text_frame, height=10, wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Button Frame
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            button_frame,
            text="ส่ง",
            command=self.submit_reply
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="ยกเลิก",
            command=self.parent.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # โฟกัสไปยังช่องข้อความ
        self.text_widget.focus()
    
    def submit_reply(self):
        """ส่งการตอบกลับ"""
        reply_text = self.text_widget.get(1.0, tk.END).strip()
        
        if not reply_text:
            messagebox.showwarning("แจ้งเตือน", "กรุณาป้อนข้อความตอบกลับ")
            return
        
        # บันทึกการตอบกลับผ่าน Controller
        try:
            self.controller.submit_response(self.complaint_id, reply_text)
            messagebox.showinfo("สำเร็จ", "ส่งการตอบกลับเรียบร้อย")
            
            # เรียก callback ถ้ามี
            if self.callback:
                self.callback()
            
            self.parent.destroy()
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {str(e)}")
