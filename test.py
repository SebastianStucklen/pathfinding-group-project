import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 1. Prepare your data dictionary
data_dict = {
    'x_values': [1, 2, 3, 4, 5],
    'y_values': [2, 4, 5, 4, 6],
    'category': ['A', 'B', 'A', 'B', 'A']
}

# 2. Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data_dict)

print(df)
