import hashlib
import uuid
from datetime import datetime
from app.core.config import settings
import httpx

class PaymentService:
    @staticmethod
    def verify_paystack_payment(reference: str) -> dict:
        """Verify Paystack payment"""
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        
        url = f"{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}"
        
        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
            return None
        except Exception as e:
            print(f"Error verifying Paystack payment: {e}")
            return None
    
    @staticmethod
    def verify_flutterwave_payment(transaction_id: str) -> dict:
        """Verify Flutterwave payment"""
        headers = {
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"
        }
        
        url = f"{settings.FLUTTERWAVE_BASE_URL}/transactions/{transaction_id}/verify"
        
        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
            return None
        except Exception as e:
            print(f"Error verifying Flutterwave payment: {e}")
            return None
    
    @staticmethod
    def create_payment_reference() -> str:
        """Generate unique payment reference"""
        return str(uuid.uuid4())
