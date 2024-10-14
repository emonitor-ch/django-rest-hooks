from cryptography.fernet import Fernet

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

ENCRYPTION_KEY = getattr(settings, 'ENCRYPTION_KEY', None)


class EncryptedTextField(models.TextField):
    @property
    def fernet(self):
        if not ENCRYPTION_KEY:
            raise ImproperlyConfigured("ENCRYPTION_KEY must be set in settings")
        return Fernet(ENCRYPTION_KEY)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.fernet.decrypt(value.encode()).decode()

    def to_python(self, value):
        if value is None:
            return value
        return self.fernet.decrypt(value.encode()).decode()

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.fernet.encrypt(value.encode()).decode()
