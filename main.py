"""
ระบบติดตามการร้องเรียนคุณภาพอาหาร
Entry Point ของแอปพลิเคชัน
"""

import tkinter as tk
import sys
import os

# เพิ่ม path สำหรับ import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.complaint_model import ComplaintModel
from controllers.complaint_controller import ComplaintController
from views.main_window import MainWindow


def main():
    """ฟังก์ชันหลักเพื่อเรียกใช้แอปพลิเคชัน"""
    # สร้าง Model
    model = ComplaintModel(data_dir="data")
    
    # สร้าง Controller
    controller = ComplaintController(model)
    
    # สร้าง Main Window
    root = tk.Tk()
    app = MainWindow(root, controller)
    
    # เรียกใช้แอปพลิเคชัน
    app.run()


if __name__ == "__main__":
    main()
