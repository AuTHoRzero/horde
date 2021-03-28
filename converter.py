import pprint
import pandas
import json

data = pandas.read_excel('groupparse.xlsx', sheet_name='TDSheet')
pprint.pprint (json.loads(data.to_json()))
