# %%
import bnlearn
print(bnlearn.__version__)
dir(bnlearn)


# %%
dir(bnlearn.structure_learning)


# %% Load example dataframe from sprinkler
df = bnlearn.import_example()
# Structure learning
model = bnlearn.structure_learning.fit(df)
# Plot
G = bnlearn.plot(model)


# %% Try all methods vs score types
model_hc_bic = bnlearn.structure_learning.fit(df, methodtype='hc', scoretype='bic')
model_hc_k2 = bnlearn.structure_learning.fit(df, methodtype='hc', scoretype='k2')
model_hc_bdeu = bnlearn.structure_learning.fit(df, methodtype='hc', scoretype='bdeu')
model_ex_bic = bnlearn.structure_learning.fit(df, methodtype='ex', scoretype='bic')
model_ex_k2 = bnlearn.structure_learning.fit(df, methodtype='ex', scoretype='k2')
model_ex_bdeu = bnlearn.structure_learning.fit(df, methodtype='ex', scoretype='bdeu')

bnlearn.compare_networks(model, model_hc_bic, pos=G['pos'])


# %% Example with dataset
DAG = bnlearn.import_DAG()
# plot ground truth
G = bnlearn.plot(DAG)


# %% Inference using custom DAG
from tabulate import tabulate
# Load asia DAG
import bnlearn
df = bnlearn.import_example('asia')
# print(tabulate(df.head(), tablefmt="grid", headers="keys"))
print(df)

edges = [('smoke', 'lung'),
         ('smoke', 'bronc'),
         ('lung', 'xray'),
         ('bronc', 'xray')]

# Make the actual Bayesian DAG
DAG = bnlearn.make_DAG(edges)
# Plot the DAG
bnlearn.plot(DAG)
# Print the CPDs
bnlearn.print_CPD(DAG)

# Learn its parameters from data and perform the inference.
DAG = bnlearn.parameter_learning.fit(DAG, df, methodtype='bayes')
# Print the CPDs
bnlearn.print_CPD(DAG)

# Make inference
q1 = bnlearn.inference.fit(DAG, variables=['lung'], evidence={'smoke':1})
q2 = bnlearn.inference.fit(DAG, variables=['bronc'], evidence={'smoke':1})
q3 = bnlearn.inference.fit(DAG, variables=['lung'], evidence={'smoke':1, 'bronc':1})
q4 = bnlearn.inference.fit(DAG, variables=['bronc','lung'], evidence={'smoke':1, 'xray':0})
q4 = bnlearn.inference.fit(DAG, variables=['bronc','lung'], evidence={'smoke':0, 'xray':0})

# DAGmle = bnlearn.parameter_learning.fit(DAG, df, methodtype='maximumlikelihood')
# bnlearn.print_CPD(DAGmle)
# bnlearn.print_CPD(DAGbay)

# # Make inference
# q1 = bnlearn.inference.fit(DAGmle, variables=['lung'], evidence={'smoke':1})
# q2 = bnlearn.inference.fit(DAGmle, variables=['bronc'], evidence={'smoke':1})
# q3 = bnlearn.inference.fit(DAGmle, variables=['lung'], evidence={'smoke':1, 'bronc':1})
# q4 = bnlearn.inference.fit(DAGmle, variables=['bronc','lung'], evidence={'smoke':1, 'xray':0})

# bnlearn.compare_networks(DAGbay, DAGnew)
# bnlearn.compare_networks(DAGnew, DAGbay)

# %% compute causalities
# Load asia DAG
import bnlearn
df = bnlearn.import_example('asia')
# print(tabulate(df.head(), tablefmt="grid", headers="keys"))
# print(df)

# Structure learning
model = bnlearn.structure_learning.fit(df)
# Plot the DAG
bnlearn.plot(model)
# Print the CPDs
bnlearn.print_CPD(model)
# Comparison
bnlearn.compare_networks(DAG, model)
bnlearn.compare_networks(model, DAG)

