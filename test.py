
# %%
import numpy as np
x = np.zeros((7, 2))
y = np.array([[1,2], [3, 4]])
print(x)
print(y)
x[1:3] = y

print(x)

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