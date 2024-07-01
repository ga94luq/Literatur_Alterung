import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/ga94luq/Literatur_Alterung/main/Daten_CSV.csv', delimiter=';')
df = pd.DataFrame(df)

data = df
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__)
server = app.server
Breite_Boxen = '300px'
# Layout der Dash App
app.layout = html.Div([
    html.H1('Auswertung der Literatur', style={'text-align': 'center', 'color': 'white'}),

    html.Label('Zelle:', style={'color': 'white'}),
    dcc.Checklist(
        id='cell-checklist',
        options=[{'label': cell, 'value': cell} for cell in df['Zelle'].unique()],
        value=df['Zelle'].unique().tolist(),
        inline=True,  # Horizontal layout
        style={'display': 'flex', 'flex-wrap': 'wrap', 'color': 'white'}
    ),

    # Checkboxen für Paper Auswahl
    html.Label('Paper:', style={'color': 'white'}),
    dcc.Checklist(
        id='paper-checklist',
        options=[{'label': paper, 'value': paper} for paper in df['Paper'].unique()],
        value=df['Paper'].unique().tolist(),
        inline=True,  # Horizontal layout
        style={'display': 'flex', 'flex-wrap': 'wrap', 'color': 'white'}
    ),

    # Checkboxen für Chemie Auswahl
    html.Label('Chemie:', style={'color': 'white'}),
    dcc.Checklist(
        id='chemie-checklist',
        options=[{'label': chemie, 'value': chemie} for chemie in df['Chemie'].unique()],
        value=df['Chemie'].unique().tolist(),
        inline=True,  # Horizontal layout
        style={'display': 'flex', 'flex-wrap': 'wrap', 'color': 'white'}
    ),

    html.Div([
        html.Label('X-Achse auswählen:', style={'color': 'white'}),
        dcc.Dropdown(
            id='X_Achse_dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='Volt/SOC',
            clearable=True,
            multi=False,
            style={'color': 'black', 'width': Breite_Boxen}
        ),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label('Y-Achse auswählen:', style={'color': 'white'}),
        dcc.Dropdown(
            id='Y_Achse_dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='Rel. Kapa. % / Tag',
            clearable=True,
            multi=False,
            style={'color': 'black', 'width': Breite_Boxen}
        ),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label('Rowauswahl: Hier Festlegen nach welchem Kriterium Spalten gebildet werden sollen. Nur 1 auswählen.',
                   style={'color': 'white'}),
        dcc.Checklist(
            id='RowAuswahl-checklist',
            options=[{'label': col, 'value': col} for col in df.columns],
            value=[],
            inline=True,  # Horizontal layout
            style={'display': 'flex', 'flex-wrap': 'wrap', 'color': 'white'}
        ),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label('Farbauswahl: Hier Festlegen nach welchem Kriterium Farben zugeordnet werden sollen.',
                   style={'color': 'white'}),
        dcc.Dropdown(
            id='Farbauswahl-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='Zelle',
            clearable=True,
            multi=False,
            style={'color': 'black', 'width': Breite_Boxen}
        ),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label('Styleauswahl: Hier Festlegen nach welchem Kriterium die Marker zugeordnet werden sollen.',
                   style={'color': 'white'}),
        dcc.Dropdown(
            id='Styleauswahl-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value='Paper',
            clearable=True,
            multi=False,
            style={'color': 'black', 'width': Breite_Boxen}
        ),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label(
            'Informationsauswahl: Hier Festlegen welche Informationen bei Anklicken der Datenpunkte angezeigt werden sollen.',
            style={'color': 'white'}),
        dcc.Checklist(
            id='Informationsauswahl-checklist',
            options=[{'label': col, 'value': col} for col in df.columns],
            value=df.columns.tolist(),
            inline=True,  # Horizontal layout
            style={'display': 'flex', 'flex-wrap': 'wrap', 'color': 'white'}
        ),
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label('Geschätze Alterung nach Tagen x. Gebe voraussichtliche Dauer der kal. Alterung an:',
                   style={'color': 'white'}),
        dcc.Slider(
            id='Alterungsdauer-input',
            min=1,
            max=200,
            step=1,  # Anpassung je nach Bedarf
            value=1,
            tooltip={"placement": "bottom", "always_visible": False},
            marks={i: f'{i}' for i in [0, 30, 60, 90, 120, 150, 180]}
        ),
    ], style={'margin-bottom': '20px', 'width': '1000px'}),

    html.Div([
        html.Label('Hier festlegen welche Alterungsperiode berücksichtigt werden sollen.', style={'color': 'white'}),
        dcc.RangeSlider(
            id='DauerMin_Range',
            min=df['Dauer d. Alterung in Tagen'].min(),
            max=df['Dauer d. Alterung in Tagen'].max(),
            step=1,  # Anpassung je nach Bedarf
            value=[df['Dauer d. Alterung in Tagen'].min(), df['Dauer d. Alterung in Tagen'].max()],
            tooltip={"placement": "bottom", "always_visible": False},
            marks=None
        ),
    ], style={'margin-bottom': '20px', 'width': '1000px'}),

    # Div zur Darstellung des Plots
    html.Div([
        dcc.Graph(id='scatter-plot-without-facet'),
    ])
], style={'backgroundColor': 'grey', 'padding': '20px'})  # Dark background with padding


