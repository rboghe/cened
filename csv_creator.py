import pandas as pd

# Load files
cened2 = pd.read_csv('Database_CENED_2_-_Certificazione_ENergetica_degli_EDifici.csv') 
cened12 = pd.read_csv('CENED___Certificazione_ENergetica_degli_EDifici.csv')

# Drop partial entries
cened2 = cened2[cened2['INTERO_EDIFICIO'] == True]

# Fix data types in cened 1.2
cened12['SUPERFICIE_DISPERDENTE'] = cened12['SUPERFICIE_DISPERDENTE'].str.replace(r',', '')
cened12['SUPERFICIE_DISPERDENTE'] = cened12['SUPERFICIE_DISPERDENTE'].astype(float)

# Drop NaN 
cened2 = cened2.dropna(subset=['COMUNE','FOGLIO', 'PARTICELLA','SUPERFICIE_DISPERDENTE'])
cened12 = cened12.dropna(subset=['COMUNE','FOGLIO', 'PARTICELLA','SUPERFICIE_DISPERDENTE'])

# Merge dfs
cenedtot = pd.merge(left=cened2, right=cened12, left_on=['COMUNE','FOGLIO', 'PARTICELLA'], right_on=['COMUNE','FOGLIO', 'PARTICELLA'],  how='inner')

# Drop renovations
cenedtot = cenedtot[cenedtot['RISTRUTTURAZIONE_IMPORTANTE'] == False]
cenedtot = cenedtot[cenedtot['RIQUALIFICAZIONE_ENERGETICA'] == False]

# Compute difference between ext surfaces
cenedtot['surfdiff'] = abs((cenedtot['SUPERFICIE_DISPERDENTE_x'] - cenedtot['SUPERFICIE_DISPERDENTE_y'])/cenedtot['SUPERFICIE_DISPERDENTE_x'])

# Drop rows with high difference
cenedtot = cenedtot[cenedtot['surfdiff'] < 0.05]

cenedtot.to_csv('cened_joined.csv')