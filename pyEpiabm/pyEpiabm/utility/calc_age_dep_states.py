import numpy as np
from numpy import mean

age_proportions = [6.2, 5.6, 5.8, 6.3, 6.8, 6.8, 6.5, 6.6,
                   7.3, 7.3, 6.5, 5.7, 6., 4.8, 3.9, 3.2, 4.7]


def wmean(values):
    return np.average(values, weights=age_proportions)

def list_print(values):
    print(', '.join(str(round(x, 6)) for x in values))


# Final probabilities
Prop_Mild_ByAge = np.array([0.666244874, 0.666307235, 0.666002907, 0.665309462, 0.663636419, 0.660834577, 0.657465236, 0.65343285, 0.650261465, 0.64478501, 0.633943755, 0.625619329, 0.609080537, 0.600364976, 0.5838608, 0.566553872, 0.564646465])
Prop_ILI_ByAge = np.array([0.333122437, 0.333153617, 0.333001453, 0.332654731, 0.33181821, 0.330417289, 0.328732618, 0.326716425, 0.325130732, 0.322392505, 0.316971878, 0.312809664, 0.304540269, 0.300182488, 0.2919304, 0.283276936, 0.282323232])
Prop_SARI_ByAge = np.array([0.000557744,	0.000475283, 0.000877703, 0.001794658, 0.004006955, 0.007711884, 0.012167229, 0.017359248, 0.021140307, 0.027047193, 0.03708932, 0.039871236, 0.040788928, 0.027444452, 0.101605674, 0.142001415, 0.150469697])
Prop_Critical_ByAge = np.array([7.49444E-05,	6.38641E-05, 0.000117937, 0.000241149, 0.000538417, 0.00103625, 0.001634918, 0.002491477, 0.003467496, 0.005775292, 0.011995047, 0.021699771, 0.045590266, 0.072008084, 0.022603126, 0.008167778, 0.002560606])

# Prop_ILI_ByAge = np.array(Prop_ILI_ByAge)
# Prop_SARI_ByAge = np.array(Prop_SARI_ByAge)
# Prop_Critical_ByAge = np.array(Prop_Critical_ByAge)
# Prop_Mild_ByAge = np.array(Prop_Mild_ByAge)

# list_print(wmean(Prop_ILI_ByAge), wmean(Prop_SARI_ByAge), wmean(Prop_Critical_ByAge), wmean(Prop_Mild_ByAge))
# list_print(sum((wmean(Prop_ILI_ByAge), wmean(Prop_SARI_ByAge), wmean(Prop_Critical_ByAge), wmean(Prop_Mild_ByAge))))

# Next steps - GP
prob_gp = Prop_ILI_ByAge + Prop_SARI_ByAge + Prop_Critical_ByAge
prob_gp_to_hosp = (Prop_SARI_ByAge + Prop_Critical_ByAge) / prob_gp
prob_gp_to_recov = 1 - prob_gp_to_hosp
# list_print(wmean(prob_gp), wmean(prob_gp_to_hosp), wmean(prob_gp_to_recov))
list_print(prob_gp_to_hosp)
list_print(prob_gp_to_recov)

# Next steps - Hosp other mortality rates calc below)
prob_hosp_to_icu = Prop_Critical_ByAge / (prob_gp * prob_gp_to_hosp)

# Symptomatic Data

Prop_Symptomatic_ByAge = [0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66]

prop_exposed_to_asympt = [(1 - x) for x in Prop_Symptomatic_ByAge]
prop_exposed_to_mild = Prop_Symptomatic_ByAge * Prop_Mild_ByAge
prop_exposed_to_gp = Prop_Symptomatic_ByAge * prob_gp

print("exposed")
list_print(prop_exposed_to_asympt)
list_print(prop_exposed_to_gp)
list_print(prop_exposed_to_mild)
# list_print(wmean(prop_exposed_to_asympt), wmean(prop_exposed_to_mild), wmean(prop_exposed_to_gp))
# list_print(sum((wmean(prop_exposed_to_asympt), wmean(prop_exposed_to_mild), wmean(prop_exposed_to_gp))))

# Mortality Risk

CFR_Critical_ByAge = np.array([0.5234896, 0.5234896,	0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896, 0.5234896])
CFR_SARI_ByAge = np.array([0.125893251, 0.12261338, 0.135672867, 0.152667869, 0.174303077, 0.194187895, 0.209361731, 0.224432564, 0.237013516, 0.257828065, 0.290874602, 0.320763971, 0.362563751, 0.390965457, 0.421151485, 0.447545892, 0.482])
CFR_ILI_ByAge = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


# CFR_ILI_ByAge = np.array(CFR_ILI_ByAge)
# CFR_SARI_ByAge = np.array(CFR_SARI_ByAge)
# CFR_Critical_ByAge = np.array(CFR_Critical_ByAge)

# list_print(wmean(CFR_ILI_ByAge), wmean(CFR_SARI_ByAge), wmean(CFR_Critical_ByAge))

# Hosp Data
prob_hosp_to_death = (1 - prob_hosp_to_icu) * CFR_SARI_ByAge
prob_hosp_to_recov = (1 - prob_hosp_to_icu) * (1 - CFR_SARI_ByAge)

print("Hosp")
list_print(prob_hosp_to_death)
list_print(prob_hosp_to_recov)
list_print(prob_hosp_to_icu)

# list_print(wmean(prob_hosp_to_icu), wmean(prob_hosp_to_death), wmean(prob_hosp_to_recov))
# list_print(sum((wmean(prob_hosp_to_icu), wmean(prob_hosp_to_death), wmean(prob_hosp_to_recov))))

# ICU data
prob_icu_to_death = CFR_Critical_ByAge
prob_icu_to_icurecov = 1 - CFR_Critical_ByAge

print("ICU")
list_print(prob_icu_to_death)
list_print(prob_icu_to_icurecov)

# list_print(wmean(prob_icu_to_death), wmean(prob_icu_to_icurecov))
