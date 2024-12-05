import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

# Load
df = pd.read_csv('data_raw/airports_1.csv', na_values=['', 'NULL'], keep_default_na=False)
city_code_df = pd.read_csv('data_raw/airports_2.csv')

# Rename columns
df = df.rename(columns={
    'name': 'airport_nm',
    'latitude_deg': 'latitude',
    'longitude_deg': 'longitude',
    'iso_country': 'country_cd',
    'iso_region': 'region_cd',
    'municipality': 'city_nm',
    'iata_code': 'airport_cd'
})

# Filter
df = df[df['scheduled_service'] == 'yes']
df = df[df['type'].isin(['large_airport'])]
df = df[df['continent'].isin(['NA']) | df['country_cd'].isin(['US', 'CA', 'MX'])]
df = df.dropna(subset=['airport_cd'])

# Exclude some airports
df = df[~df['country_cd'].isin(['CU'])]
df = df[~df['airport_cd'].isin(['OMA', 'SDF', 'LRM', 'DGO'])]

# Join city_cd
city_code_df = city_code_df.rename(columns={'code': 'airport_cd', 'city_code': 'city_cd', 'time_zone': 'timezone'})
df = pd.merge(df, city_code_df[['airport_cd', 'city_cd', 'timezone']], on='airport_cd', how='left')

