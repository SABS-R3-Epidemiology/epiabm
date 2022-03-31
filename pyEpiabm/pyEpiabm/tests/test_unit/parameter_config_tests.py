#
# Custom testing class to import parameters
#

import unittest
import os

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
        filepath = os.path.join(os.path.dirname(__file__),
                                os.pardir, 'testing_parameters.json')
        pe.Parameters.set_file(filepath)

    @classmethod
    def tearDownClass(cls):
        if pe.Parameters._instance:
            pe.Parameters._instance = None
