# core/provisioning_service.py

import secrets
import string

from django.conf import settings
from django.db import transaction

from core.models import HostingAccount
from core.whm_service import whm


class ProvisioningService:
    """
    Handles automatic hosting account provisioning.
    """

    def generate_username(self, domain):
        """
        Generate a valid cPanel username.

        Rules:
        - max 8 characters
        - starts with a letter
        - letters/numbers only
        """

        base = domain.split(".")[0].lower()

        base = "".join(c for c in base if c.isalnum())

        if not base:
            base = "host"

        if not base[0].isalpha():
            base = "h" + base

        base = base[:6]

        while True:
            suffix = "".join(secrets.choice(string.digits) for _ in range(2))
            username = f"{base}{suffix}"

            if not HostingAccount.objects.filter(
                cpanel_username=username
            ).exists():
                return username

    def generate_password(self):
        """
        Generate a strong password.
        """
        alphabet = (
            string.ascii_letters
            + string.digits
            + "!@#$%^&*"
        )

        return "".join(
            secrets.choice(alphabet)
            for _ in range(18)
        )

    @transaction.atomic
    def provision_hosting(
        self,
        *,
        user,
        order,
        hosting_plan,
        domain,
    ):
        """
        Create a WHM/cPanel account and save it locally.
        """

        username = self.generate_username(domain)
        password = self.generate_password()

        response = whm.create_account(
            domain=domain,
            username=username,
            password=password,
            email=user.email,
            package=hosting_plan.whm_package,
        )

        if response.get("metadata", {}).get("result") != 1:
            return {
                "success": False,
                "error": response.get("metadata", {}).get(
                    "reason",
                    "WHM provisioning failed."
                ),
                "response": response,
            }

        account = HostingAccount.objects.create(
            user=user,
            order=order,
            plan=hosting_plan,
            domain=domain,
            cpanel_username=username,
            cpanel_login_url=f"{settings.WHM_HOST.replace(':2087', ':2083')}",
            status="active",
        )

        return {
            "success": True,
            "account": account,
            "username": username,
            "password": password,
            "response": response,
        }


provisioning = ProvisioningService()