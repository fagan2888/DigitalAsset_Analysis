import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
              'col1': list(range(1, 10)), \
              'col2': list(range(10, 19)) \
              })

print(np.log(df['col1']).diff())
