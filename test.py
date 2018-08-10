
# %%
import numpy as np
x = np.zeros((7, 2))
y = np.array([[1,2], [3, 4], [5, 6], [7, 8]])
print(y)
condlist = [y[:, 0]<3, y[:, 1]>5]
np.select(condlist, y)

# %%
x = np.arange(10)
condlist = [x<3, x>5]
choicelist = [x, x**2]
np.select(condlist, choicelist)
print(condlist)
print(choicelist)

# %%
a = [1,2,3]
b = [3,2,1]
arepeat = np.repeat(a, b)
print(arepeat)
# %%
# import time
import tqdm
import time

for i in tqdm.trange(100):
    time.sleep(0.02)