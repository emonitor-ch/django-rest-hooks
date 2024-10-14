class EncryptedTextField(models.TextField):
    @property
    def fernet(self):
        if not hasattr(settings, 'ENCRYPTION_KEY'):
            raise ImproperlyConfigured("ENCRYPTION_KEY must be set in settings")
        return Fernet(settings.ENCRYPTION_KEY)

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
