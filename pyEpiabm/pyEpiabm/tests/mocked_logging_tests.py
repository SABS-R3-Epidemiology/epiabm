#
# Custom testing class to patching logging
#

import unittest
from unittest.mock import patch


class TestMockedLogs(unittest.TestCase):
    """Inherits from the default unittest class, but
    with mocked logging functions to prevent printing"""
    @classmethod
    def setUpClass(cls):
        """Inherits from the unittest setup, and patches the warning
        and error logging classes, that otherwise print to terminal
        """
        super(TestMockedLogs, cls).setUpClass()
        cls.warning_patcher = patch('logging.warning')
        cls.error_patcher = patch('logging.error')

        cls.warning_patcher.start()
        cls.error_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Inherits from the unittest teardown, and remove all patches"""
        super(TestMockedLogs, cls).tearDownClass()
        cls.warning_patcher.stop()
        cls.error_patcher.stop()
