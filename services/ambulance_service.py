import uuid

from models.models import AmbulanceRequest


class AmbulanceService:
    """Simulated ambulance workflow for demo/prototype purposes."""

    @staticmethod
    def create_request(emergency):
        request_id = f"AMB-{uuid.uuid4().hex[:8].upper()}"
        ambulance_request = AmbulanceRequest(
            emergency_id=emergency.id,
            request_id=request_id,
            status="REQUEST RECEIVED",
        )
        return ambulance_request

    @staticmethod
    def get_status_options():
        return [
            "REQUEST RECEIVED",
            "AMBULANCE ASSIGNED",
            "AMBULANCE ON THE WAY",
            "ARRIVED",
            "COMPLETED",
        ]

    @staticmethod
    def update_status(request, new_status):
        if new_status in AmbulanceService.get_status_options():
            request.status = new_status
            return True
        return False


ambulance_service = AmbulanceService()
