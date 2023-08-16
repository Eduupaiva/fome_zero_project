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
from folium.plugins import MarkerCluster

st.set_page_config( page_title='Visão Geral', page_icon='📊', layout='wide' )

#=================================================================
#                 IMPORTAÇÃO DE DADOS
#=================================================================
df = pd.read_csv(r'C:\Users\dudup\Documents\Comunidade Ds\Projeto Do Aluno\zomato.csv')

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

st.header( 'Fome Zero')

#image_path = r'C:\Users\dudup\Documents\Comunidade Ds\Projeto Do Aluno\logo.jpg'
image_path = "logo.png"
image = Image.open(image_path)
st.sidebar.image( image, width=300 )

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")

default_countries = df1['Country Name'].unique()[:10]
selecao_paises = st.sidebar.multiselect( 
    'Escolha os Países que Deseja Visualizar os Restaurantes',
    df1['Country Name'].unique(),default= default_countries) 
    

st.sidebar.markdown("""---""")
st.sidebar.markdown("""### Powered by Eduardo""")

# Filtro de País
df1['Country Name'] = df1['Country Name'].str.strip()
linhas_selecionadas = df1['Country Name'].isin(selecao_paises)
df1 = df1.loc[linhas_selecionadas, :]


# ==============================================================================
#                          layout no Streamlit
# ==============================================================================

tab1 = st.markdown('#### O Melhor lugar para encontrar seu mais novo restaurante favorito!')

with st.container():
    st.markdown( '##### Temos as seguintes marcas dentro da nossa plataforma')
                
    col1, col2, col3, col4, col5 = st.columns( 5 )

    with col1:

        # Restaurantes Cadastrados
        restaurantes_unicos = len( df1.loc[:, 'Restaurant ID'].unique() )
        col1.metric('Restaurantes Cadastrados', restaurantes_unicos)

    with col2:

        #Paises Cadastrados
        paises_unicos = len( df1.loc[:, 'Country Code'].unique() )
        col2.metric( 'Paises Cadastrados', paises_unicos)

    with col3:

        # Cidades Cadastradas
        cidades_unicas = len( df1.loc[:, 'City'].unique() )
        col3.metric('Cidades Cadastradas', cidades_unicas)

    with col4:

        #Avaliações Feitas na Plataforma
        avaliacoes_feitas = df1.loc[:, 'Votes'].sum()
        avaliacoes_feitas = '{:,.0f}'.format( avaliacoes_feitas).replace(',', '.')
        col4.metric('Avaliações Feitas na Plataforma',  avaliacoes_feitas)


    with col5:
        
        #Tipos de Culinarias Oferecidas
        unique_cuisines = set()  # Cria um conjunto vazio para armazenar os tipos de culinária únicos
        for cuisines in df1['Cuisines']:
            if isinstance(cuisines, str):  # Verifica se o valor é uma string (ignora valores nulos)
                cuisines_list = cuisines.split(', ')  # Divide as culinárias em uma lista
                unique_cuisines.update(cuisines_list)  # Adiciona as culinárias únicas ao conjunto

        total_unique_cuisines = len(unique_cuisines)  # Calcula o total de tipos de culinária únicos
        col5.metric('Tipos de Culinarias Oferecidas',total_unique_cuisines)

        
with st.container():    
    
    top10_rest = df1.loc[:,['Restaurant ID','Restaurant Name','Country Name', 'City','Cuisines', 'Average Cost for two', 'Aggregate rating', 'Votes','Latitude', 'Longitude' ]].sort_values(by=['Aggregate rating'], ascending=[False])
    # Criar o mapa
    map = folium.Map()
    # Criar um cluster de marcadores
    marker_cluster = MarkerCluster().add_to(map)
    # Iterar sobre os dados e adicionar marcadores ao cluster
    for index, location_info in top10_rest.iterrows():    
        popup_text = f"City: {location_info['City']}<br>Restaurant: {location_info['Restaurant Name']}"
        folium.Marker(
            location=[location_info['Latitude'], location_info['Longitude']],
            popup=popup_text
        ).add_to(marker_cluster)
    
    
    folium_static( map, width=1024, height=600)
    
   
            
            
            