# Learn its parameters from data and perform the inference.
DAGnew = bnlearn.parameter_learning.fit(model, df, methodtype='bayes')
# Print the CPDs
bnlearn.print_CPD(DAGnew)

# Make inference
q4 = bnlearn.inference.fit(DAGnew, variables=['bronc','lung'], evidence={'smoke':1, 'xray':0})
# q4 = bnlearn.inference.fit(DAGnew, variables=['bronc','lung'], evidence={'smoke':0, 'xray':0})


# %% Example compare networks
# Load asia DAG
import bnlearn
DAG = bnlearn.import_DAG('asia')
# plot ground truth
G = bnlearn.plot(DAG)
# Sampling
df = bnlearn.sampling(DAG, n=10000)
# Structure learning of sampled dataset
model_sl = bnlearn.structure_learning.fit(df, methodtype='hc', scoretype='bic')
# Plot based on structure learning of sampled data
bnlearn.plot(model_sl, pos=G['pos'])
# Compare networks and make plot
bnlearn.compare_networks(model, model_sl, pos=G['pos'])


# Structure learning with black list
model_wl = bnlearn.structure_learning.fit(df, methodtype='hc', white_list=['asia','tub','bronc','xray','smoke'])
bnlearn.plot(model_wl, pos=G['pos'])

model_bl = bnlearn.structure_learning.fit(df, methodtype='hc', black_list=['asia','tub'])
bnlearn.plot(model_bl, pos=G['pos'])

# Compare models
bnlearn.compare_networks(model_bl, model_wl, pos=G['pos'])


# %% PARAMETER LEARNING
df = bnlearn.import_example()
DAG = bnlearn.import_DAG('sprinkler', CPD=False)
model_update = bnlearn.parameter_learning.fit(DAG, df)
bnlearn.plot(model_update)

model_true = bnlearn.import_DAG('sprinkler', CPD=True)

# %% Example with one-hot RAW dataset: sprinkler.
# Load processed data
DAG = bnlearn.import_DAG('sprinkler')

# Read raw data and process
df_raw = bnlearn.import_example(data='sprinkler')
df = bnlearn.df2onehot(df_raw, verbose=0)[1]
df.columns=df.columns.str.replace('_1.0','')

# Learn structure
DAG = bnlearn.structure_learning.fit(df)
# Learn CPDs
model = bnlearn.parameter_learning.fit(DAG, df)
q1 = bnlearn.inference.fit(model, variables=['Wet_Grass'], evidence={'Rain':1, 'Sprinkler':0, 'Cloudy':1})
q2 = bnlearn.inference.fit(model, variables=['Wet_Grass','Rain'], evidence={'Sprinkler':1})


q2.values
q2.variables
q2.state_names
q2.name_to_no
q2.no_to_name,

# %% LOAD BIF FILE
DAG = bnlearn.import_DAG('alarm', verbose=0)
df = bnlearn.sampling(DAG, n=1000)
model_update = bnlearn.parameter_learning.fit(DAG, df)
G = bnlearn.plot(model_update)
bnlearn.print_CPD(model_update)


# %% INFERENCE
DAG = bnlearn.import_DAG('sprinkler')
bnlearn.plot(DAG)
q1 = bnlearn.inference.fit(DAG, variables=['Wet_Grass'], evidence={'Rain':1, 'Sprinkler':0, 'Cloudy':1})
q2 = bnlearn.inference.fit(DAG, variables=['Wet_Grass','Rain'], evidence={'Sprinkler': 1})

print(q1)
print(q2)


# %% INFERENCE 2
DAG = bnlearn.import_DAG('asia')
# DAG = bnlearn.import_DAG('sprinkler')
bnlearn.plot(DAG)
q1 = bnlearn.inference.fit(DAG, variables=['lung'], evidence={'bronc':1, 'smoke':1})
q2 = bnlearn.inference.fit(DAG, variables=['bronc','lung'], evidence={'smoke':1, 'xray':0, 'tub':1})
q3 = bnlearn.inference.fit(DAG, variables=['lung'], evidence={'bronc':1, 'smoke':1})

