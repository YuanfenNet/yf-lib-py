import unittest
from unittest.mock import Mock, patch

import requests

from yuanfen import ErrorResponse, SuccessResponse, Version, ip


class SmokeTests(unittest.TestCase):
    def test_response_models(self):
        self.assertEqual(SuccessResponse(data={"id": 1}).model_dump(), {"code": 0, "message": "SUCCESS", "data": {"id": 1}})
        self.assertEqual(ErrorResponse().code, 1000)

    def test_version_comparison(self):
        self.assertEqual(Version.parse("1.2.3").compare("1.2.4"), -1)
        self.assertEqual(Version(1, 2, 3).compare({"major": 1, "minor": 2, "patch": 3}), 0)

    @patch("yuanfen.ip.requests.get")
    def test_public_ip_fallback(self, get):
        get.side_effect = [requests.Timeout(), Mock(text=" 1.2.3.4 ")]
        self.assertEqual(ip.get_public_ip(), "1.2.3.4")


if __name__ == "__main__":
    unittest.main()
