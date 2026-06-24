import requests
from django.conf import settings

class TrueHostService:
    def __init__(self):
        self.api_key = settings.TRUEHOST_API_KEY
        self.api_username = settings.TRUEHOST_API_USERNAME
        self.api_url = settings.TRUEHOST_API_URL
        
    def check_domain(self, domain, tld):
        try:
            response = requests.post(f"{self.api_url}api.php", {
                'action': 'check_domain',
                'domain': domain + tld,
                'api_key': self.api_key,
                'api_username': self.api_username,
            }, timeout=5)
            return response.json().get('available') == 1
        except:
            return False
    
    def register_domain(self, domain, tld, user_data):
        try:
            response = requests.post(f"{self.api_url}api.php", {
                'action': 'register_domain',
                'domain': domain + tld,
                'years': 1,
                'firstname': user_data['first_name'],
                'lastname': user_data['last_name'],
                'email': user_data['email'],
                'api_key': self.api_key,
                'api_username': self.api_username,
            }, timeout=10)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

truehost = TrueHostService()