print(q1)
print(q2)


# %% Example with mixed dataset: titanic case
import bnlearn
# Load example mixed dataset
df_raw = bnlearn.import_example(data='titanic')
# Convert to onehot
dfhot, dfnum = bnlearn.df2onehot(df_raw)
# Structure learning
DAG = bnlearn.structure_learning.fit(dfnum, black_list=['Survived','Pclass','Sex','Embarked','Parch'])
# Plot
G = bnlearn.plot(DAG)
# Parameter learning
model = bnlearn.parameter_learning.fit(DAG, dfnum)
# Make inference
q1 = bnlearn.inference.fit(model, variables=['Survived'], evidence={'Sex':1, 'Pclass':1})
q1 = bnlearn.inference.fit(model, variables=['Survived'], evidence={'Sex':0})

bnlearn.print_CPD(model)

# %%
DAG = bnlearn.import_DAG('sprinkler', CPD=False)
DAG = bnlearn.import_DAG('asia')
bnlearn.plot(DAG)
bnlearn.print_CPD(DAG)

df = bnlearn.sampling(DAG, n=1000)
vector = bnlearn.adjmat2vec(DAG['adjmat'])
adjmat = bnlearn.vec2adjmat(vector['source'], vector['target'])

# %%
from pgmpy.factors.discrete import TabularCPD
edges = [('A', 'E'),
         ('S', 'E'),
         ('E', 'O'),
         ('E', 'R'),
         ('O', 'T'),
         ('R', 'T')]

DAG = bnlearn.make_DAG(edges)
bnlearn.plot(DAG)


cpd_A = TabularCPD(variable='A', variable_card=3, values=[[0.3], [0.5], [0.2]])
print(cpd_A)
cpd_S = TabularCPD(variable='S', variable_card=2, values=[[0.6],[ 0.4]])
print(cpd_S)
cpd_E = TabularCPD(variable='E', variable_card=2,
                           values=[
                               [0.75,0.72,0.88,0.64,0.70,0.90],
                               [0.25,0.28,0.12,0.36,0.30,0.10]
                               ],
                           evidence=['A', 'S'],
                           evidence_card=[3, 2])
print(cpd_E)


DAG = bnlearn.make_DAG(DAG, CPD=cpd_A, checkmodel=False)
bnlearn.print_CPD(DAG, checkmodel=False)

# %% Create a simple DAG:
# Building a causal DAG
from pgmpy.factors.discrete import TabularCPD

edges = [('Cloudy', 'Sprinkler'),
       ('Cloudy', 'Rain'),
       ('Sprinkler', 'Wet_Grass'),
       ('Rain', 'Wet_Grass')]

# DAG = bnlearn.import_DAG('sprinkler')
DAG = bnlearn.make_DAG(edges)
bnlearn.plot(DAG)
bnlearn.print_CPD(DAG)

# Cloudy
cpt_cloudy = TabularCPD(variable='Cloudy', variable_card=2, values=[[0.3], [0.7]])
print(cpt_cloudy)

# Sprinkler
cpt_sprinkler = TabularCPD(variable='Sprinkler', variable_card=2,
                           values=[[0.4, 0.9], [0.6, 0.1]],
                           evidence=['Cloudy'], evidence_card=[2])
print(cpt_sprinkler)

# Rain
cpt_rain = TabularCPD(variable='Rain', variable_card=2,
                      values=[[0.8, 0.2], [0.2, 0.8]],
                      evidence=['Cloudy'], evidence_card=[2])
print(cpt_rain)

# Wet Grass
cpt_wet_grass = TabularCPD(variable='Wet_Grass', variable_card=2,
                           values=[[1, 0.1, 0.1, 0.01],
                                  [0, 0.9, 0.9, 0.99]],
                           evidence=['Sprinkler', 'Rain'],
                           evidence_card=[2, 2])
print(cpt_wet_grass)

