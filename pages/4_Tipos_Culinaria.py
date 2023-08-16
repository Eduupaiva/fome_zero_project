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

st.set_page_config( page_title='Tipos de Culinária', page_icon='🍽', layout='wide' )

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

st.header( 'Visão Tipos de Culinárias')

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

# Filtro de País
df1['Country Name'] = df1['Country Name'].str.strip()
linhas_selecionadas = df1['Country Name'].isin(selecao_paises)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""---""")

# Filtro de Restaurantes

st_slider = st.sidebar.slider(
    'Selecione uma a quantidade de Restaurantes que deseja visualizar?',
    value= 10,
    min_value= 1,
    max_value= 20,
)


# Primeiro, vamos calcular a média de avaliação dos restaurantes
restaurant_avg_ratings = df1.groupby('Restaurant ID')['Aggregate rating'].mean().reset_index()

# Agora, selecionamos os restaurantes que estão entre as melhores médias de avaliação
#selected_restaurants = df1['Restaurant ID'].value_counts().nlargest(st_slider).index
selected_restaurants = df1['Restaurant Name'].value_counts().nlargest(st_slider).index

# Filtramos o DataFrame original com base nos restaurantes selecionados
df_filtered = df1[df1['Restaurant ID'].isin(selected_restaurants)]

st.sidebar.markdown("""---""")


# ==============================================================================
#                          layout no Streamlit
# ==============================================================================
    
tab1 = st.markdown( '#### Melhores restaurantes dos Prinicpais tipos Culinários')

with st.container():
                    
    col1, col2, col3, col4, col5 = st.columns( 5 )
    
    
    with col1:       
        rest_most_avg_rating_ita = df1[df1['Cuisines'] == 'Italian'].groupby(['Restaurant Name','Cuisines'])['Aggregate rating'].mean().reset_index()
        rest_most_avg_rating_ita = rest_most_avg_rating_ita.sort_values(by='Aggregate rating', ascending=False).head()
    
        if not rest_most_avg_rating_ita.empty:
            col1.metric(label=rest_most_avg_rating_ita.iloc[0]['Cuisines'], value=rest_most_avg_rating_ita.iloc[0]['Aggregate rating'])
        else:
            col1.metric(label="Italian", value=0)

    with col2:
        
        rest_high_avg_rating_usa = df1[df1['Cuisines'] == 'American'].groupby(['Restaurant Name','Cuisines'])['Aggregate rating'].mean().reset_index()
        rest_high_avg_rating_usa = rest_high_avg_rating_usa.sort_values(by='Aggregate rating', ascending=False).head()

        if not rest_high_avg_rating_usa.empty:            
            col2.metric(label=rest_high_avg_rating_usa.iloc[0]['Cuisines'], value=rest_high_avg_rating_usa.iloc[0]['Aggregate rating'])
        else:            
            col2.metric(label="American", value=0)

    with col3:
        rest_high_avg_rating_arab = df1[df1['Cuisines'] == 'Arabian'].groupby(['Restaurant Name','Cuisines'])['Aggregate rating'].mean().reset_index()
        rest_high_avg_rating_arab = rest_high_avg_rating_arab.sort_values(by='Aggregate rating', ascending=False).head()

        if not rest_high_avg_rating_arab.empty:
            col3.metric(label=rest_high_avg_rating_arab.iloc[0]['Cuisines'], value=rest_high_avg_rating_arab.iloc[0]['Aggregate rating'])
        else:
            col3.metric(label="Arabian", value=0)

    with col4:
        rest_high_avg_rating_jap = df1[df1['Cuisines'] == 'Japanese'].groupby(['Restaurant Name','Cuisines'])['Aggregate rating'].mean().reset_index()
        rest_high_avg_rating_jap = rest_high_avg_rating_jap.sort_values(by='Aggregate rating', ascending=False).head()

        if not rest_high_avg_rating_jap.empty:
            col4.metric(label=rest_high_avg_rating_jap.iloc[0]['Cuisines'], value=rest_high_avg_rating_jap.iloc[0]['Aggregate rating'])
        else:
            col4.metric(label="Japanese", value=0)

    with col5:
        rest_high_avg_rating_brazilian = df1[df1['Cuisines'] == 'Brazilian'].groupby(['Restaurant Name','Cuisines'])['Aggregate rating'].mean().reset_index()
        rest_high_avg_rating_brazilian = rest_high_avg_rating_brazilian.sort_values(by='Aggregate rating', ascending=False).head()

        if not rest_high_avg_rating_brazilian.empty:
            col5.metric(label=rest_high_avg_rating_brazilian.iloc[0]['Cuisines'], value=rest_high_avg_rating_brazilian.iloc[0]['Aggregate rating'])
        else:
            col5.metric(label="Brazilian", value=0)

with st.container():
    st.markdown( '#### Top 10 Restaurantes por Tipos de Culinárias' )
    top20_rest = df1.loc[:,['Restaurant ID','Restaurant Name','Country Name', 'City','Cuisines', 'Average Cost for two', 'Aggregate rating', 'Votes' ]].sort_values(by=['Aggregate rating'], ascending=[False]).head(st_slider)
    
    st.dataframe(top20_rest )
    
with st.container():
    col1, col2 = st.columns (2, gap='large' )
    
    with col1:
        st.markdown( '#### Top 10 Melhores Tipos de Culinárias' )
        # Encontrando a média de avaliação por tipo de culinária
        cuisine_avg_ratings = df1.groupby('Cuisines')['Aggregate rating'].mean().reset_index()
        # Ordenando pela média de avaliação
        cuisine_avg_ratings = cuisine_avg_ratings.sort_values('Aggregate rating', ascending=False)
        cuisine_avg_ratings = cuisine_avg_ratings.head(st_slider)
        
        fig = px.bar(cuisine_avg_ratings, x='Cuisines', y='Aggregate rating', text_auto='.2s', color='Cuisines', labels={'Cuisines':'Tipos de Culinaria', 'Aggregate rating':'Média da Avaliação Média'})
        
        st.plotly_chart( fig, use_container_width=True )
        
    with col2:
        st.markdown( '#### Top 10 Piores Tipos de Culinárias' )
        # Encontrando a média de avaliação por tipo de culinária
        cuisine_avg_ratings_low = df1.groupby('Cuisines')['Aggregate rating'].mean().reset_index()
        # Ordenando pela média de avaliação
        cuisine_avg_ratings_low = cuisine_avg_ratings_low.sort_values('Aggregate rating', ascending=True)
        cuisine_avg_ratings_low = cuisine_avg_ratings_low.head(st_slider)

        fig = px.bar(cuisine_avg_ratings_low, x='Cuisines', y='Aggregate rating', text_auto='.2s', color='Cuisines', labels={'Cuisines':'Tipos de Culinaria', 'Aggregate rating':'Média da Avaliação Média'})
        
        st.plotly_chart( fig, use_container_width=True )
        
        
        
        
        
        
        
        
        
        
        
        
