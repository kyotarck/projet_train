import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies
import matplotlib.pyplot as plt


# Chargement des données
df1 = pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')
df2 = pd.read_csv('emplacement-des-gares-idf.csv', sep=';')
df2[['lat', 'lng']] = df2['Geo_Point'].str.split(',', expand=True)
df2['lat'] = df2['lat'].str.strip().astype(float)
df2['lng'] = df2['lng'].str.strip().astype(float)


#Aggrégation des données 1
sort_ratp = df1.sort_values(by=['Trafic'], ascending=False).head(10)

# Création bar chart TOP 10 trafic en fonction des stations
#fig1 = px.bar(sort_ratp, x='Station', y='Trafic',width=1200, height=600)
#fig1 = px.bar(sort_ratp, x='Station', y='Trafic', color_discrete_sequence=['pink']*len(sort_ratp))

#Tri des données
sort_ratp = sort_ratp.sort_values(by='Trafic', ascending=False)

#Création du graphique à barres
plt.bar(sort_ratp['Station'], sort_ratp['Trafic'], color='#ffb6c1')

#Ajout du titre et des labels d'axes
plt.title('Trafic des stations RATP')
plt.xlabel('Stations')
plt.ylabel('Trafic')


plt.rc('font', family='Helvetica', size=16)
plt.show()


#Aggrégation des données 2
grouped_data2 = df1.groupby('Ville')['Trafic'].sum().reset_index()
top5 = grouped_data2.sort_values('Trafic', ascending=False).head(5)

#Création bar chart  TOP 5 trafic par ville
#Tri des données et sélectionner les 5 premières villes
top5 = top5.sort_values(by='Trafic', ascending=False).head(5)

#Création du graphique en camembert
plt.figure(figsize=(10, 6))
plt.pie(top5['Trafic'], labels=top5['Ville'], autopct='%1.1f%%', 
        textprops={'fontsize': 20}, colors=['#5eb0e5', '#f3f3f3', '#2e3033', '#f3d060', '#ee7762'])


plt.title('Répartition du trafic RATP par ville')
plt.show()

#Aggrégation des données 3
grouped_data3 = df2.groupby('exploitant')['nom_long'].count().reset_index()
grouped_data3= grouped_data3.rename(columns={'nom_long': 'nombres_stations'})

#Création bar chart Nombre de stations par exploitant
grouped_data3 = grouped_data3.sort_values(by='nombres_stations', ascending=False)

#Création du graphique à barres
plt.figure(figsize=(10, 6))
plt.bar(grouped_data3['exploitant'], grouped_data3['nombres_stations'], 
        color='#5eb0e5')

#Ajout du titre et des labels d'axes
plt.title('Nombre de stations par exploitant')
plt.xlabel('Exploitant')
plt.ylabel('Nombre de stations')
plt.rcParams.update({'font.family': 'Helvetica', 'font.size': 16})
plt.show()


# Aggrégation des données 4
grouped_data4 = df2.groupby('ligne')['nom_long'].count().reset_index()
grouped_data4 = grouped_data4.rename(columns={'nom_long': 'nombres_stations'})

grouped_data4 = grouped_data4.sort_values(by='nombres_stations', ascending=False)

#Création du graphique à barre
plt.figure(figsize=(10, 6))
plt.bar(grouped_data4['ligne'], grouped_data4['nombres_stations'], 
        color='#5eb0e5')

#Ajout du titre et des labels d'axes
plt.title('Nombre de stations par ligne')
plt.xlabel('Ligne')
plt.ylabel('Nombre de stations')
plt.rcParams.update({'font.family': 'Helvetica', 'font.size': 16})
plt.show()


#Ajout de la carte avec les positions des stations
fig5 = px.scatter_mapbox(df2, lat="lat", lon="lng", hover_name="nom_long", hover_data=["Geo_Point", "exploitant"],
                          color_discrete_sequence=["#1f77b4"], zoom=9, height=600)
fig5.update_layout(mapbox_style="open-street-map")
fig5.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig5.update_layout(
    font=dict(
        family="Helvetica",
        size=16,
    )
)

fig5.show()

#Création d'un filtre qui sélectionne les 10 premières stations de chaque réseau
top10_res = sort_ratp.groupby('Réseau').head(10)

#Création du graphique à barres 
fig6 = px.bar(top10_res, x='Réseau', y='Trafic', color='Réseau', color_discrete_sequence=['#1f77b4'])
fig6.update_layout(
    font=dict(
        family="Helvetica",
        size=16,
    )
)

#Configuration de la couleur des marqueurs
fig6.update_traces(marker_color='#1f77b4')

#Regroupement des données par exploitant et comptage du nombre de stations
grouped_data5 = df2.groupby('exploitant')['nom_long'].count().reset_index()

