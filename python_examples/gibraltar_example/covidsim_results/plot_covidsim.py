
import pandas as pd
import numpy as np
import sys
import os
# Add plotting functions to path
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir,
                "../age_stratified_example"))
print(os.path.join(os.path.dirname(__file__), os.path.pardir,
                   "../age_stratified_example"))
from age_stratified_plot import Plotter  # noqa

data = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                "severity_age.csv"))

header_list = (data.columns[0].split('\t'))
dataFrame = None
for index, row in data.iterrows():
    newdata = (row.values[0].split('\t'))
    newdata = np.array([float(n) for n in newdata])
    if dataFrame is None:
        dataFrame = pd.DataFrame([newdata], columns=header_list)
    else:
        dataFrame.loc[len(dataFrame.index)] = newdata

INCdF = dataFrame[list(dataFrame.filter(regex='inc'))]
CUMdF = dataFrame[list(dataFrame.filter(regex='cum'))]
Pcolumns = list(dataFrame.filter(regex='P'))
dF = dataFrame.drop(columns=(list(INCdF.columns) + list(CUMdF.columns)
                    + list(Pcolumns)))

case_list = list(dF.columns)[1:]  # remove time column
severity_list = list(set(['_'.join(case.split('_')[:-1])
                         for case in case_list]))
age_list = [case.split('_')[-1] for case in case_list]

num_age_groups = max([int(age) for age in age_list]) + 1

agedF = []
for t in dF['t']:
    for age in range(num_age_groups):
        newrow = {'t': int(t), 'age': age}
        orig_row = dF.iloc[int(t)]
        for status in severity_list:
            newrow[status] = orig_row[status+'_'+str(age)]
        agedF.append(newrow)
finalDF = pd.DataFrame(agedF)

# Rename infection status to be consistent with epiabm
colname_replace = {'t': 'time', 'age': 'age',
                   'CritRecov': 'InfectionStatus.InfectICURecov',
                   'Mild': 'InfectionStatus.InfectMild',
                   'Critical': 'InfectionStatus.InfectICU',
                   'ILI': 'InfectionStatus.InfectGP',
                   'SARI': 'InfectionStatus.InfectHosp'}
finalDF = finalDF.rename(columns=colname_replace)

for index, row in finalDF.iterrows():
    if sum(row.values[2:]) == 0:
        finalDF = finalDF.copy().drop([index], axis=0)
# Write the fully modified
finalDF['time'] = finalDF['time'] - finalDF.iloc[(0, 0)]
finalDF = finalDF.reset_index().drop(columns=['index'])
print(finalDF)
finalDF.to_csv(os.path.join(os.path.dirname(__file__),
               "modified_age_severity.csv"))

p = Plotter(os.path.join(os.path.dirname(__file__),
            "modified_age_severity.csv"),
            start_date='18-03-2022', sum_weekly=True)
p.barchart(os.path.join(os.path.dirname(__file__),
           "age_stratify.png"),
           write_Df_toFile=os.path.join(os.path.dirname(__file__),
           "covidsim_daily_cases.csv"),
           param_file=os.path.join(os.path.dirname(__file__),
           os.path.pardir, "./gibraltar_parameters.json"))
# Default file format is .png, but can be changed to .pdf, .svg, etc.
