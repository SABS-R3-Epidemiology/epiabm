**********
Properties
**********

.. currentmodule:: pyEpiabm.property

Properties provides various methods to get information from the population.

It includes many infection methods for houses, places and other spatial cells,
characterised by a force of infection exerted by each infected person.
This includes infectiousness and susceptibility components.

Infectiousness is (broadly) a function of 1 person (their age, places,
number of people in their household etc).
Susceptibility is (broadly) a function of 2 people (a person's susceptibility
to another person / potential infector).

Overview:

- :class:`InfectionStatus`
- :class:`PlaceType`
- :class:`PersonalInfection`
- :class:`HouseholdInfection`
- :class:`PlaceInfection`
- :class:`SpatialInfection`

.. autoclass:: InfectionStatus
    :members:

.. autoclass:: PlaceType
    :members:

.. autoclass:: PersonalInfection
    :members:

.. autoclass:: HouseholdInfection
    :members:

.. autoclass:: PlaceInfection
    :members:

.. autoclass:: SpatialInfection
    :members:
