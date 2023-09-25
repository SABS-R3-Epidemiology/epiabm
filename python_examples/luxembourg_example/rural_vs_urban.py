import os
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt


# Creation of a plot of results (plotter from spatial_simulation_flow)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__),
                        "simulation_outputs/large_csv",
                        "output_luxembourg_pre_change.csv")
SIRdf = pd.read_csv(filename)

clipped_df = SIRdf.loc[SIRdf['location_y'] < 49.81]

print('Clipped', clipped_df.shape)
# print('Clipped', clipped_df['location_y'])

clipped_df = clipped_df.loc[clipped_df['location_y'] > 49.78]

print('Clipped', clipped_df.shape)

clipped_df_2 = clipped_df.loc[clipped_df['location_x'] < 6.184]
clipped_df_2 = clipped_df_2.loc[clipped_df_2['location_x'] > 6.158]

print('Clipped', clipped_df_2.shape)

SIRdf_rural_pre = clipped_df_2

####################
clipped_df = SIRdf.loc[SIRdf['location_y'] < 49.626]

print('Clipped', clipped_df.shape)
# print('Clipped', clipped_df['location_y'])

clipped_df = clipped_df.loc[clipped_df['location_y'] > 49.599]

print('Clipped', clipped_df.shape)

clipped_df_2 = clipped_df.loc[clipped_df['location_x'] < 6.142]
clipped_df_2 = clipped_df_2.loc[clipped_df_2['location_x'] > 6.116]

print('Clipped', clipped_df_2.shape)

SIRdf_urban_pre = clipped_df_2



# Creation of a plot of results (plotter from spatial_simulation_flow)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__),
                        "simulation_outputs/large_csv",
                        "output_luxembourg_post_change.csv")
SIRdf = pd.read_csv(filename)

clipped_df = SIRdf.loc[SIRdf['location_y'] < 49.81]

print('Clipped', clipped_df.shape)
# print('Clipped', clipped_df['location_y'])

clipped_df = clipped_df.loc[clipped_df['location_y'] > 49.78]

print('Clipped', clipped_df.shape)

clipped_df_2 = clipped_df.loc[clipped_df['location_x'] < 6.184]
clipped_df_2 = clipped_df_2.loc[clipped_df_2['location_x'] > 6.158]

print('Clipped', clipped_df_2.shape)

SIRdf_rural_post = clipped_df_2

####################
clipped_df = SIRdf.loc[SIRdf['location_y'] < 49.626]

print('Clipped', clipped_df.shape)
# print('Clipped', clipped_df['location_y'])

clipped_df = clipped_df.loc[clipped_df['location_y'] > 49.599]

print('Clipped', clipped_df.shape)

clipped_df_2 = clipped_df.loc[clipped_df['location_x'] < 6.142]
clipped_df_2 = clipped_df_2.loc[clipped_df_2['location_x'] > 6.116]

print('Clipped', clipped_df_2.shape)

SIRdf_urban_post = clipped_df_2

##############
total_rural_pre = SIRdf_rural_pre[list(SIRdf_rural_pre.filter(regex='InfectionStatus.Infect'))]
SIRdf_rural_pre["Infected"] = total_rural_pre.sum(axis=1)
SIRdf_rural_pre = SIRdf_rural_pre.groupby(["time"]).agg(
                                {"Infected": 'sum'})

# Create infected plot
# SIRdf_rural.plot(y=["Infected"])

total_rural_post = SIRdf_rural_post[list(SIRdf_rural_post.filter(regex='InfectionStatus.Infect'))]
SIRdf_rural_post["Infected"] = total_rural_post.sum(axis=1)
SIRdf_rural_post = SIRdf_rural_post.groupby(["time"]).agg(
                                {"Infected": 'sum'})

# Create plot to show SIR curves against time
SIRdf_rural_post.plot(y=["Infected"])

print('Df', SIRdf_rural_post)
plt.figure()
plt.plot(SIRdf_rural_pre['Infected'])
plt.plot(SIRdf_rural_post['Infected'])
plt.legend(['Distance weighted', 'Distance and population weighted'])
plt.xlabel('time (days)')
plt.ylabel('Infected people')


plt.savefig(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/rural.png"), dpi=300)


##############
total_urban_pre = SIRdf_urban_pre[list(SIRdf_urban_pre.filter(regex='InfectionStatus.Infect'))]
SIRdf_urban_pre["Infected"] = total_urban_pre.sum(axis=1)
SIRdf_urban_pre = SIRdf_urban_pre.groupby(["time"]).agg(
                                {"Infected": 'sum'})

# Create infected plot

total_urban_post = SIRdf_urban_post[list(SIRdf_urban_post.filter(regex='InfectionStatus.Infect'))]
SIRdf_urban_post["Infected"] = total_urban_post.sum(axis=1)
SIRdf_urban_post = SIRdf_urban_post.groupby(["time"]).agg(
                                {"Infected": 'sum'})

# Create plot to show SIR curves against time
SIRdf_urban_post.plot(y=["Infected"])

print('Df', SIRdf_urban_post)
plt.figure()
plt.plot(SIRdf_urban_pre['Infected'])
plt.plot(SIRdf_urban_post['Infected'])
plt.legend(['Distance weighted', 'Distance and population weighted'])
plt.xlabel('time (days)')
plt.ylabel('Infected people')


plt.savefig(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/infected_urban.png"), dpi=300)
