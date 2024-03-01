class ConfigValidator:
    """Class to validate the configuration file to avoid runtime errors
    """
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def validate_secrets(self) -> bool:
        """Returns True if configuration is valid, False otherwise.
        """
        self._check_type()
        if self._check_type() and self._check_length():
            return True
        return False

    def _check_type(self) -> bool:
        """The client_id and client_secret must be strings.
        """

        if not isinstance(self.client_id, str) or \
                not isinstance(self.client_secret, str):
            return False
        return True

    def _check_length(self) -> bool:
        """If the client_id and client_secret are empty, the configuration is invalid.
        """
        if len(self.client_id) < 1 or len(self.client_secret) < 1:
            return False
        return True
