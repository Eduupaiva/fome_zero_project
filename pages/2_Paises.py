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

st.set_page_config( page_title='Países', page_icon='🌍', layout='wide' )

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

st.header( 'Visão Países')

#image_path = r'C:\Users\dudup\Documents\Comunidade Ds\Projeto Do Aluno\logo.jpg'
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
    col1, col2 = st.columns ( 2, gap='large' )
    with col1:        
        st.markdown( '#### Quantidade de Restaurantes Registrados por País' )
        #Fazendo o agrupamento de paises e contando o numero de cidades registradas
        df_aux = df1.loc[:,['Restaurant ID', 'Country Name']].groupby(['Country Name']).nunique().sort_values(['Restaurant ID'], ascending=False).reset_index()

        fig = px.bar(df_aux, x='Country Name', y='Restaurant ID', text_auto='.2s', color='Country Name', labels={'Country Name':'Paises', 'Restaurant ID':'Quantidade De Restaurantes'})

        st.plotly_chart( fig )

    with col2:
        st.markdown( '#### Quantidade de Cidades Resgistrados por País' )
        #Fazendo o agrupamento de paises e contando o numero de cidades registradas
        country_by_city = df1.loc[:,['City', 'Country Name']].groupby(['Country Name']).nunique().sort_values(['City'], ascending=False).reset_index()

        fig = px.bar(country_by_city, x='Country Name', y='City', text_auto='.2s', color='Country Name', labels={'Country Name':'Paises', 'City':'Quantidade De Cidades'})

        st.plotly_chart( fig )

with st.container():
    col1, col2 = st.columns (2, gap='large' )
    with col1:
        st.markdown( '#### Média de Avaliações Feitas por Paíse' )
        #Fazendo o agrupamento de paises e contando o numero de avaliações registradas
        country_by_votes = df1.loc[:,['Votes', 'Country Name']].groupby(['Country Name']).mean().sort_values(['Votes'], ascending=False).reset_index()
        
        fig = px.bar(country_by_votes, x='Country Name', y='Votes', text_auto='.2s', color='Country Name',labels={'Country Name':'Paises', 'Votes':'Quantidade De Avaliações'})
        
        st.plotly_chart( fig, use_container_width=True )
        
    with col2:
        st.markdown( '#### Média de Preço de um prato para duas pessoas p/ País' )
        avg_cost_for_two = df1.loc[:, ['Average Cost for two', 'Country Name']].groupby(['Country Name']).mean(['Average Cost for two']).sort_values(['Average Cost for two'], ascending=False).reset_index()
        
        fig = px.bar(avg_cost_for_two, x='Country Name', y='Average Cost for two', text_auto='.2s', color='Country Name', labels={'Country Name':'Paises', 'Average Cost for two':'Preço Do Prato para Duas Pessoas'})
        
        st.plotly_chart( fig )