# Join attributes
attributes_map = {
    "YEG": ["city", "nature"],
    "YHZ": ["coastal", "history", "nature"],
    "YOW": ["city", "history", "culture"],
    "YQB": ["city", "history", "culture", "nature"],
    "YUL": ["city", "culture", "foodie", "shopping"],
    "YVR": ["city", "coastal", "nature", "foodie", "tech"],
    "YWG": ["city", "nature"],
    "YYC": ["city", "nature", "culture"],
    "YYT": ["coastal", "nature", "history"],
    "YYZ": ["city", "culture", "shopping", "tech"],
    "ABQ": ["nature", "culture"],
    "ATL": ["city", "foodie", "tech", "culture"],
    "AUS": ["city", "foodie", "tech"],
    "BDL": ["history", "nature"],
    "BNA": ["city", "culture", "foodie", "nature"],
    "BOS": ["city", "history", "culture", "shopping", "tech", "foodie"],
    "BUF": ["nature", "history"],
    "BWI": ["city", "history", "coastal"],
    "CLE": ["city", "nature"],
    "CLT": ["city", "foodie"],
    "CMH": ["city", "nature"],
    "CVG": ["city", "culture"],
    "DCA": ["city", "history", "culture", "foodie", "shopping"],
    "DEN": ["city", "nature", "tech"],
    "DFW": ["city", "shopping", "tech", "culture"],
    "DTW": ["city", "tech", "history"],
    "EWR": ["city", "shopping", "tech", "foodie", "culture", "history"],
    "FLL": ["coastal", "resort", "shopping"],
    "IAD": ["city", "history", "shopping", "culture", "foodie"],
    "IAH": ["city", "tech", "shopping", "culture", "foodie"],
    "IND": ["nature", "history"],
    "JAX": ["coastal", "nature"],
    "JFK": ["city", "shopping", "tech", "foodie", "culture", "history"],
    "LAS": ["city", "resort", "shopping", "tech"],
    "LAX": ["city", "foodie", "tech", "shopping", "culture", "nature"],
    "LGA": ["city", "shopping", "tech", "foodie", "culture", "history"],
    "MCI": ["city", "history"],
    "MCO": ["city", "resort", "shopping", "culture"],
    "MDW": ["city", "tech", "shopping"],
    "MEM": ["city", "culture", "history"],
    "MIA": ["city", "coastal", "foodie", "shopping"],
    "MKE": ["city", "culture", "foodie"],
    "MSP": ["city", "nature", "culture"],
    "MSY": ["city", "foodie", "culture", "history"],
    "OAK": ["city", "coastal", "tech"],
    "OKC": ["city", "nature"],
    "OMA": ["nature", "history"],
    "ONT": ["city", "foodie", "tech", "shopping", "culture", "nature"],
    "ORD": ["city", "shopping", "tech"],
    "ORF": ["coastal", "history"],
    "PBI": ["coastal", "resort"],
    "PDX": ["city", "nature", "foodie", "tech"],
    "PHL": ["city", "history", "culture", "shopping"],
    "PHX": ["city", "nature", "resort"],
    "PIT": ["city", "history", "tech"],
    "PVD": ["coastal", "history"],
    "PWM": ["coastal", "nature"],
    "RDU": ["city", "tech"],
    "RIC": ["history", "culture"],
    "RNO": ["resort", "nature"],
    "RSW": ["coastal", "resort"],
    "SAN": ["city", "coastal", "nature", "foodie"],
    "SAT": ["city", "culture", "history"],
    "SAV": ["coastal", "history", "foodie"],
    "SDF": ["city", "history", "culture"],
    "SEA": ["city", "tech", "foodie", "nature"],
    "SFB": ["coastal", "resort"],
    "SFO": ["city", "tech", "foodie", "culture", "nature"],
    "SJC": ["city", "tech", "shopping"],
    "SLC": ["city", "nature", "tech"],
    "SMF": ["city", "nature", "nature"],
    "SNA": ["city", "foodie", "tech", "shopping", "culture", "nature"],
    "SRQ": ["coastal", "resort"],
    "STL": ["city", "history", "culture"],
    "SYR": ["city", "nature"],
    "TPA": ["coastal", "resort", "foodie"],
    "TUL": ["city", "nature"],
    "PLS": ["resort", "coastal"],
    "LRM": ["resort", "coastal"],
    "PUJ": ["resort", "coastal"],
    "SDQ": ["city", "history", "culture"],
    "GUA": ["city", "history", "nature"],
    "KIN": ["city", "coastal", "history"],
    "CZM": ["coastal", "resort"],
    "DGO": ["nature", "history"],
    "GDL": ["city", "culture", "foodie"],
    "MID": ["city", "history", "culture"],
    "MEX": ["city", "history", "tech", "foodie"],
    "MTY": ["city", "culture", "tech"],
    "MZT": ["coastal", "resort"],
    "PVR": ["coastal", "resort"],
    "SJD": ["coastal", "resort"],
    "NLU": ["city", "history"],
    "TIJ": ["coastal", "city"],
    "CUN": ["coastal", "resort"],
    "PTY": ["city", "shopping"],
    "LIR": ["coastal", "nature", "resort"],
    "SAL": ["city", "history"],
    "PAP": ["city", "history"],
    "HAV": ["city", "history", "culture", "foodie"],
    "VRA": ["coastal", "resort"],
    "GCM": ["coastal", "resort"],
    "NAS": ["coastal", "resort"],
    "BZE": ["coastal", "nature", "history"],
    "ANC": ["nature", "history", "culture"],
    "HNL": ["city", "coastal", "resort", "nature"],
    "OGG": ["coastal", "resort", "foodie"],
    "AEP": ["city", "history"],
    "EZE": ["city", "culture", "shopping"],
    "BEL": ["coastal", "nature"],
    "BSB": ["city", "history", "tech"],
    "CNF": ["city", "culture"],
    "MAO": ["nature", "culture"],
    "FLN": ["coastal", "resort"],
    "FOR": ["coastal", "resort"],
    "GIG": ["city", "coastal", "foodie", "culture"],
    "GRU": ["city", "culture", "foodie", "tech"],
    "BPS": ["coastal", "resort"],
    "SSA": ["city", "history", "culture"],
    "VIX": ["coastal", "city"],
    "SCL": ["city", "history", "culture"],
    "GYE": ["city", "coastal"],
    "UIO": ["city", "history", "culture"],
    "ASU": ["city", "history"],
    "ENO": ["city", "nature"],
    "AGT": ["nature", "city"],
    "BOG": ["city", "history", "culture"],
    "VVI": ["city", "nature"],
    "PBM": ["city", "nature"],
    "CAY": ["coastal", "nature"],
    "LIM": ["city", "history", "foodie"],
    "CUZ": ["history", "nature"],
    "MVD": ["city", "history", "coastal"],
    "BLA": ["coastal", "nature"],
    "CCS": ["city", "history"],
    "FDF": ["coastal", "city"],
    "PTP": ["coastal", "resort"],
    "SJU": ["coastal", "resort", "foodie"],
    "UVF": ["coastal", "resort"],
    "AUA": ["coastal", "resort"],
    "BON": ["coastal", "resort"],
    "CUR": ["coastal", "resort"],
    "SXM": ["coastal", "resort"]
}

attributes_df = pd.DataFrame(attributes_map.items(), columns=['airport_cd', 'attributes'])
df = df.merge(attributes_df, on='airport_cd', how='left')
df['attributes'] = df['attributes'].apply(lambda x: ', '.join(x))

# Only keep the columns we need
df = df[['airport_cd', 'airport_nm', 'city_nm', 'city_cd', 'country_cd', 'region_cd', 'timezone', 'latitude', 'longitude', 'attributes']]

# Sort
df = df.sort_values(by=['country_cd', 'region_cd', 'city_cd', 'airport_cd'])

df.to_csv('data_processed/airports.csv', index=False)
print("Done")

# print all unique attributes options in col attributes
attributes_set = set()
for index, row in df.iterrows():
    for attribute in row['attributes'].split(', '):
        attributes_set.add(attribute)

print(attributes_set)
