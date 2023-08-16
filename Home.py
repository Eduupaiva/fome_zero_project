import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="📈"
   
)

#image_path = r'\Users\dudup\Documents\Comunidade Ds\Repos\\'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=300 )

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")

st.write( "# Fome Zero Dashboard" )

st.markdown(
    """                       
    Este projeto apresenta uma análise exploratória detalhada dos dados de restaurantes disponíveis na plataforma Zomato. 
    Utilizando bibliotecas como Pandas, Plotly, Folium e Streamlit, foi investigado diversos aspectos, desde tipos de culinária mais populares até a distribuição geográfica dos restaurantes.
    A análise abrange avaliações, localização, preços médios e muitas outras informações interessantes sobre os restaurantes. O código Python bem organizado e as visualizações interativas permitem uma compreensão completa dos insights obtidos. Dê uma olhada nos resultados e surpreenda-se com a riqueza de informações ocultas nos dados dos restaurantes.
    Esse Dashboard foi construído para que seja possivel obter de forma segmentada informações pertinentes referente ao Marketplace de restaurantes Fome Zero de forma que os dados apresentados possam servir de apoio para que seja possivel  tomar as melhores decisões estratégicas
            
            ### Como utilizar esse Dashboard?
                — Geral:
                    — Visão Geral: Países cadastrados e informações gerais sobre o conjunto de dados.                    
                — Visão Países:
                    — Acompanhamento dos indicadores segmentado por países
                — Visão Cidades:
                    — Rankeamento de Cidades baseadas nos restaurantes 
                 — Visão Tipos de Culinária:
                     —  Rankeamento e informações referente aos melhores restaurantes por tipo de culinária com filtros para melhor segmentação.  
                """ )