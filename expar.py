import pandas as pd
from pprint import pprint

cols = [1, 3]

stud = pd.read_excel('stud_25.04.2021.xlsx')

s1 =(stud['39-55'].tolist())
pprint(s1)