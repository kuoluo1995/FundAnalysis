import json
import os

with open('data/good_funds.json', 'r') as fp:
    good_fund = json.load(fp)
print(len(good_fund))