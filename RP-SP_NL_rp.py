# Translated to .py by Yundi Zhang
# Jan 05 2017

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *

#Parameters to be estimated
# Arguments:
#   1  Name for report. Typically, the same as the variable
#   2  Starting value
#   3  Lower bound
#   4  Upper bound
#   5  0: estimate the parameter, 1: keep it fixed
ASC_RP_CAR	 = Beta('ASC_RP_CAR',0,-100,100,1)
ASC_RP_RAIL	 = Beta('ASC_RP_RAIL',0,-100,100,0)
BETA_COST	 = Beta('BETA_COST',0,-100,100,0)
BETA_TIME	 = Beta('BETA_TIME',0,-100,100,0)

# Define here arithmetic expressions for name that are not directly available from the data
one  = DefineVariable('one',1)
rail_time  = DefineVariable('rail_time', rail_ivtt   +  rp_rail_ovt )
car_time  = DefineVariable('car_time', car_ivtt   +  rp_car_ovt  )

# Utilities
__Car = ASC_RP_CAR * one + BETA_COST * car_cost + BETA_TIME * car_time
__Rail = ASC_RP_RAIL * one + BETA_COST * rail_cost + BETA_TIME * rail_time
__V = {0: __Car,1: __Rail}
__av = {0: rp,1: rp}

#Exclude
BIOGEME_OBJECT.EXCLUDE = sp != 0

# The choice model is a logit, with availability conditions
prob = bioLogit(__V,__av,choice)
__l = log(prob)

# Defines an itertor on the data
rowIterator('obsIter') 

# Define the likelihood function for the estimation
BIOGEME_OBJECT.ESTIMATE = Sum(__l,'obsIter')

# Optimization algorithm
BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = "BIO"

# Print some statistics:
nullLoglikelihood(__av,'obsIter')
choiceSet = [0,1]
cteLoglikelihood(choiceSet,choice,'obsIter')
availabilityStatistics(__av,'obsIter')
BIOGEME_OBJECT.FORMULAS['Car utility'] = __Car
BIOGEME_OBJECT.FORMULAS['Rail utility'] = __Rail