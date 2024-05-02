import csv
from fuzzywuzzy import process
import pandas as pd


g = pd.read_csv("/Users/alexforman/Documents/GitHub/UC-Investments/Data-Collection/final-fund-holdings/MSCI ACWI IMI TF EX‐TOB AND FF.csv")

print(g[0])