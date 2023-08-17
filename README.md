# 1. Problema de negócio
Parabéns! Você acaba de ser contratado como Cientista de Dados da empresa
Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra
a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
utilizando dados!
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.
O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às seguintes perguntas:

## Geral:

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## Pais
1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

## Cidades:

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?

## Restaurantes:

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

## Tipos de Culinária:

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

# 2. Premissas assumidas para a análise:

 1. A analise foi realizada com dados fornecidos pela API do aplicativo FomeZero
 2. Marketplace foi o modelo de negócio assumido.
 3. Os 5 principais visões do negócio foram: Visão Geral, Visão Países, Visão Cidades, Visão Restaurantes e Visão Tipos de Culinárias.
 
# 3. Estratégia da solução

## O painel estratégico foi desenvolvido utilizando as métricas que refletem as 5 principais visões do modelo de negócio da empresa:

 1. Visão Geral de restaurantes e paises
 2. Visão Países
 3. Visão Cidades
 4. Visão Resturantes
 5. Tipos de Culinárias 

## Cada visão é representada pelo seguinte conjunto de métricas

1. Visão Geral de restaurantes e paises:
 1. Total de restaurantes cadastrados
 2. Total Paises cadastrados
 3. Total Cidades cadastradas
 4. Total de avaliações feitas na plataforma
 5. Total dos tipos de culinárias oferecidas

2. Visão Países:
 1. Quantidade de Restaurantes Registrados por País
 2. Quantidade de Cidades Resgistrados por País
 3. Média de Avaliações Feitas por Países
 4. Média de Preço de um prato para duas pessoas p/ País

3. Visão Cidades:
 1. Top 10 Cidades com mais Restaurantes na Base de Dados
 2. Top 7 Cidades c/ Restaurantes c/ média de avaliação acima de 4
 3. Top 7 Cidades c/ Restaurantes c/ média de avaliação abaixo de 2.5
 4. Top 10 Cidades mais restaurantes com tipos culinarios distintos

4. Visão Tipos de Culinárias e Restaurantes:
 1. Melhores restaurantes dos Prinicpais tipos Culinários
 2. Top 10 Restaurantes por Tipos de Culinárias
 3. Top 10 Melhores Tipos de Culinárias
 4. Top 10 Piores Tipos de Culinárias

# 4. Top 3 Insights de dados
 1. India é o pais principal do aplicativo onde possui a maior quantidade de restaurantes registrados por país
 2. Birmingham possui a maior variedade de tipos de comida de todos os paises
 3. Os melhores restaurantes com maiores notas por tipos de culinaria ficam em USA	

# 5. O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em
qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://fomezeroproject.streamlit.app

# 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas
que exibam essas métricas da melhor forma possível para o CEO, 
para que seja possivel obter de forma segmentada informações pertinentes referente ao Marketplace de restaurantes Fome Zero de forma que os dados apresentados possam servir de apoio para que seja possivel tomar as melhores decisões estratégicas.

Referente aos tipos de culinárias podemos ver que a maior parte das melhores notas e tipos de culinárias encontra-se em cidades dos EUA

# 7. Próximo passos
 1. Reduzir o número de métricas.
 2. Criar novos filtros.
 3. Adicionar novas visões de negócio.
