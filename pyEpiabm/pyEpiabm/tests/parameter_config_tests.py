#
# Custom testing class to import parameters
#

import unittest

import pyEpiabm as pe


class TestPyEpiabm(unittest.TestCase):
    """Inherits from the default unittest class, but
    also sets up parameters config file for use in testing"""
    @classmethod
    def setUpClass(cls):
        """Inherits from the unittest setup, and patches the warning
        and error logging classes, that otherwise print to terminal
        """
        super(TestPyEpiabm, cls).setUpClass()
        pe.Parameters.set_file("pyEpiabm/pyEpiabm/tests/"
                               + "testing_parameters.json")

    @classmethod
    def tearDownClass(cls):
        if pe.Parameters._instance:
            pe.Parameters._instance = None
