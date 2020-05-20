from pprint import pprint
from scipy.stats import chi2, chi2_contingency
from sys import argv
import numpy as np
import pandas as pd


file_name = 'restaurant.csv'

#chi square value for pruning
alpha = 0.05 

def get_data(values):
    # to store the possible values that each attribute can take, taking the unique values of each column and storing it in a list
    data = pd.read_csv(file_name)

    for i in data.columns:
        values.append(data[i].unique())

    return values
    
    

def partition(a, selected_attribute, values):
    #takes values of an attribute as parameter and splits it based on values
    dict = {}
    for c in np.unique(a):
        dict.update({c : (a==c).nonzero()[0] })

    for i in values[selected_attribute]:
        if i not in dict:
            dict.update({i : None })

    return dict


def entropy(s):
    # to calculate entropy of attributes, measures the degree of randomness in the variable, higher the entropy harder it is to draw conclusions from that information
    #  as the information gain increases, entropy decreases
    result = 0
    val, counts = np.unique(s, return_counts=True)
    frequencies = counts.astype('float')/len(s)
    for p in frequencies:
        if p != 0.0:
            result -= p * np.log2(p)
    return result


def information_gain(y, x):
    # to compute the information gain of each attribute

    res = entropy(y)

    # We partition x, according to attribute values x_i
    val, counts = np.unique(x, return_counts=True)
    freqs = counts.astype('float')/len(x)

    # We calculate a weighted average of the entropy
    for p, v in zip(freqs, val):
        res -= p * entropy(y[x == v])

    return res


def is_pure(s):
   #checks if all weights are the same
    return len(set(s)) == 1


def recursive_split(x, y, attributeName, values):

    # to compute the best split from list of examples having various attributes, returns a dictionary with maximum information gain
    
    # If all weights are same, cannot be split further, return the weight , either 'yes' or 'no'
    if is_pure(y) or len(y) == 0: 
        
        return str(y[0])

    gain = np.array([round(information_gain(y, x_attr), 2) for x_attr in x.T])
    selected_attribute = np.argmax(gain)


    if np.all(gain < 1e-6):
        return y

    sets = partition(x[:, selected_attribute], selected_attribute, values)

    res = {}
    for k, v in sets.items():

        
        if v is None:
            res[attributeName[selected_attribute] + " = " + k ] = 'Yes'
        else:
            # to create subsets of data based on the split
            y_subset = y.take(v, axis=0)
            x_subset = x.take(v, axis=0)
            x_subset = np.delete(x_subset, selected_attribute, 1)
            values_subset = values[:selected_attribute] + values[selected_attribute+1:]
            attributeName_subset = attributeName[:selected_attribute] + attributeName[selected_attribute+1:]
            res[attributeName[selected_attribute] + " = " + k ] = recursive_split(x_subset, y_subset, attributeName_subset, values_subset)

    return res


def pruneLeaves(obj):
    # takes a decision tree input and based on chi square, returns a pruned tree
    
    isLeaf = True
    parent = None
    for key in obj:
        if isinstance(obj[key], dict):
            isLeaf = False
            parent = key
            break
    if isLeaf and list(obj.keys())[0].split(' ')[0] not in satisfied_attributes:
        global pruned
        pruned = True
        return 'pruned'
    if not isLeaf:
        if pruneLeaves(obj[parent]):
            obj[parent] = None
    return obj


#read examples from the csv file
data = np.loadtxt(open(file_name, "rb"), delimiter=",", dtype='str', converters = {3: lambda s: s.strip()})
attributeName = data.take(0,0)[:-1].tolist()
y = data[...,-1][1:]
X = data[...,:-1]
X = np.delete(X,0,0)

values = []
get_data(values)


#call recursive_split to train the decision tree
tree = recursive_split(X, y, attributeName, values)

satisfied_attributes = []
for i in range(len(X[0])):
    contengency = pd.crosstab(X.T[i], y)
    c, p, dof, expected = chi2_contingency(contengency)
    if c > chi2.isf(q=alpha, df=dof):
        satisfied_attributes.append(attributeName[i])


print('\nDecision tree before pruning-\n')
pprint(tree)

print ('\nDecision tree after pruning-\n')
pruned = True
while pruned:
    #keep pruning till leaf nodes can be pruned or till whole tree has been pruned
    pruned = False
    tree = pruneLeaves(tree)
    if tree == 'pruned':
        break
pprint(tree)
