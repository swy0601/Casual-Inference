# This is the code for the essay "**What makes a readable code? A causal analysis method**".



The experiments in this thesis consist of the following three main parts including the production of the dataset, the construction of the causal graph and the causal inference part.



## Dataset Construction

This part of the experiment involves three packages including **Dataset** (P<sub>Dataset</sub>), **Data Construction** (P<sub>Data Construction</sub>), and **Result** (P<sub>Result</sub>). 

In the P<sub>Dataset</sub>, we show the code snippets we used in our experiments including D<sub>Buse</sub>, D<sub>Scalabrino</sub>, and D<sub>Dorn</sub>. Since D<sub>Dorn</sub> includes three types of code snippets (Java, Python, and Cuda), we treat D<sub>Dorn</sub> separately. The files **"BuseAndSc.csv"** and **"Dorn.csv"** are used to record the values of different features in different code snippets. Since Scalabrino et al. has already provided the dataset on his own proposed features (as shown in the file **"feature_S.csv"**), we only need to compute the features proposed by Buse and Weimer. 

In the P<sub>Data Construction</sub>, we provide our code that uses the scrML tool to compute different features. The result of the calculation is stored in P<sub>Result</sub> (**"data_Dorn_all.csv"**, and **"data_java_all.csv"**). Note that since our experiments are conducted for Java, we distinguish the data in the **"data_Dorn_all.csv"** file by marking 0 for all non-Java code snippets. The dataset of all code snippets is stored in the P<sub>Result</sub> (**"normal_data.csv"**). To remove the non-Java data, we use the file "data_clear.py" in P<sub>Data Construction</sub> and the file is stored in the P<sub>Result</sub> (**"data_clear.csv"**). Finally, we merge files **"data_clear.csv"** in P<sub>Result</sub> and **"feature_S.csv"** in P<sub>Dataset</sub> to get the final dataset and store in the P<sub>Result</sub> (**"exp_merge_mix.csv"**).



## Causal Graph Construction

This part of the experiment mainly includes feature screening and causal graph construction. In the P<sub>Causal Graph Construction</sub>, we  provide a jupyter file **"DecisionTreeRegression.ipynb"** to show the results of feature selection, and we provide a code for causal graph generation (**"CDT.py"**).



## Causal Inference

This part of the experiment deals with inference of causal effects and robustness testing. The files **"Causal Effect.ipynb"** and **"Robustness Test Cal.py"** in P<sub>Causal Effect</sub> are used for calculating the causal effect and robustness testing.
