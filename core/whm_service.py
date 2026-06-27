import requests
from django.conf import settings
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class WHMService:
    def __init__(self):
        self.host = settings.WHM_HOST.rstrip("/")
        self.username = settings.WHM_USERNAME
        self.token = settings.WHM_API_TOKEN

        self.headers = {
            "Authorization": f"whm {self.username}:{self.token}"
        }

    def _request(self, endpoint, params=None):
        """
        Make a request to the WHM API.
        """
        try:
            url = f"{self.host}/json-api/{endpoint}"

            if params is None:
                params = {}

            params["api.version"] = 1

            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=False,
                timeout=30,
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    # ----------------------------
    # Packages
    # ----------------------------

    def list_packages(self):
        return self._request("listpkgs")

    # ----------------------------
    # Accounts
    # ----------------------------

    def create_account(
        self,
        domain,
        username,
        password,
        email,
        package,
    ):
        return self._request(
            "createacct",
            {
                "domain": domain,
                "username": username,
                "password": password,
                "contactemail": email,
                "plan": package,
            },
        )

    def suspend_account(self, username, reason="Suspended"):
        return self._request(
            "suspendacct",
            {
                "user": username,
                "reason": reason,
            },
        )

    def unsuspend_account(self, username):
        return self._request(
            "unsuspendacct",
            {
                "user": username,
            },
        )

    def terminate_account(self, username):
        return self._request(
            "removeacct",
            {
                "user": username,
            },
        )

    def change_package(self, username, package):
        return self._request(
            "changepackage",
            {
                "user": username,
                "pkg": package,
            },
        )

    # ----------------------------
    # Account Information
    # ----------------------------

    def account_summary(self, username):
        return self._request(
            "accountsummary",
            {
                "user": username,
            },
        )

    def list_accounts(self):
        return self._request("listaccts")

    def list_resellers(self):
        return self._request("listresellers")


whm = WHMService()