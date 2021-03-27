
import pandas
import encodings
import json
excel_data_df = pandas.read_excel('groupparse.xlsx', sheet_name='TDSheet')

json_str = excel_data_df.to_json()
str = json.dumps(json_str, ensure_ascii=False, indent=4)
print('Excel Sheet to JSON:\n', json.loads(str))
