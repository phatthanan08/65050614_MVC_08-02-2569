import csv
import os
from datetime import datetime
from typing import List, Dict, Any


class ComplaintModel:
    """Model สำหรับจัดการข้อมูลระบบร้องเรียนอาหาร"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.canteens: List[Dict[str, Any]] = []
        self.stalls: List[Dict[str, Any]] = []
        self.complaints: List[Dict[str, Any]] = []
        self.responses: List[Dict[str, Any]] = []
        self.load_all_data()
    
    def load_all_data(self):
        """โหลดข้อมูลจากไฟล์ CSV ทั้งหมด"""
        self.load_canteens()
        self.load_stalls()
        self.load_complaints()
        self.load_responses()
    
    def load_canteens(self):
        """โหลดข้อมูลโรงอาหาร"""
        csv_path = os.path.join(self.data_dir, "canteens.csv")
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.canteens = list(reader)
    
    def load_stalls(self):
        """โหลดข้อมูลร้านอาหาร"""
        csv_path = os.path.join(self.data_dir, "stalls.csv")
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.stalls = list(reader)
    
    def load_complaints(self):
        """โหลดข้อมูลการร้องเรียน"""
        csv_path = os.path.join(self.data_dir, "complaints.csv")
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.complaints = list(reader)
                # แปลง complaint_id เป็น int
                for complaint in self.complaints:
                    complaint['complaint_id'] = complaint.get('complaint_id', '')
    
    def load_responses(self):
        """โหลดข้อมูลการตอบกลับ"""
        csv_path = os.path.join(self.data_dir, "responses.csv")
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.responses = list(reader)
    
    def save_complaints(self):
        """บันทึกข้อมูลการร้องเรียน"""
        if not self.complaints:
            return
        
        csv_path = os.path.join(self.data_dir, "complaints.csv")
        fieldnames = ['complaint_id', 'stall_id', 'complaint_date', 
                    'problem_type', 'complaint_description', 'status']
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.complaints)
    
    def save_responses(self):
        """บันทึกข้อมูลการตอบกลับ"""
        if not self.responses:
            return
        
        csv_path = os.path.join(self.data_dir, "responses.csv")
        fieldnames = ['response_id', 'complaint_id', 'response_date', 'response_text']
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.responses)
    
    # ===== Canteen Operations =====
    def get_all_canteens(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลโรงอาหารทั้งหมด"""
        return self.canteens
    
    def get_canteen_by_id(self, canteen_id: str) -> Dict[str, Any] or None:
        """ดึงข้อมูลโรงอาหารตาม ID"""
        for canteen in self.canteens:
            if canteen['canteen_id'] == canteen_id:
                return canteen
        return None
    
    # ===== Stall Operations =====
    def get_all_stalls(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลร้านอาหารทั้งหมด"""
        return self.stalls
    
    def get_stall_by_id(self, stall_id: str) -> Dict[str, Any] or None:
        """ดึงข้อมูลร้านอาหารตาม ID"""
        for stall in self.stalls:
            if stall['stall_id'] == stall_id:
                return stall
        return None
    
    def get_stalls_by_canteen(self, canteen_id: str) -> List[Dict[str, Any]]:
        """ดึงร้านอาหารตามโรงอาหาร"""
        return [s for s in self.stalls if s['canteen_id'] == canteen_id]
    
    def get_stall_name(self, stall_id: str) -> str:
        """ดึงชื่อร้านจาก stall_id"""
        stall = self.get_stall_by_id(stall_id)
        return stall['stall_name'] if stall else 'ไม่พบร้าน'
    
    # ===== Complaint Operations =====
    def get_all_complaints(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลการร้องเรียนทั้งหมดเรียงตามวันที่ล่าสุด"""
        sorted_complaints = sorted(
            self.complaints,
            key=lambda x: datetime.strptime(x['complaint_date'], '%Y-%m-%d'),
            reverse=True
        )
        return sorted_complaints
    
    def get_complaint_by_id(self, complaint_id: str) -> Dict[str, Any] or None:
        """ดึงข้อมูลการร้องเรียนตาม ID"""
        for complaint in self.complaints:
            if complaint['complaint_id'] == complaint_id:
                return complaint
        return None
    
    def get_complaints_by_stall(self, stall_id: str) -> List[Dict[str, Any]]:
        """ดึงการร้องเรียนของร้านหนึ่ง"""
        return [c for c in self.get_all_complaints() if c['stall_id'] == stall_id]
    
    def get_complaints_by_status(self, status: str) -> List[Dict[str, Any]]:
        """ดึงการร้องเรียนตามสถานะ"""
        filtered = [c for c in self.get_all_complaints() if c['status'] == status]
        return filtered
    
    def add_complaint(self, stall_id: str, problem_type: str, description: str) -> str:
        """เพิ่มการร้องเรียนใหม่"""
        new_id = f"C{len(self.complaints) + 1:03d}"
        new_complaint = {
            'complaint_id': new_id,
            'stall_id': stall_id,
            'complaint_date': datetime.now().strftime('%Y-%m-%d'),
            'problem_type': problem_type,
            'complaint_description': description,
            'status': 'รอดำเนินการ'
        }
        self.complaints.append(new_complaint)
        self.save_complaints()
        return new_id
    
    def update_complaint_status(self, complaint_id: str, status: str):
        """อัปเดตสถานะการร้องเรียน"""
        complaint = self.get_complaint_by_id(complaint_id)
        if complaint:
            complaint['status'] = status
            self.save_complaints()
    
    # ===== Response Operations =====
    def get_responses_by_complaint(self, complaint_id: str) -> List[Dict[str, Any]]:
        """ดึงการตอบกลับทั้งหมดของการร้องเรียนหนึ่ง"""
        responses = [r for r in self.responses if r['complaint_id'] == complaint_id]
        # เรียงตามวันที่
        return sorted(responses, key=lambda x: x['response_date'])
    
    def add_response(self, complaint_id: str, response_text: str, response_date: str = None) -> str:
        """เพิ่มการตอบกลับการร้องเรียน"""
        if response_date is None:
            response_date = datetime.now().strftime('%Y-%m-%d')
        
        new_response_id = f"R{len(self.responses) + 1:03d}"
        new_response = {
            'response_id': new_response_id,
            'complaint_id': complaint_id,
            'response_date': response_date,
            'response_text': response_text
        }
        self.responses.append(new_response)
        self.save_responses()
        
        # อัปเดตสถานะเป็น "ดำเนินการแล้ว"
        self.update_complaint_status(complaint_id, 'ดำเนินการแล้ว')
        
        return new_response_id
    
    # ===== Statistics Operations =====
    def get_stall_complaint_summary(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลร้านทั้งหมด และจำนวนการร้องเรียนแต่ละสัถานะ"""
        # เริ่มจากร้านทั้งหมด (0 ร้องเรียน)
        stall_stats = {}
        for stall in self.stalls:
            stall_id = stall['stall_id']
            stall_stats[stall_id] = {
                'stall_id': stall_id,
                'stall_name': stall['stall_name'],
                'complaint_count': 0,
                'status_count': {'รอดำเนินการ': 0, 'ดำเนินการแล้ว': 0}
            }
        
        # เพิ่มจำนวนร้องเรียน
        for complaint in self.complaints:
            stall_id = complaint['stall_id']
            if stall_id in stall_stats:
                stall_stats[stall_id]['complaint_count'] += 1
                status = complaint['status']
                if status in stall_stats[stall_id]['status_count']:
                    stall_stats[stall_id]['status_count'][status] += 1
        
        # เรียงตามจำนวนการร้องเรียนมากไปน้อย
        return sorted(stall_stats.values(), key=lambda x: x['complaint_count'], reverse=True)
    
    def get_canteen_summary(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลโรงอาหารทั้งหมด และจำนวนการร้องเรียน"""
        # เริ่มจากโรงอาหารทั้งหมด (0 ร้องเรียน)
        canteen_stats = {}
        for canteen in self.canteens:
            canteen_id = canteen['canteen_id']
            canteen_stats[canteen_id] = {
                'canteen_id': canteen_id,
                'canteen_name': canteen['canteen_name'],
                'location': canteen['location'],
                'complaint_count': 0
            }
        
        # นับจำนวนร้องเรียนจากแต่ละโรงอาหาร
        for complaint in self.complaints:
            stall = self.get_stall_by_id(complaint['stall_id'])
            if stall:
                canteen_id = stall['canteen_id']
                if canteen_id in canteen_stats:
                    canteen_stats[canteen_id]['complaint_count'] += 1
        
        return sorted(canteen_stats.values(), key=lambda x: x['complaint_count'], reverse=True)
