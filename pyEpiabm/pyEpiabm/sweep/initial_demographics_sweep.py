#
# Sweep to record demographic information of the population in a .csv file
#

import os
import typing

from pyEpiabm.core import Parameters
from pyEpiabm.output import _CsvDictWriter

from .abstract_sweep import AbstractSweep


class InitialDemographicsSweep(AbstractSweep):
    """Class to sweep through the population at the beginning of the simulation
    and record their demographic information

    """

    def __init__(self, dem_file_params: typing.Dict):
        """Initiate file parameters referring to the file location and
        which columns are to be included

        dem_file_params Contains:
            * `output_dir`: String for the location of the output file, \
               as a relative path
            * `spatial_output`: Boolean to determine whether a spatial output \
               should be used
            * `age_output`: Boolean to determine whether the output will \
                have ages

        """

        # Must have an output directory
        if "output_dir" not in dem_file_params:
            raise ValueError("output_dir must be specified in dem_file_params")

        # Check for invalid keys
        invalid_keys = set(dem_file_params.keys()) - \
            {"output_dir", "age_output", "spatial_output"}
        if len(invalid_keys) != 0:
            raise ValueError(f"dem_file_params contains invalid keys: "
                             f"{invalid_keys}")
        self.spatial_output = dem_file_params["spatial_output"] \
            if "spatial_output" in dem_file_params else False
        self.age_output = dem_file_params["age_output"] \
            if "age_output" in dem_file_params else False
        if self.age_output and not Parameters.instance().use_ages:
            raise ValueError("age_output cannot be True as Parameters"
                             ".instance().use_ages is False")

        # Here we set up the writer
        folder = os.path.join(os.getcwd(),
                              dem_file_params["output_dir"])
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

        Note that kw_or_chr stands for 'key worker or care home resident'. For
        kw_or_chr, 'W' refers to a key worker, 'C' refers to a care home
        resident and 'X' refers to a person who is neither

        """
        for cell in self._population.cells:
            for person in cell.persons:
                data = {"id": person.id,
                        "age_group": person.age_group
                        if self.age_output else None,
                        "location_x": cell.location[0]
                        if self.spatial_output else None,
                        "location_y": cell.location[1]
                        if self.spatial_output else None,
                        "kw_or_chr": "W" if person.key_worker else
                        ("C" if person.care_home_resident else "X")}
                data = {k: data[k] for k in data if data[k] is not None}
                self.writer.write(data)
