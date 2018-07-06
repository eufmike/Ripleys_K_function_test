## borrow from https://blog.csdn.net/howhigh/article/details/78007317
## np.random.binomial()
## np.random.poisson()
## np.random.exponential()
## np.random.normal()

#%%
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
# range between 0 and 1
N = 1000 # sample size
rdnumber_1 = np.random.rand(N)
print(rdnumber_1)

plt.hist(rdnumber_1, bins=100)
plt.title('histogram random test 01')
plt.show()

#%%
# binomial distribution
def plot_binomial(n,p):
    # Probability mass function (PMF)
    # create 10000 objects following binomial distribution
    sample = np.random.binomial(n,p,size=10000)  
    bins = np.arange(n+2) 
    plt.hist(sample, bins=bins, align='left', normed=True, rwidth=0.1) #plot histogram
    #set title 
    plt.title('Binomial PMF with n={}, p={}'.format(n,p))  
    plt.xlabel('number of successes')
    plt.ylabel('probability')

plot_binomial(10, 0.5)

#%%
# Poisson distribution
# Probability mass function (PMF)
# create 10000 objects following Poisson distribution
lamb = 6
sample = np.random.poisson(lamb, size=10000)
# sample.head()
bins = np.arange(20)
print(bins)
plt.hist(sample, bins=bins, align='left', rwidth=0.1, normed=True)
plt.title('Poisson PMF (lambda=6)')
plt.xlabel('number of arrivals')
plt.ylabel('probability')
plt.show()

#%%
# Exponential distribution (negative exponential distribution)
# Probability Density Function (PDF)
# create 10000 objects following exponential distribution

# plot histogram
tau = 10
sample = np.random.exponential(tau, size=10000)  
plt.hist(sample, bins=80, alpha=0.7, normed=True)
plt.margins(0.02) 

# plot PDF
lam = 1 / tau
x = np.arange(0,80,0.1)
y = lam * np.exp(- lam * x)
plt.plot(x,y,color='orange', lw=3)
plt.title('Exponential distribution, 1/lambda=10')
plt.xlabel('time')
plt.ylabel('PDF')
plt.show()

#%%
# standard normal distribution (negative exponential distribution)
def norm_pdf(x,mu,sigma):
    # Probability Density Function (PDF)
    pdf = np.exp( -((x - mu)**2)/(2* sigma**2)) / (sigma * np.sqrt(2*np.pi))    
    return pdf

mu = 0    # mean = 0
sigma = 1 # std = 1

# plot histogram
sample = np.random.normal(mu, sigma, size=10000)
plt.hist(sample, bins=100, alpha=0.7, normed=True)# 根据正态分布的公式绘制PDF曲线

# plot PDF
x = np.arange(-5, 5, 0.01)
y = norm_pdf(x, mu, sigma)
plt.plot(x,y, color='orange', lw=3)
plt.show()

## 2D simulation
# for Cartesian coordinate system
#%%
# 2D random distribution 
N = 1000 # sample size

rdn_x = 2 * np.random.rand(N) - 1
rdn_y = 2 * np.random.rand(N) - 1

plt.figure(figsize=(10,10))
plt.scatter(rdn_x, rdn_y)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()

#%%
# 2D normal distribution 
N = 1000 # sample size

mu = 0    # mean = 0
sigma = 0.25 # std

rdn_x = np.random.normal(mu, sigma, size = N)
rdn_y = np.random.normal(mu, sigma, size = N)
plt.figure(figsize=(10,10))
plt.scatter(rdn_x, rdn_y)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()

#%%
# Poisson distribution
# Probability mass function (PMF)
# create 10000 objects following Poisson distribution
lamb = 6
sample = np.random.poisson(lamb, size=10000)
print(sample[range(10)])

#%%
# sample.head()
bins = np.arange(20)
plt.hist(sample, bins=bins, normed=True)
plt.title('Poisson PMF (lambda=6)')
plt.xlabel('number of arrivals')
plt.ylabel('probability')
plt.show()





#%%
## 2D simulation
# for Polar coordinate system

# 2D random distribution 
N = 1000 # sample size

rdn_r = np.random.rand(N) # the range of radius
theta = 2 * np.pi * np.random.rand(N)
colors = theta

fig = plt.figure(figsize=(10,10))
ax = plt.subplot(111, projection='polar')
ax.scatter(theta, rdn_r, c = colors, cmap='hsv')
ax.set_rmax(1)
plt.show()