#
# Custom testing class to patching logging
#

from unittest.mock import patch

from .parameter_config_tests import TestPyEpiabm


class TestMockedLogs(TestPyEpiabm):
    """Inherits from the custom testing function, which is
    the unittest.TestCase class with a parameters file bolted
    on, but with mocked logging functions to prevent printing

    """
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
