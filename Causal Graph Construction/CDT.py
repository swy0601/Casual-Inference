import cdt
from cdt import SETTINGS
import pandas as pd
from pandas import Series

SETTINGS.verbose = True
#SETTINGS.NJOBS = 16
#SETTINGS.GPU = 1
import networkx as nx
import matplotlib.pyplot as plt
plt.axis('off')

# Load data
data = pd.read_csv('../Result/data_clear.csv')



list = ['score', 'avg_comment', 'avg_identifier', 'max_indentation',
        'max_single_char', 'avg_dot', 'avg_keyword', 'avg_bracket',
        'avg_if', 'avg_assignment', 'avg_comparison']


data.drop(['id'],axis = 1, inplace = True)
index = data[data['score'] == 0].index
data.drop(index, axis = 0, inplace= True)

name_list = ['avg_identifier_length','max_identifier_length','avg_identifier','max_identifier','max_single_identifier'
        ,'avg_arithmetic','avg_comparison','avg_assignment','avg_comma','avg_dot','avg_bracket','max_keyword'
        ,'avg_keyword','max_number','avg_number','avg_loop','avg_if','avg_space','max_indentation'
        ,'avg_indentation','avg_comment','max_single_char','avg_blank','max_line_length','avg_line_length'
        ,'score'
       ]

for element in name_list:
    if element not in list:
        data.drop([element], axis=1, inplace=True)


print(data.head())

# Finding the structure of the graph
# glasso = cdt.independence.graph.Glasso()
# skeleton = glasso.predict(data)


# PC Algorithm
model = cdt.causality.graph.PC()
skeleton = model.predict(data)

# Additive Noise Models
model = cdt.causality.pairwise.ANM()
output_graph = model.predict(data, skeleton)


# Visualize causality graph
options = {
        "node_color": "#A0CBE2",
        "width": 1,
        "node_size":600,
        "edge_cmap": plt.cm.Blues,
        "with_labels": True,
    }

nx.draw_networkx(output_graph, nx.shell_layout(output_graph), **options)
# plt.savefig("result.png")
plt.show()





