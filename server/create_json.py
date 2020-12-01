import json
from server import fund_market

ProjectPath = '/home/kuoluo/projects/FundAnalysis/data/explore'

data1 = fund_market.get_market_sector_value()
sector_date_value = {}
for sector,values in data1.items():
    sector_date_value[sector] = {}
    for date, num in values.items():
        year = str(date)[0:4]
        if year not in sector_date_value[sector]:
            sector_date_value[sector][year] = 0
        sector_date_value[sector][year] = round((num/10000),2) # 万为单位
with open(ProjectPath + '/sector_date_value.json', 'w') as wp:
    json.dump(sector_date_value, wp)
print('over')