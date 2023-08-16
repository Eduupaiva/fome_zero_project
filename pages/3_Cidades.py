#=================================================================
#                 BIBLIOTECAS NECESSÁRIAS
#=================================================================

import pandas as pd
import re
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from haversine import haversine
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Cidades', page_icon='🏙', layout='wide' )

#=================================================================
#                 IMPORTAÇÃO DE DADOS
#=================================================================
df = pd.read_csv('zomato.csv')

df1 = df.copy()

#=================================================================
#                 LIMPEZA DE DADOS
#=================================================================

#Eliminando Valores Duplicados

df1 = df.drop_duplicates().copy()

# 1. Preenchimento dos nomes dos paises;

def country_name(country_id):

    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
  }

    return COUNTRIES[country_id]

# Incluindo o Country Name como coluna da tabela
df1['Country Name'] = df['Country Code'].map(country_name)

# 2. Criação do Tipo de categoria de comida;

def create_price_tye(price_range):
    if price_range == 1:        
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# 3.  Criação do nome das Cores

COLORS = {
  "3F7E00": "darkgreen",
  "5BA829": "green",
  "9ACD32": "lightgreen",
  "CDD614": "orange",
  "FFBA00": "red",
  "CBCBC8": "darkred",
  "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

# 4.  Renomear as colunas do DataFrame

def rename_columns(df1):        
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df

#Tranformar todos os restaurantes com apenas um tipo de culinaria
df1 = df1[df1["Cuisines"].notnull()].copy()
df1["Cuisines"] = df1.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

#Deixando os valores 1 e 0 como Yes or No
def table_booking (Has_Table_booking):
    if Has_Table_booking == 1:
        return "Yes"
    else:
        return "No"
#Aplicando a função à coluna "Has Table booking" e criando uma nova coluna "Booking Status"
df1['Booking Status'] = df1['Has Table booking'].apply(table_booking)
# Mapear os valores 0 e 1 para strings "Não" e "Sim" respectivamente
df1['Is delivering now'] = df1['Is delivering now'].map({0: 'Não', 1: 'Sim'})
#Deixando os valores 1 e 0 como Yes or No
df1['Has Online delivery'] = df1['Has Online delivery'].map({0: 'Não', 1: 'Sim'})

# ==============================================================================
#                        Barra Lateral no Streamlit
# ==============================================================================

st.header( 'Visão Cidades')

image_path = "logo.png"
image = Image.open(image_path)
st.sidebar.image( image, width=300 )

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")

# Pega os cinco primeiros países únicos da coluna 'Country Name' como valores padrão
default_countries = df1['Country Name'].unique()[:6]

selecao_paises = st.sidebar.multiselect( 
    'Escolha os Países que Deseja Visualizar os Restaurantes',
    df1['Country Name'].unique(),
    default= default_countries) 

st.sidebar.markdown("""---""")
st.sidebar.markdown("""### Powered by Eduardo""")

# Filtro de País
df1['Country Name'] = df1['Country Name'].str.strip()
linhas_selecionadas = df1['Country Name'].isin(selecao_paises)
df1 = df1.loc[linhas_selecionadas, :]



# ==============================================================================
#                          layout no Streamlit
# ==============================================================================


with st.container():
    
    st.markdown( '#### Top 10 Cidades com mais Restaurantes na Base de Dados' )
    rest_per_city = df1.loc[:,['City', 'Restaurant ID']].groupby(['City']).nunique().sort_values(['Restaurant ID'], ascending=False).reset_index()
    top10 = rest_per_city.head(10)
    
    fig = px.bar(top10, x='City', y='Restaurant ID', text_auto='.2s',color='City', labels={'City':'Cidade', 'Restaurant ID':'Quantidade De Restaurantes'})
    
    st.plotly_chart( fig )

with st.container():
    col1, col2 = st.columns (2, gap='large' )
    
    with col1:
        st.markdown( '#### Top 7 Cidades c/ Restaurantes c/ média de avaliação acima de 4' )
        restaurants_high_rate = df1[df1['Aggregate rating'] > 4].groupby('City')['Aggregate rating'].count().reset_index()

        # Ordenando pelo número de restaurantes (opcional)
        restaurants_high_rate = restaurants_high_rate.sort_values(['Aggregate rating'], ascending=False)
        top7 = restaurants_high_rate.head(7)
        
        fig = px.bar(top7, x='City', y='Aggregate rating', text_auto='.2s',color='City', labels={'City':'Cidade', 'Aggregate rating':'Quantidade De Restaurantes'})
        
        st.plotly_chart( fig, use_container_width=True )
    
    with col2:
        st.markdown( '#### Top 7 Cidades c/ Restaurantes c/ média de avaliação abaixo de 2.5' )
        restaurants_low_rate = df1[df1['Aggregate rating'] < 2.5].groupby('City')['Aggregate rating'].count()

        # Ordenando pelo número de restaurantes (opcional)
        restaurants_low_rate = restaurants_low_rate.sort_values(ascending=False).reset_index()
        top7 = restaurants_low_rate.head(7)
        
        fig = px.bar(top7, x='City', y='Aggregate rating', text_auto='.2s', color='City', labels={'City':'Cidade', 'Aggregate rating':'Quantidade De Restaurantes'})
        
        st.plotly_chart ( fig  )

with st.container():
    
    st.markdown( '### Top 10 Cidades mais restaurantes com tipos culinarios distintos' )
    city_per_cuisine = df1.loc[:, ['Cuisines', 'City']].groupby(['City']).nunique().sort_values(['Cuisines'], ascending=False).reset_index()
    top_sete = city_per_cuisine.head(7)
    
    fig = px.bar(top_sete, x='City', y='Cuisines', text_auto='.2s', color='Cuisines', labels={'City':'Cidade', 'Cuisines':'Quantidade De Tipos Culinarios'})
    
    st.plotly_chart( fig )
    