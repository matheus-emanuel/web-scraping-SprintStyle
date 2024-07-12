import pandas as pd
from datetime import datetime

# Carregando o arquivo do mercado livre
df_mercado_livre = pd.read_json('../../data/raw_data/data_mercado_livre.json')


# Transformar as colunas
df_mercado_livre['old_price'] = df_mercado_livre['old_price'].fillna(0).astype(float)
df_mercado_livre['old_price_cents'] = df_mercado_livre['old_price_cents'].fillna(0).astype(float)

df_mercado_livre['new_price'] = df_mercado_livre['new_price'].fillna(0).astype(float)
df_mercado_livre['new_price_cents'] = df_mercado_livre['new_price_cents'].fillna(0).astype(float)

# Juntar as colunas de preço antigo em uma só
df_mercado_livre['old_price'] = df_mercado_livre['old_price'] + df_mercado_livre['old_price_cents'] / 100

# Juntar as colunas de preço novo em uma só
df_mercado_livre['new_price'] = df_mercado_livre['new_price'] + df_mercado_livre['new_price_cents'] / 100

# Tranformar e ajustar a coluna reviews_amount
df_mercado_livre['reviews_amount'] = df_mercado_livre['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df_mercado_livre['reviews_amount'] = df_mercado_livre['reviews_amount'].fillna(0).astype(int)

# Inserir a coluna de source_data
df_mercado_livre['source_data'] = 'Mercado Livre'

# Inserir a coluna de source_page
df_mercado_livre['source_page'] = 'https://lista.mercadolivre.com.br/tenis-corrida-masculino'

# Inserir a coluna de process_datetime
df_mercado_livre['process_datetime'] = datetime.now()

# Dropar as colunas desnecessárias
df_mercado_livre = df_mercado_livre.drop(columns=['old_price_cents', 'new_price_cents'])

df_mercado_livre.to_json('../../data/clean_data/data_mercado_livre.json')
