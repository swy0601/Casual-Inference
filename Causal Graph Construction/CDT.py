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


data = pd.read_csv("exp_merge_mix.csv")
top_feature_list = ['Readable', 'BW-Avg-number-of-identifiers', 'BW-Avg-comments', 'BW-Max-indentation',
        'BW-Max-char', 'BW-Avg-periods', 'BW-Avg-Assignment', 'BW-Max-line-length',
        'New-Semantic-Text-Coherence-Standard-@-0.1', 'BW-Avg-Identifiers-Length', "New-Number-of-senses-AVG",
                    'BW-Max-Single-identifiers', 'BW-Max-number-of-identifiers']


# 得到所有的feature name
feature_list = []
for row in data:
    feature_list.append(row)


#
for element in feature_list:
    if element not in top_feature_list:
        data.drop([element], axis=1, inplace=True)


print(data.head())

# Finding the structure of the graph
# 确认骨架
# glasso = cdt.independence.graph.Glasso()
# skeleton = glasso.predict(data)


# 用PC算法确认骨架
model = cdt.causality.graph.PC()
skeleton = model.predict(data)

# output_graph = skeleton

# Pairwise setting
# 确认方向
# ANM方法是添加单向噪音来区别因和果
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





