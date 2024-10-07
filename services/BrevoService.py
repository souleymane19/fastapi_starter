import os

import requests
import json
from dotenv import load_dotenv
# Charger le fichier .env
load_dotenv()


# from config import settings

class BrevoService:
    def __init__(self):
        self.EMAIL_FROM = os.getenv("EMAIL_FROM")
        self.BREVO_API_KEY = os.getenv("BREVO_API_KEY")

    def send_mail(self, to_email: str, subject: str, text_content: str):
        print(f"Email from: {self.EMAIL_FROM}")
        url = "https://api.brevo.com/v3/smtp/email"
        payload = json.dumps(
            {
                "sender": {"name": "Sourabh", "email": self.EMAIL_FROM},
                "to": [{"email": f"{to_email}"}],
                "subject": subject,
                "textContent": text_content,
            }
        )
        headers = {
            "accept": "application/json",
            "api-key": self.BREVO_API_KEY,
            "content-type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # Imprimer le code de statut et la réponse pour voir ce qui se passe
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        return response


