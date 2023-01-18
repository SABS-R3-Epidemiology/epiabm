import os
import matplotlib.pyplot as plt
  
x = []
y = []
for line in open('Sim_Speeds_plot.txt', 'r'):
    lines = [i for i in line.split()]
    x.append(lines[1])
    y.append(int(lines[4]))
      
plt.title("Simulation time for basic simulation over 60 days")
plt.xlabel('Population Size')
plt.ylabel('time (s)')
plt.plot(x, y, marker = 'o', c = 'g')

plt.show()

plt.savefig("basic_sim_speed.png")
