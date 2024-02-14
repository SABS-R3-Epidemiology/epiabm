#
# Class to produce a multiplier for the force of infection depending on an
# individual's IgG antibody count
#

import pyEpiabm as pe


class IgGFOIMultiplier:
    """Class which calculates a multiplier for the susceptibility in the force
    of infection (to be used in personal_foi.py) based on the current IgG
    antibody count.
    """
    def __init__(self, max_41: float, half_life_41: float,
                 change_in_max_10: float, change_in_half_life_10: float,
                 days_positive_pcr_to_max_igg: int):
        """Constructor Method

        Parameters
        ----------
        max_41 : float
            Maximum IgG titre (at the age of 41)
        half_life_41 : float
            Half-life in IgG titre (at the age of 41)
        change_in_max_10 : float
            Amount by which the maximum IgG increases for every extra 10 years
            of age a person has
        change_in_half_life_10 : float
            Amount by which the half-life in IgG increases for every extra 10
            years of age a person has
        days_positive_pcr_to_max_igg : int
            Mean number of days from the first positive PCR test to the day
            of maximum IgG titre
        """
        self.max_41 = max_41
        self.half_life_41 = half_life_41
        self.change_in_max_10 = change_in_max_10
        self.change_in_half_life_10 = change_in_half_life_10
        self.days_positive_pcr_to_max_igg = days_positive_pcr_to_max_igg
        # Parameter checks
        if max_41 <= 0:
            raise ValueError("max_41 must be positive")
        if half_life_41 <= 0:
            raise ValueError("half_life_41 must be positive")
        if days_positive_pcr_to_max_igg <= 0:
            raise ValueError("days_positive_pcr_to_max_igg must be positive")

        # We also need to ensure that the maximal IgG and half life will never
        # go negative when taking the changes into account. Multiplying by 4
        # corresponds to a change in 40 years of age from 41.
        maximal_change_in_max_igg = change_in_max_10 * 4
        maximal_change_in_half_life = change_in_half_life_10 * 4
        if abs(maximal_change_in_max_igg) > max_41:
            raise ValueError(f"change_in_max_10 is too large in magnitude "
                             f"(4 * {abs(change_in_max_10)} > {max_41})")
        if abs(maximal_change_in_half_life) > half_life_41:
            raise ValueError(f"change_in_half_life_10 is too large is too "
                             f"large in magnitude (4 * "
                             f"{abs(change_in_half_life_10)} > {half_life_41})"
                             )

        # This is the normalisation constant used later, defined as the maximal
        # IgG value (at time_since_max = 0) for the maximal age_group
        self.normalisation = self._calculate_igg_titre(0, 16)

    def __call__(self, time_since_infection: float, age_group: int) -> float:
        """Calculates the multiplier to be used in the force of infection.
        Takes the form 1 - A * 2^(-bt) where A and b are factors dependent on
        `age_group`. If we are not using ages, then we use values for age = 41.

        This will be a decaying exponential from the time of peak IgG titre,
        which occurs a fixed period of time after first being infected. Before
        the peak a person cannot be re-infected, so their force of infection
        will be zero.

        Parameters
        ----------
        time_since_infection : float
            Time (in days) since the `Person` first became infected
        age_group : int
            Age group of the `Person`

        Returns
        -------
        float
            An IgG multiplier for the force of infection
        """
        # If time_since_infection < days_positive_pcr_to_max_igg, then the
        # person cannot be reinfected yet, so set their multiplier to 0.
        if time_since_infection < self.days_positive_pcr_to_max_igg:
            return 0

        # time_since_max represents the days since maximal IgG titre
        time_since_max = (time_since_infection -
                          self.days_positive_pcr_to_max_igg)

        # If we are not using ages, then we take the normalised titre to just
        # be dependent on the half_life_41 value (as we want igg_titre = 1
        # when time_since_max = 0)
        if not pe.Parameters.instance().use_ages:
            igg_titre = 2 ** (- time_since_max / self.half_life_41)
        else:
            igg_titre = self._calculate_igg_titre(time_since_max, age_group)

            igg_titre /= self.normalisation

        return 1 - igg_titre

    def _calculate_igg_titre(self, time_since_max: float,
                            age_group: int) -> float:
        """The general expression for the titre is A * 2^(-t/c) where A is the
        max titre and c is the half-life. Both these values vary with age, and
        so given the values at age = 41 and the changes per 10 years of age,
        we calculate A and c for any given age_group.

        Parameters
        ----------
        time_since_max : float
            Time (in days) since a `Person`'s maximal IgG titre
        age_group : int
            Age group of the `Person`

        Returns
        -------
        float
            A value representing the IgG titre at a certain time
        """
        # Calculate parameters based on the person's age group
        # Note that 41 corresponds to an age_group of 8, and as the change
        # is over 10 years, we need to divide by 2 to get the change for
        # 5 years
        change_in_max = (age_group - 8) * self.change_in_max_10 / 2
        change_in_half_life = ((age_group - 8) *
                               self.change_in_half_life_10 / 2)

        # Find IgG titre
        igg_titre = ((self.max_41 + change_in_max) *
                     (2 ** (- time_since_max /
                            (self.half_life_41 + change_in_half_life))))
        return igg_titre
