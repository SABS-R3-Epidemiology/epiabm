import unittest
import pyEpiabm as pe
from unittest.mock import patch, MagicMock


class TestSimulation(unittest.TestCase):
    """Tests the 'Simulation' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.pop_factory = pe.ToyPopulationFactory()
        cls.test_population = cls.pop_factory.make_pop(0, 1, 1, 1)
        pe.Parameters.instance().time_steps_per_day = 1
        cls.sim_params = {"simulation_start_time": 0,
                          "simulation_end_time": 1,
                          "initial_infected_number": 5}

        cls.file_params = {"output_file": "output.csv",
                           "output_dir": "python_examples/simulation_outputs"}

        cls.initial_sweeps = [pe.InitialInfectedSweep()]
        cls.sweeps = [pe.PlaceSweep()]

    def test_configure(self):
        initial_sweeps = [0.5]
        test_sim = pe.Simulation()
        # Test assertion raised when sweep lists don't contain sweeps.
        self.assertRaises(AssertionError, test_sim.configure,
                          self.test_population, initial_sweeps,
                          self.sweeps, self.sim_params, self.file_params)
        # Test configure binds parameters as expected.
        test_sim.configure(self.test_population, self.initial_sweeps,
                           self.sweeps, self.sim_params, self.file_params)
        self.assertEqual(len(test_sim.initial_sweeps), 1)
        self.assertEqual(len(test_sim.sweeps), 1)
        self.assertIsInstance(test_sim.population, pe.Population)
        self.assertIsInstance(test_sim.writer, pe._CsvDictWriter)

    def test_run_sweeps(self):
        initial_sweep = MagicMock()
        sweep = MagicMock()
        initial_sweep.return_value = 0
        sweep.return_value = 0
        time = self.sim_params["simulation_end_time"] - 1
        test_sim = pe.Simulation()
        test_sim.configure(self.test_population, initial_sweep,
                           sweep, self.sim_params, self.file_params)
        with patch.object(test_sim, 'write_to_file') as mock:
            test_sim.run_sweeps()
            mock.assert_called_with(time)

    def test_write_to_file(self):
        time = 1
        test_sim = pe.Simulation()
        test_sim.configure(self.test_population, self.initial_sweeps,
                           self.sweeps, self.sim_params, self.file_params)
        data = {s: 0 for s in list(pe.InfectionStatus)}
        data["time"] = time
        with patch.object(test_sim.writer, 'write') as mock:
            test_sim.write_to_file(time)
            mock.assert_called_with(data)


if __name__ == '__main__':
    unittest.main()
