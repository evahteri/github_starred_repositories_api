import unittest
from services.config_validator import ConfigValidator


class TestConfigValidator(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_config(self):
        empty_client_id_str = ""
        empty_client_secret_str = ""
        config_validator = ConfigValidator(
            empty_client_id_str, empty_client_secret_str)
        self.assertEqual(config_validator.validate_secrets(), False)

    def test_invalid_type_config(self):
        client_id_int = 123
        client_secret_int = 321
        config_validator = ConfigValidator(client_id_int, client_secret_int)
        self.assertEqual(config_validator.validate_secrets(), False)

    def test_valid_config(self):
        client_id_str = "jk21jbop122"
        client_secret_str = "k1l2mö012nk21nkn"
        config_validator = ConfigValidator(client_id_str, client_secret_str)
        self.assertEqual(config_validator.validate_secrets(), True)
