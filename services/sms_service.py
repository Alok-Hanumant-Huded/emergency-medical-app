from datetime import datetime


class SMSService:
    """Simple SMS abstraction designed for demo use.

    In production, this class can be replaced with Twilio or another provider.
    """

    def __init__(self):
        self.provider = "demo"
        self.logs = []

    def send_alert(self, patient_name, contact_name, contact_phone, risk_level, location_link):
        message = (
            "🚨 EMERGENCY ALERT\n\n"
            f"{patient_name} has activated emergency assistance.\n\n"
            f"Possible emergency level: {risk_level}\n\n"
            "Location:\n"
            f"{location_link}\n\n"
            "Please contact the person immediately.\n\n"
            "This is an automated emergency alert from the Emergency Medical Assistance System."
        )

        log = {
            "contact_name": contact_name,
            "contact_phone": contact_phone,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "SIMULATED",
        }
        self.logs.append(log)
        return log


sms_service = SMSService()
