import pandas as pd

raw_data = pd.read_csv('./edu_sample_data.csv', encoding='big5')
s281 = raw_data[raw_data['PseudoID']==281]
s281_ans = s281.groupby(['dp001_video_item_sn', 'dp001_indicator'])['dp001_video_item_sn'].count()

print(s281_ans)