# The make_DAG function will required a CPD for each node. If this is not the case, use the checkmodel=False
DAG = bnlearn.make_DAG(DAG, CPD=cpt_cloudy, checkmodel=False)
DAG = bnlearn.make_DAG(DAG, CPD=[cpt_cloudy, cpt_sprinkler], checkmodel=False)
DAG = bnlearn.make_DAG(DAG, CPD=[cpt_cloudy, cpt_sprinkler, cpt_rain, cpt_wet_grass])
bnlearn.print_CPD(DAG)

q1 = bnlearn.inference.fit(DAG, variables=['Wet_Grass'], evidence={'Rain':1, 'Sprinkler':0, 'Cloudy':1})

# %% Example from sphinx
# Import dataset
# Import the library
import bnlearn

# Define the network structure
edges = [('Cloudy', 'Sprinkler'),
         ('Cloudy', 'Rain'),
         ('Sprinkler', 'Wet_Grass'),
         ('Rain', 'Wet_Grass')]

# Make the actual Bayesian DAG
DAG = bnlearn.make_DAG(edges)

bnlearn.plot(DAG)


bnlearn.print_CPD(DAG)

# Import the library
from pgmpy.factors.discrete import TabularCPD

# Cloudy
cpt_cloudy = TabularCPD(variable='Cloudy', variable_card=2, values=[[0.5], [0.5]])
print(cpt_cloudy)

# Sprinkler
cpt_sprinkler = TabularCPD(variable='Sprinkler', variable_card=2,
                           values=[[0.5, 0.9],
                                   [0.5, 0.1]],
                           evidence=['Cloudy'], evidence_card=[2])
print(cpt_sprinkler)

# Rain
cpt_rain = TabularCPD(variable='Rain', variable_card=2,
                      values=[[0.8, 0.2],
                              [0.2, 0.8]],
                      evidence=['Cloudy'], evidence_card=[2])
print(cpt_rain)

# Wet Grass
cpt_wet_grass = TabularCPD(variable='Wet_Grass', variable_card=2,
                           values=[[1, 0.1, 0.1, 0.01],
                                   [0, 0.9, 0.9, 0.99]],
                           evidence=['Sprinkler', 'Rain'],
                           evidence_card=[2, 2])
print(cpt_wet_grass)

DAG = bnlearn.make_DAG(DAG, CPD=[cpt_cloudy, cpt_sprinkler, cpt_rain, cpt_wet_grass])


bnlearn.print_CPD(DAG)


q1 = bnlearn.inference.fit(DAG, variables=['Wet_Grass'], evidence={'Rain':1, 'Sprinkler':0, 'Cloudy':1})


# %% Example to create a Bayesian Network, learn its parameters from data and perform the inference.

import bnlearn

# Import example dataset
df = bnlearn.import_example('sprinkler')

# Define the network structure
edges = [('Cloudy', 'Sprinkler'),
         ('Cloudy', 'Rain'),
         ('Sprinkler', 'Wet_Grass'),
         ('Rain', 'Wet_Grass')]

# Make the actual Bayesian DAG
DAG = bnlearn.make_DAG(edges)
# [BNLEARN] Bayesian DAG created.

# Print the CPDs
bnlearn.print_CPD(DAG)
# [BNLEARN.print_CPD] No CPDs to print. Use bnlearn.plot(DAG) to make a plot.

# Plot the DAG
bnlearn.plot(DAG)

# Parameter learning on the user-defined DAG and input data using maximumlikelihood
DAGmle = bnlearn.parameter_learning.fit(DAG, df, methodtype='maximumlikelihood')
DAGbay = bnlearn.parameter_learning.fit(DAG, df, methodtype='bayes')

# Print the learned CPDs
bnlearn.print_CPD(DAGmle)
bnlearn.print_CPD(DAGbay)

# Make inference
q1 = bnlearn.inference.fit(DAGmle, variables=['Wet_Grass'], evidence={'Rain':1, 'Sprinkler':0, 'Cloudy':1})
q1 = bnlearn.inference.fit(DAGbay, variables=['Wet_Grass'], evidence={'Rain':1, 'Sprinkler':0, 'Cloudy':1})

print(q1.values)

