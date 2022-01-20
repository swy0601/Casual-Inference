import pandas as pd


data = pd.read_csv('../Result/normal_data.csv')
index = data[data['score'] == 0].index
data.drop(index, axis = 0, inplace= True)
data.to_csv("../Result/data_clear.csv", index=False)