#Création du graphique à barres avec les données précédentes
fig7 = px.bar(grouped_data5, x='exploitant', y='nom_long', labels={'exploitant': 'Exploitant', 'nom_long': 'Nombre de stations'},
              color_discrete_sequence=['#d62728']*len(grouped_data5))
fig7.update_layout(
    font=dict(
        family="Helvetica",
        size=16,
    )
)
#Création de l'application Dash
app = Dash(__name__)

#Définition de la mise en page
app.layout = html.Div(children=[
    html.H1("Dashboard de visualisation de données RATP", style={'color': 'black','text-align': 'center', 'font-size': '36px', 'font-family': 'Arial', 'font-weight': 'bold','text-decoration': 'underline'}),
    
    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(className='col-md-6', children=[
            html.H2("Top 10 des stations avec le plus grand trafic", style={'color': '#f4cccc','text-align': 'center', 'font-size': '25px', 'font-family': 'Helvetica', 'font-weight': 'bold'}),
            dcc.Graph(id='bar-chart-1', figure=sort_ratp, style={'backgroundColor': 'white', 'height': '600px','width': '800px' ,'color': '#f4cccc'},config={'displayModeBar': False})
        ]),

        html.Div(className='col-md-6', children=[
            html.H2("Top 5 villes avec le plus grand trafic", style={'color': '#f4cccc','text-align': 'center'}),
            dcc.Graph(id='pie-chart-1', figure=top5,style={'backgroundColor': 'white', 'height': '500px', 'width': '800px'},
            config={'displayModeBar': False})
        ])
    ]),

    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(className='col-md-6', children=[
            html.H2("Nombre de stations par exploitant", style={'color': '#d2a6a1','text-align': 'center', 'font-size': '25px', 'font-family': 'Helvetica', 'font-weight': 'bold'}),
            dcc.Graph(id='bar-chart-2', figure=grouped_data3,style={'backgroundColor': 'white', 'height': '400px','width': '800px' ,'color': '#d2a6a1'},config={'displayModeBar': False})
        ]),

        html.Div(className='col-md-6', children=[
            html.H2("Nombre de stations par ligne", style={'color': '#d2a6a1','text-align': 'center', 'font-size': '25px', 'font-family': 'Helvetica', 'font-weight': 'bold'}),
            dcc.Graph(id='bar-chart-5', figure=grouped_data4,style={'backgroundColor': 'white', 'height': '550px','width': '1300px' ,'color': '#d2a6a1'},config={'displayModeBar': False})
        ])
    ]),

    html.Div(children=[
        html.H2("Position des stations sur une carte", style={'color': '#d9ad7c','text-align': 'center', 'font-size': '25px', 'font-family': 'Helvetica', 'font-weight': 'bold'}),
        dcc.Graph(id='map-chart', figure=fig5)
    ]),

    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(className='col-md-6', children=[
            html.H2("Top 10 stations avec le plus grand trafic avec un filtre réseau", style={'color': '#e7b8b4','text-align': 'center', 'font-size': '25px', 'font-family': 'Helvetica', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='reseau-filter',
                options=[{'label': category, 'value': category} for category in sort_ratp['Réseau'].unique()],
                value=None,
                placeholder='Select a category'
            ),
            dcc.Graph(id='bar-chart_3', figure=fig6,style={'backgroundColor': 'white', 'height': '550px','width': '1000px' ,'color': '#e7b8b4'},config={'displayModeBar': False})
        ]),
        html.Div(className='col-md-6', children=[
            html.H2("Nombre de lignes par exploitant avec filtre", style={'color': '#e7b8b4','text-align': 'center', 'font-size': '25px', 'font-family': 'Helvetica', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='exploit-filter',
                options=[{'label': category, 'value': category} for category in df2['exploitant'].unique()],
                value=None,
                placeholder='Select a category'
            ),
            dcc.Graph(id='bar-chart4', figure=fig7,style={'backgroundColor': 'white', 'height': '500px','width': '1000px' ,'color': '#e7b8b4'},config={'displayModeBar': False})
        ])
    ])
])

#Définition du callback

@app.callback(
    dependencies.Output('bar-chart_3', 'figure'),
    dependencies.Input('reseau-filter', 'value')
)
def update_bar_chart1(category):
    if category is None:
        filtered_df = top10_res
    else:
        filtered_df = top10_res[top10_res['Réseau'] == category]

    return px.bar(filtered_df, x='Station', y='Trafic')

@app.callback(
    dependencies.Output('bar-chart4', 'figure'),
    dependencies.Input('exploit-filter', 'value')
)
def update_bar_chart2(category):
    if category is None:
        filtered_df = grouped_data5
    else:
        filtered_df = grouped_data5[grouped_data5['exploitant'] == category]

    return px.bar(filtered_df, x='exploitant', y='nom_long')


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)