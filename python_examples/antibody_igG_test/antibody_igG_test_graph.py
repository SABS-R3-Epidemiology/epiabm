import matplotlib.pyplot as plt
import numpy as np


def f(t, A, b):
    """Function modelling IgG antibody levels

    Args:
        t (np.linspace): time values
        A (float): maximum antibody level
        b (float): reciprocal of the mean half life

    Returns:
        np.linspace: Returns the corresponding antibody levels
    """

    return A * 2 ** (-b * t)

# create figure
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Values from Lumley et al. paper for ages 41
intercept_41 = 4.26
half_life_41 = 85.38

# Values from Lumley et al. paper for interpolating across ages
intercept_change = 0.21
half_life_change = 4.07

# time values
t = np.linspace(0, 200)

# match graph colours with the paper
colours = ['red', 'orange', 'green', 'blue', 'purple']

# begin from age 21
age = 21

# loop through all reference ages
while age < 62:

    # calculate multiplier of change values
    age_difference_factor = int((age - 41) / 10)

    # select plot colour from array
    plot_colour = colours[age_difference_factor + 2]

    # calculate intercept and decay values
    A = intercept_41 + age_difference_factor * intercept_change
    b = 1 / (half_life_41 + age_difference_factor * half_life_change)

    # return plots for correspinding constants
    igg_plot = f(t, A, b)

    # plot standard graph and log-2 graph
    axes[0].plot(t, igg_plot, color=plot_colour, label=f'Age={age}')
    axes[1].plot(t, igg_plot, color=plot_colour, label=f'Age={age}')
    axes[1].set_yscale('log', base=2)

    # increment age
    age += 10

# set up first plot
axes[0].set_xlabel('Time from maximum antibody titre, days')
axes[0].set_ylabel('IgG titre, arbitrary units')
axes[0].set_title('Posterior mean IgG antibody level by age categories')
axes[0].legend()
axes[0].grid(True)

# set up second plot
axes[1].set_xlabel('Time from maximum antibody titre, days')
axes[1].set_ylabel('Log-base 2 of IgG titre, arbitrary units')
axes[1].set_title('Posterior mean IgG antibody level by age categories')
axes[1].legend()
axes[1].grid(True)

# format layout of pane
plt.tight_layout()

# save the plot in the current directory
plt.savefig('IgG_validation_graphs.png')

# display plot pane
plt.show()
