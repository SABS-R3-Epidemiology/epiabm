#
# Sweep to record demographic information of the population in a .csv file
#

import os
import typing

from pyEpiabm.output import _CsvDictWriter

from .abstract_sweep import AbstractSweep


class InitialDemographicsSweep(AbstractSweep):
    """Class to sweep through the population at the beginning of the simulation
    and record their demographic information

    """

    def __init__(self, file_params: typing.Dict):
        """Initiate file parameters referring to the file location and
        which columns are to be included

        file_params Contains:
            * `output_dir`: String for the location of the output file, \
               as a relative path
            * `spatial_output`: Boolean to determine whether a spatial output \
               should be used
            * `age_output`: Boolean to determine whether the output will \
                have ages

        """
        if "output_dir" not in file_params:
            raise ValueError("output_dir must be specified in file_params")
        self.spatial_output = file_params["spatial_output"] \
            if "spatial_output" in file_params else False
        self.age_output = file_params["age_output"] \
            if "age_output" in file_params else False

        # Here we set up the writer
        folder = os.path.join(os.getcwd(),
                              file_params["output_dir"])
        file_name = "demographics.csv"
        self.titles = ["id"]
        if self.age_output:
            self.titles.append("age_group")
        if self.spatial_output:
            self.titles += ["location_x", "location_y"]
        self.titles.append("kw_or_chr")
        self.writer = _CsvDictWriter(
            folder, file_name, self.titles)

    def __call__(self, *args):
        """During the initial sweeps, this will be called, and will loop
        through everyone in the population and write their demographic data
        to a .csv file titled "demographics.csv". This file will have one row
        per person, and will have the following columns: id (str),
        age_group (int, optional), location_x (float, optional), location_y
        (float, optional), kw_or_chr (str)

        For the final column, 'K' refers to a key worker, 'C' refers to a
        care home resident and 'X' refers to a person who is neither

        """
        if self.spatial_output:
            if self.age_output:
                for cell in self._population.cells:
                    for person in cell.persons:
                        data = {"id": person.id,
                                "age_group": person.age_group,
                                "location_x": cell.location[0],
                                "location_y": cell.location[1],
                                "kw_or_chr": "K" if person.key_worker else
                                ("C" if person.care_home_resident else "X")}
                        self.writer.write(data)
            else:
                for cell in self._population.cells:
                    for person in cell.persons:
                        data = {"id": person.id,
                                "location_x": cell.location[0],
                                "location_y": cell.location[1],
                                "kw_or_chr": "K" if person.key_worker else
                                ("C" if person.care_home_resident else "X")}
                        self.writer.write(data)
        else:
            if self.age_output:
                for cell in self._population.cells:
                    for person in cell.persons:
                        data = {"id": person.id,
                                "age_group": person.age_group,
                                "kw_or_chr": "K" if person.key_worker else
                                ("C" if person.care_home_resident else "X")}
                        self.writer.write(data)
            else:
                for cell in self._population.cells:
                    for person in cell.persons:
                        data = {"id": person.id,
                                "kw_or_chr": "K" if person.key_worker else
                                ("C" if person.care_home_resident else "X")}
                        self.writer.write(data)
