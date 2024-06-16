import pandas as pd

# Example Series
s = pd.Series([10, 20, 30, 40, 50])
value_to_find = 30
if value_to_find in s.values:
    print(f"{value_to_find} is present in the Series.")
else:
    print(f"{value_to_find} is not present in the Series.")
