import matplotlib.pyplot as plt
import numpy as np


fig, axes = plt.subplots(1, 2, figsize=(10, 4))

def f(t, A, b):

    return A * 2 ** (-b * t)


intercept_41 = 4.26
half_life_41 = 85.38

intercept_change = 0.21
half_life_change = 4.07

t = np.linspace(0, 200)

colours = ['red', 'orange', 'green', 'blue', 'purple']

age = 21

while age < 62:

    age_difference_factor = int((age - 41) / 10)

    plot_colour = colours[age_difference_factor + 2]

    print(age_difference_factor)

    A = intercept_41 + age_difference_factor * intercept_change

    b = 1 / (half_life_41 + age_difference_factor * half_life_change)

    igg_plot = f(t, A, b)

    axes[0].plot(t, igg_plot, color=plot_colour, label=f'Age={age}')

    axes[1].plot(t, igg_plot, color=plot_colour, label=f'Age={age}')
    axes[1].set_yscale('log', base=2)

    age += 10

axes[0].set_xlabel('Time from maximum antibody titre, days')
axes[0].set_ylabel('Anti−nucleocapsid IgG titre, arbitrary units')
axes[0].set_title('Posterior mean IgG antibody level by age categories')
axes[0].legend()

axes[1].set_xlabel('Time from maximum antibody titre, days')
axes[1].set_ylabel('Log-base 2 of Anti−nucleocapsid IgG titre, arbitrary units')
axes[1].set_title('Posterior mean IgG antibody level by age categories')
axes[1].legend()

plt.tight_layout()

plt.show()