# Callback zur Aktualisierung des Scatter Plots
@app.callback(
Output('scatter-plot-without-facet', 'figure'),
[Input('cell-checklist', 'value'),
 Input('paper-checklist', 'value'),
 Input('chemie-checklist', 'value'),
 Input('RowAuswahl-checklist', 'value'),
 Input('Farbauswahl-dropdown', 'value'),
 Input('Styleauswahl-dropdown', 'value'),
 Input('Informationsauswahl-checklist', 'value'),
 Input('Alterungsdauer-input', 'value'),
 Input('DauerMin_Range', 'value'),
 Input('Y_Achse_dropdown', 'value'),
 Input('X_Achse_dropdown', 'value')]
)

def update_scatter_plot(selected_cells, selected_papers, selected_chemies, RowAuswahl, Farbauswahl, Styleauswahl,
                        Informationsauswahl, Dauer_in_Tagen, DauerMin, Y_Achse, X_Achse):
    filtered_df = df[
        df['Zelle'].isin(selected_cells) &
        df['Paper'].isin(selected_papers) &
        df['Chemie'].isin(selected_chemies) &
        df['Dauer d. Alterung in Tagen'].between(DauerMin[0], DauerMin[1])
        ]

    filtered_df['Rel. Kapa. % / Tag'] = data['Rel. Kapa. % / Tag'] * Dauer_in_Tagen

    if len(RowAuswahl) == 0:
        fig = px.scatter(
            filtered_df,
            x=X_Achse,
            y=Y_Achse,
            color=Farbauswahl,
            symbol=Styleauswahl,
            labels={'(rel. Kal. Alterung %)/Tag': '(rel. Kal. Alterung %)/Tag'},
            hover_data=Informationsauswahl,
        )
    elif len(RowAuswahl) == 1:
        fig = px.scatter(
            filtered_df,
            x=X_Achse,
            y=Y_Achse,
            color=Farbauswahl,
            symbol=Styleauswahl,
            labels={'(rel. Kal. Alterung %)/Tag': '(rel. Kal. Alterung %)/Tag'},
            hover_data=Informationsauswahl,
            facet_row=RowAuswahl[0]
        )
    else:
        print('Fehler - Nur eine Auswahl erlaubt!.')
        fig = px.scatter()  # Empty figure

    fig.update_traces(marker=dict(size=15))
    if Dauer_in_Tagen < 2:
        fig.update_layout(
            title='Auswertung der Literaturergebnisse',
            xaxis_title=f'{X_Achse}',
            yaxis_title=f'{Y_Achse}',
            legend_title_text='Legende',
            font=dict(
                family='Arial',
                size=14,
                color='white'  # White font color
            ),
            height=1250,  # Set the height of the plot
            width=1500,  # Set the width of the plot
            plot_bgcolor='grey',  # Dark background
            paper_bgcolor='grey',  # Dark background
            font_color='white',  # White font color
            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=-.5,
                #xanchor="center",
                x=0.5
            )
        )
    else:
        y_Achsenbeschriftung = f'voraussichtlicher {Y_Achse} nach {Dauer_in_Tagen} Tagen'
        fig.update_layout(
            title='Auswertung der Literaturergebnisse',
            xaxis_title=f'{X_Achse}',
            yaxis_title=y_Achsenbeschriftung,
            legend_title_text='Legende:',
            font=dict(
                family='Arial',
                size=14,
                color='white'  # White font color
            ),
            height=1250,  # Set the height of the plot
            width=1500,  # Set the width of the plot
            plot_bgcolor='grey',  # Dark background
            paper_bgcolor='grey',  # Dark background
            font_color='white',  # White font color
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.5,
                xanchor="center",
                x=0.5
            )
        )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
