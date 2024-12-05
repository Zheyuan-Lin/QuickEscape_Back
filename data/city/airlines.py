import pandas as pd

df = pd.read_csv('data_raw/airlines.csv',
                 na_values=['', 'NULL', 'UNKNOWN', 'Unknown', '-', '..'],
                 keep_default_na=False)

# Filter rows
df = df[df['Active'] == 'Y']
df = df.dropna(subset=['IATA', 'ICAO'])

# Select columns
df = df[['Name', 'IATA', 'ICAO', 'Country']]

# Rename columns
df = df.rename(columns={
    'Name': 'airline_nm',
    'IATA': 'airline_cd',
    'ICAO': 'icao_cd',
    'Country': 'country_nm',
})

# Remove rows
# Where airline_cd is null or not a two character string made up with numbers or A-Z
df = df[df['airline_cd'].str.match(r'^[A-Z0-9]{2}$')]

# Where icao_cd is null or not a three character string made up with numbers or A-Z
df = df[df['icao_cd'].str.match(r'^[A-Z0-9]{3}$')]

# Strip values
df['airline_cd'] = df['airline_cd'].str.strip()
df['icao_cd'] = df['icao_cd'].str.strip()

# Export to CSV
df.to_csv('data_processed/airlines.csv', index=False)