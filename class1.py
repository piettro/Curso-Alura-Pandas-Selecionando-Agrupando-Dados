import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

gas_emission = pd.read_excel('Data/1-SEEG10_GERAL-BR_UF_2022.10.27-FINAL-SITE.xlsx', sheet_name = 'GEE Estados')
print(gas_emission.head())
print(gas_emission.info())
print(gas_emission.describe())

print(gas_emission['Emissão / Remoção / Bunker'].unique())
print(gas_emission[gas_emission['Emissão / Remoção / Bunker'].isin(['Remoção NCI', 'Remoção'])])
print(gas_emission.loc[gas_emission['Emissão / Remoção / Bunker'].isin(['Remoção NCI', 'Remoção']), 1970:2021])
print(gas_emission.loc[gas_emission['Emissão / Remoção / Bunker'].isin(['Remoção NCI', 'Remoção']), 1970:2021].max())
print(gas_emission.loc[gas_emission['Emissão / Remoção / Bunker'] == 'Bunker', 'Estado'].unique())

gas_emission = gas_emission[gas_emission['Emissão / Remoção / Bunker'] == 'Emissão']
gas_emission = gas_emission.drop(columns = 'Emissão / Remoção / Bunker')

#Modify Dataframe format
columns_info = list(gas_emission.loc[:,'Nível 1 - Setor':'Produto'].columns)
columns_emission = list(gas_emission.loc[:,1970:2021].columns)
emission_per_year = gas_emission.melt(id_vars = columns_info, value_vars = columns_emission, var_name = 'Ano' , value_name = 'Emissão')

print(emission_per_year.groupby('Gás'))
print(emission_per_year.groupby('Gás').groups)
print(emission_per_year.groupby('Gás').get_group('CO2 (t)'))
print(emission_per_year.groupby('Gás').sum())

emission_per_gas = emission_per_year.groupby('Gás').sum().sort_values('Emissão', ascending = False)
emission_per_gas.plot(kind = 'barh', figsize = (10,6))
plt.show()

print(f'A emissão de CO2 corresponde a {float(emission_per_gas.iloc[0:9].sum()/emission_per_gas.sum())*100:.2f} % de emissão total de gases estufa no Brasil de 1970 a 2021.')

#Emissao de gas por setor
gas_per_sector = emission_per_year.groupby(['Gás', 'Nível 1 - Setor']).sum()

print(gas_per_sector.xs('CO2 (t)', level = 0))
print(gas_per_sector.xs(('CO2 (t)', 'Mudança de Uso da Terra e Floresta'), level = [0,1]))
print(gas_per_sector.xs('CO2 (t)', level = 0).max())
print(gas_per_sector.xs('CO2 (t)', level = 0).idxmax())
print(gas_per_sector.groupby(level = 0).idxmax())
print(gas_per_sector.groupby(level = 0).max())

max_values = gas_per_sector.groupby(level = 0).max().values
summarized_table = gas_per_sector.groupby(level = 0).idxmax()
summarized_table.insert(1, 'Quantidade de emissão', max_values)

print(gas_per_sector.swaplevel(0, 1).groupby(level = 0).idxmax())

#Emissao ao longo dos anos
emission_per_year.groupby('Ano').mean().plot(figsize = (10,6))
plt.show()

anual_emission_mean = emission_per_year.groupby(['Ano', 'Gás']).mean().reset_index()
anual_emission_mean = anual_emission_mean.pivot_table(index = 'Ano', columns = 'Gás', values = 'Emissão')

anual_emission_mean.plot(subplots = True, figsize = (10,40))
plt.show()

#Unindo dados
states_population = pd.read_excel('Data/POP2022_Municipios.xls', header = 1, skipfooter = 34)
print(states_population.head())
print(states_population.info())
print(states_population.describe())

states_population = states_population.assign(
    population_without_parathesis = states_population['POPULAÇÃO'].str.replace('\(\d{1,2}\)', '',regex=True),
    population = lambda x : x.loc[:,'population_without_parathesis'].str.replace('\.','',regex=True)
)
states_population['population'] = states_population['population'].astype(int)
states_population = states_population.groupby('UF').sum(numeric_only=True).reset_index()
print(states_population.head())

emission_per_state = emission_per_year[emission_per_year['Ano'] == 2021].groupby('Estado')[['Emissão']].sum().reset_index()
print(emission_per_state.head())

agr_data = pd.merge(emission_per_state, states_population, left_on = 'Estado', right_on = 'UF')
agr_data.plot(x = 'populacao', y= 'Emissão', kind = 'scatter', figsize=(8,6))
plt.show()

agr_data = agr_data.assign(emissao_per_capita = agr_data['Emissão']/agr_data['populacao']).sort_values('emissao_per_capita', ascending = False)
px.scatter(data_frame = agr_data, x = 'populacao', y = 'Emissão', text = 'Estado', opacity = 0)
plt.show()
px.bar(data_frame = agr_data, x = 'Estado', y = 'emissao_per_capita')
plt.show()
px.scatter(data_frame = agr_data, x = 'populacao', y = 'Emissão', text = 'Estado', size = 'emissao_per_capita')
plt.show()