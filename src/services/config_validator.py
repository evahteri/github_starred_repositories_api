import configuration

class ConfigValidator:
    def __init__(self):
        self.client_id = configuration.CLIENT_ID
        self.client_secret = configuration.CLIENT_SECRET

    
    def validate_secrets(self):
        self._check_type()
        if self._check_type() and self._check_length():
            return True
        return False

    def _check_type(self):
        if not isinstance(self.client_id, str) or \
            not isinstance(self.client_secret, str):
            return False
        return True
    
    def _check_length(self):
        if len(self.client_id) < 1 or len(self.client_secret) < 1:
            return False
        return True