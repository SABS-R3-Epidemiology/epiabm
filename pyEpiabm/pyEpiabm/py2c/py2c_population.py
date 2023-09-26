import time
from pyEpiabm.core import Population
from pyEpiabm.property import InfectionStatus


def py2c_population(py_population: Population, c_factory, c_status_map):
    return _py2c_converter(py_population, c_factory, c_status_map).c_population


class _Timer:
    def __init__(self, name: str):
        self.name = name
        self.t = time.perf_counter()

    def __del__(self):
        print(f'{self.name} took {time.perf_counter()-self.t}s')


class _py2c_converter:
    def __init__(self, py_population: Population, c_factory, c_status_map):
        self.py_population = py_population
        self.c_factory = c_factory
        self.c_population = None
        self.c_status_map = c_status_map

        self._index_population()
        self._validate_households()
        self._copy_structure()
        self._add_people()
        self._configure_people()
        self._configure_households()
        self._link_places()

    def _index_population(self):
        _ = _Timer("_index_population")
        place_i = 0
        for c_i, cell in enumerate(self.py_population.cells):
            cell._index = c_i  # Index cell
            person_index = 0
            self.households = set()
            for mc_i, m_cell in enumerate(cell.microcells):
                # Index microcells
                m_cell._index = (c_i, mc_i)
                assert m_cell.cell._index == c_i, \
                    "Microcell incorrectly linked to cell"
                for person in m_cell.persons:
                    # Index people
                    assert person.microcell.cell == cell, \
                        "Person incorrectly linked to microcell\
                            outside of cell"
                    assert person.microcell == m_cell
                    assert not hasattr(person, "_index"), \
                        "Person already indexed (is person in two microcells?)"
                    person._index = (c_i, person.microcell._index[1],
                                     person_index)
                    person_index += 1
                    if person.household is not None:
                        person.household._microcell_index = None
                        self.households.add(person.household)
            for place in cell.places:
                # cEpiabm stores places alongside population not cell
                place._index = place_i
                place_i += 1
        self.n_places = place_i

    def _validate_households(self):
        _ = _Timer("_validate_households")
        for household in self.households:
            for person in household.persons:
                if household._microcell_index is None:
                    household._microcell_index = person.microcell._index
                else:
                    assert household._microcell_index ==\
                        person.microcell._index, \
                        "Household cannot link two people\
                            in different microcells."
            if household._microcell_index is None:
                print("Warning: Empty Household exists.")
        for cell in self.py_population.cells:
            for m_cell in cell.microcells:
                m_cell._n_households = 0
        for household in self.households:
            id = household._microcell_index
            if id is None:
                continue
            self.py_population.cells[id[0]].microcells[id[1]]._n_households\
                += 1

    def _copy_structure(self):
        _ = _Timer("_copy_structure")
        self.c_population = self.c_factory.make_empty_population()
        n_cells = len(self.py_population.cells)
        self.c_factory.add_cells(self.c_population, n_cells)
        self.c_factory.add_places(self.c_population, self.n_places)
        for py_cell, c_cell in zip(
          self.py_population.cells, self.c_population.cells()):
            if py_cell.location is not None:
                c_cell.set_location(py_cell.location)
            n_microcells = len(py_cell.microcells)
            self.c_factory.add_microcells(c_cell, n_microcells)
            for py_mcell, c_mcell in zip(
              py_cell.microcells, c_cell.microcells()):
                self.c_factory.add_households(c_mcell, py_mcell._n_households)

    def _add_people(self):
        _ = _Timer("_add_people")
        for py_cell in self.py_population.cells:
            c_cell = self.c_population.get_cell(py_cell._index)
            for py_mcell in py_cell.microcells:
                c_mcell = c_cell.get_microcell(py_mcell._index[1])
                self.c_factory.add_persons(
                    c_cell, c_mcell, len(py_mcell.persons))

    def _configure_people(self):
        _ = _Timer("_configure_people")
        for py_cell, c_cell in zip(
          self.py_population.cells, self.c_population.cells()):
            assert py_cell._index == c_cell.index()
            for py_person, c_person in zip(py_cell.persons, c_cell.persons()):
                (c_i, mc_i, p_i) = py_person._index
                assert c_i == py_cell._index
                params = c_person.params()
                params.infectiousness = py_person.infectiousness
                params.initial_infectiousness =\
                    py_person.initial_infectiousness
                params.susceptibility = 1.0  # Is this correct? each
                #      person doesn't have their own susceptibility?
                params.age_group = py_person.age_group \
                    if py_person.age_group is not None else 0
                params.next_status_time = int(
                    py_person.time_of_status_change) \
                    if py_person.time_of_status_change is not None else 0
                if py_person.next_infection_status is not None:
                    params.next_status =\
                        self.c_status_map[py_person.next_infection_status]
                c_person.set_status(
                    self.c_status_map[py_person.infection_status])
                if py_person.infection_status == InfectionStatus.Susceptible:
                    c_cell.mark_non_infectious(c_i)
                elif py_person.infection_status == InfectionStatus.Exposed:
                    c_cell.mark_exposed(c_i)
                elif py_person.infection_status == InfectionStatus.Recovered:
                    c_cell.mark_recovered(c_i)
                elif py_person.infection_status == InfectionStatus.Dead:
                    c_cell.mark_dead(c_i)
                else:
                    c_cell.mark_infectious(c_i)

    def _configure_households(self):
        _ = _Timer("_configure_households")
        index_counter = {}
        for _, py_household in enumerate(self.households):
            (c_i, mc_i) = py_household._microcell_index
            c_cell = self.c_population.get_cell(c_i)
            c_mcell = c_cell.get_microcell(mc_i)
            if py_household._microcell_index in index_counter:
                index_counter[py_household._microcell_index] += 1
            else:
                index_counter[py_household._microcell_index] = 0
            hh_i = index_counter[py_household._microcell_index]
            py_household._microcell_index = (c_i, mc_i, hh_i)
            c_household = c_mcell.get_household(hh_i)
            # Link People
            for py_person in py_household.persons:
                c_person = c_cell.get_person(py_person._index[2])
                assert c_person.set_household(hh_i), \
                    "Person was already in a different household"
                c_household.add_member(c_person.microcell_pos())
            # Configure Household Parameters
            params = c_household.params()
            params.infectiousness = py_household.infectiousness
            params.susceptibility = py_household.susceptibility
            params.location = py_household.location

    def _link_places(self):
        _ = _Timer("_link_places")
        for py_cell in self.py_population.cells:
            for py_place in py_cell.places:
                c_place = self.c_population.get_place(py_place._index)
                assert c_place.index() == py_place._index

                for group, persons in py_place.person_groups.items():
                    for py_person in persons:
                        (c_i, mc_i, p_i) = py_person._index
                        c_cell = self.c_population.get_cell(c_i)
                        c_cell.get_person(p_i).add_place(
                            self.c_population, c_cell,
                            c_place.index(), group)
