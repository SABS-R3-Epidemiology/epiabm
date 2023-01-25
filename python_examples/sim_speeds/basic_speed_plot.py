# Code to plot runtime from .txt file

import matplotlib.pyplot as plt
import os


def get_seconds(time_str):
    print('Time in mm:ss:', time_str)
    # split in hh, mm, ss
    mm, ss = time_str.split(':')
    return int(mm) * 60 + int(ss)


print('Time in Seconds:', get_seconds('05:15'))
print('Time in Seconds:', get_seconds('00:32'))

x = []
y_list = []
y = []

# for line in open(os.path.join(os.path.dirname(__file__),
#                  "Sim_Speeds.txt"), 'r'):
#     print('line split:', line.split())
#     lines = [i for i in range(1, line.split(), 1)]
#     x.append(int(lines[1]))
#     y_list.append(lines[4])
#     y.append(get_seconds(y_list))
# #    y.append(int(lines[4]))

with open(os.path.join(os.path.dirname(__file__),
                       "Sim_Speeds.txt"), 'r') as input_data:
    all_data = [line.strip() for line in input_data.readlines()]
    only_data = all_data[1:]
    print('DATA! ', all_data)
    print('length! ', len(all_data))
    print('popu_size ', only_data)
    for i in range(1, len(only_data)):
        print('i', i)
        print('data 1: ', only_data(i,1))
        x.append(int(only_data[i,1]))
    # y_list.append(lines[4])
        y.append(int(get_seconds(only_data[i,4])))
#    y.append(int(lines[4]))

plt.title("Simulation time for basic simulation over 60 days")
plt.xlabel('Population Size')
plt.xscale('log')
plt.yscale('log')
plt.ylabel('time (s)')
plt.plot(x, y, marker='o', c='g')

plt.savefig("sim_speeds_plots/basic_sim_speed.png")


plt.show()
