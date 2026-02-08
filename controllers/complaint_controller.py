from models.complaint_model import ComplaintModel
from typing import List, Dict, Any, Callable


class ComplaintController:
    """Controller สำหรับจัดการ business logic ของระบบร้องเรียน"""
    
    def __init__(self, model: ComplaintModel):
        self.model = model
        self.callbacks: Dict[str, List[Callable]] = {
            'complaints_updated': [],
            'complaint_detail_updated': [],
            'responses_updated': []
        }
    
    def register_callback(self, event: str, callback: Callable):
        """ลงทะเบียน callback function สำหรับ event"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    def notify_observers(self, event: str):
        """แจ้ง observer ทั้งหมดสำหรับ event"""
        for callback in self.callbacks.get(event, []):
            callback()
    
    # ===== Canteen Operations =====
    def get_all_canteens(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลโรงอาหารทั้งหมด"""
        return self.model.get_all_canteens()
    
    def get_canteen_summary(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลโรงอาหารพร้อมจำนวนการร้องเรียน"""
        return self.model.get_canteen_summary()
    
    # ===== Stall Operations =====
    def get_all_stalls(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลร้านอาหารทั้งหมด"""
        return self.model.get_all_stalls()
    
    def get_stalls_by_canteen(self, canteen_id: str) -> List[Dict[str, Any]]:
        """ดึงร้านอาหารของโรงอาหารหนึ่ง"""
        return self.model.get_stalls_by_canteen(canteen_id)
    
    def get_stall_summary(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลร้านอาหารพร้อมจำนวนการร้องเรียน"""
        return self.model.get_stall_complaint_summary()
    
    def get_stall_name(self, stall_id: str) -> str:
        """ดึงชื่อร้านจาก ID"""
        return self.model.get_stall_name(stall_id)
    
    # ===== Complaint List Operations =====
    def get_all_complaints_sorted(self) -> List[Dict[str, Any]]:
        """ดึงข้อมูลการร้องเรียนทั้งหมดเรียงตามวันที่ล่าสุด"""
        return self.model.get_all_complaints()
    
    def get_complaints_by_stall(self, stall_id: str) -> List[Dict[str, Any]]:
        """ดึงการร้องเรียนของร้านหนึ่ง"""
        return self.model.get_complaints_by_stall(stall_id)
    
    def get_complaints_by_status(self, status: str) -> List[Dict[str, Any]]:
        """ดึงการร้องเรียนตามสถานะ"""
        return self.model.get_complaints_by_status(status)
    
    # ===== Complaint Detail Operations =====
    def get_complaint_detail(self, complaint_id: str) -> Dict[str, Any]:
        """ดึงรายละเอียดการร้องเรียน"""
        return self.model.get_complaint_by_id(complaint_id)
    
    def get_complaint_responses(self, complaint_id: str) -> List[Dict[str, Any]]:
        """ดึงการตอบกลับของการร้องเรียน"""
        return self.model.get_responses_by_complaint(complaint_id)
    
    # ===== Response Operations =====
    def submit_response(self, complaint_id: str, response_text: str) -> str:
        """ส่งการตอบกลับให้การร้องเรียน"""
        response_id = self.model.add_response(complaint_id, response_text)
        self.notify_observers('responses_updated')
        self.notify_observers('complaints_updated')
        return response_id
    
    # ===== Complaint Creation Operations =====
    def create_new_complaint(self, stall_id: str, problem_type: str, description: str) -> str:
        """เพิ่มการร้องเรียนใหม่"""
        complaint_id = self.model.add_complaint(stall_id, problem_type, description)
        self.notify_observers('complaints_updated')
        return complaint_id
