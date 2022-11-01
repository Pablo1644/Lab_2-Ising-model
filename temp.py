import pandas as pd
import numpy as np
from time import sleep
from tqdm import tqdm,trange

# https://www.youtube.com/watch?v=n4E7of9BINo&t=107s

dogs = np.random.choice(['labrador','owczarek','york'],size = 100)
smell = np.random.randint(0,100,size=100)
df = pd.DataFrame(data=np.array([dogs,smell]).T,columns=['dog','smell'])

for dogs in tqdm(dogs):
    sleep(0.000001)
print(df.head())

for i in trange(0,50):
    sleep(0.1)
print('done')

