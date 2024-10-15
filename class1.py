import pandas as pd

data = pd.read_excel('Data/1-SEEG10_GERAL-BR_UF_2022.10.27-FINAL-SITE.xlsx', sheet_name = 'GEE Estados')

print(data.head())
print(data.info())

print(data['Emissão / Remoção / Bunker'].unique())

filter_data_1 = data[data['Emissão / Remoção / Bunker'].isin([['Remoção NCI', 'Remoção']])]
check_negative_values_filter_data_1 = filter_data_1.loc[:, 1970:2021].max()

filter_data_2 = data.loc[data['Emissão / Remoção / Bunker'] == 'Bunker', 'Estado'].unique()

data = data[data['Emissão / Remoção / Bunker'] == 'Emissão']
data = data.drop(columns = 'Emissão / Remoção / Bunker')