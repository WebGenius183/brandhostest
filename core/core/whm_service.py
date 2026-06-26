import requests
import json
from django.conf import settings
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings (WHM uses self-signed certs)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class WHMService:
    def __init__(self):
        self.host = settings.WHM_HOST
        self.token = settings.WHM_API_TOKEN
        self.username = settings.WHM_USERNAME
        self.headers = {
            'Authorization': f'whm {self.username}:{self.token}',
            'Content-Type': 'application/json'
        }
    
    def create_account(self, domain, username, password, plan_name):
        """Create hosting account in WHM"""
        try:
            url = f"{self.host}/json-api/cpanel"
            
            payload = {
                'cpanel_jsonapi_user': self.username,
                'cpanel_jsonapi_module': 'CPanel',
                'cpanel_jsonapi_func': 'addacct',
                'domain': domain,
                'username': username,
                'password': password,
                'plan': plan_name,
                'contactemail': 'admin@yourdomain.com',
            }
            
            response = requests.post(
                url,
                data=payload,
                headers=self.headers,
                verify=False,
                timeout=30
            )
            
            result = response.json()
            
            if result.get('cpanelresult', {}).get('status') == 1:
                return {
                    'success': True,
                    'message': 'Account created successfully',
                    'data': result
                }
            else:
                return {
                    'success': False,
                    'message': result.get('cpanelresult', {}).get('statusmsg', 'Unknown error')
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def suspend_account(self, username, reason=''):
        """Suspend hosting account"""
        try:
            url = f"{self.host}/json-api/cpanel"
            
            payload = {
                'cpanel_jsonapi_user': self.username,
                'cpanel_jsonapi_module': 'CPanel',
                'cpanel_jsonapi_func': 'suspendacct',
                'user': username,
                'reason': reason or 'Suspended by customer request',
            }
            
            response = requests.post(
                url,
                data=payload,
                headers=self.headers,
                verify=False,
                timeout=30
            )
            
            return response.json()
            
        except Exception as e:
            return {'error': str(e)}
    
    def unsuspend_account(self, username):
        """Unsuspend hosting account"""
        try:
            url = f"{self.host}/json-api/cpanel"
            
            payload = {
                'cpanel_jsonapi_user': self.username,
                'cpanel_jsonapi_module': 'CPanel',
                'cpanel_jsonapi_func': 'unsuspendacct',
                'user': username,
            }
            
            response = requests.post(
                url,
                data=payload,
                headers=self.headers,
                verify=False,
                timeout=30
            )
            
            return response.json()
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_account_info(self, username):
        """Get account information"""
        try:
            url = f"{self.host}/json-api/cpanel"
            
            payload = {
                'cpanel_jsonapi_user': self.username,
                'cpanel_jsonapi_module': 'CPanel',
                'cpanel_jsonapi_func': 'accountsummary',
                'user': username,
            }
            
            response = requests.post(
                url,
                data=payload,
                headers=self.headers,
                verify=False,
                timeout=30
            )
            
            return response.json()
            
        except Exception as e:
            return {'error': str(e)}
    
    def list_plans(self):
        """List all hosting plans in WHM"""
        try:
            url = f"{self.host}/json-api/cpanel"
            
            payload = {
                'cpanel_jsonapi_user': self.username,
                'cpanel_jsonapi_module': 'CPanel',
                'cpanel_jsonapi_func': 'listplans',
            }
            
            response = requests.post(
                url,
                data=payload,
                headers=self.headers,
                verify=False,
                timeout=30
            )
            
            return response.json()
            
        except Exception as e:
            return {'error': str(e)}

# Initialize service
whm = WHMService()
