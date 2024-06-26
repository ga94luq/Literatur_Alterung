import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

# Laden der Daten
Pfad = 'https://raw.githubusercontent.com/ga94luq/Literatur_Alterung/main/Auswertungsdaten.csv'
df = pd.read_csv(Pfad, delimiter=';')

# Datenbereinigung
df['(rel. Kal. Alterung %)/Tag'] = df['(rel. Kal. Alterung %)/Tag'].str.replace(',', '.').astype(float)
df['Volt/SOC'] = df['Volt/SOC'].str.replace(',', '.').astype(float)
df['Temperatur in '] = df['Temperatur in '].astype(str)

# Initialisierung der Dash App
app = Dash(__name__)
server = app.server

# Layout der Dash App
app.layout = html.Div([
    html.H1('Auswertung der Literatur'),

    # Checkboxen für Zellen Auswahl
    html.Label('Zelle:'),
    dcc.Checklist(
        id='cell-checklist',
        options=[{'label': cell, 'value': cell} for cell in df['Zelle'].unique()],
        value=df['Zelle'].unique().tolist(),
        inline=False
    ),

    # Checkboxen für Paper Auswahl
    html.Label('Paper:'),
    dcc.Checklist(
        id='paper-checklist',
        options=[{'label': paper, 'value': paper} for paper in df['Paper'].unique()],
        value=df['Paper'].unique().tolist(),
        inline=False
    ),

    # Checkboxen für Chemie Auswahl
    html.Label('Chemie:'),
    dcc.Checklist(
        id='chemie-checklist',
        options=[{'label': chemie, 'value': chemie} for chemie in df['Chemie'].unique()],
        value=df['Chemie'].unique().tolist(),
        inline=False
    ),

    # Div zur Darstellung der beiden Plots
    html.Div([
        dcc.Graph(id='scatter-plot-without-facet'),

        # Schieberegler zur Einstellung der y-Achsen-Grenzen
        html.Label('Y-Achsen Bereich (×10^6):'),
        dcc.RangeSlider(
            id='y-axis-slider',
            min=(-0.02 * 10 ** 6),
            max=(0.04 * 10 ** 6),
            step=1,
            value=[-0.02 * 10 ** 6, 0.04 * 10 ** 6],
            marks={i: str(i / 10 ** 6) for i in
                   range(int(-0.02 * 10 ** 6), int(0.04 * 10 ** 6) + 1, int(0.01 * 10 ** 6))}
        ),

        dcc.Graph(id='scatter-plot-with-facet')
    ], style={'display': 'flex', 'flex-direction': 'column'})
])


# Callback zur Aktualisierung der beiden Scatter Plots
@app.callback(
    Output('scatter-plot-without-facet', 'figure'),
    Output('scatter-plot-with-facet', 'figure'),
    [Input('cell-checklist', 'value'),
     Input('paper-checklist', 'value'),
     Input('chemie-checklist', 'value'),
     Input('y-axis-slider', 'value')]
)
def update_scatter_plots(selected_cells, selected_papers, selected_chemies, y_axis_range):
    filtered_df = df[
        df['Zelle'].isin(selected_cells) & df['Paper'].isin(selected_papers) & df['Chemie'].isin(selected_chemies)]

    # Scatter Plot ohne facet_row
    fig_without_facet = px.scatter(
        filtered_df,
        x='Volt/SOC',
        y='(rel. Kal. Alterung %)/Tag',
        color='Zelle',
        symbol='Paper',
        labels={'(rel. Kal. Alterung %)/Tag': '(rel. Kal. Alterung %)/Tag'},
        hover_data={'Chemie': True, 'Volt/SOC': True, 'Zelle': True}
    )
    fig_without_facet.update_traces(marker=dict(size=15))
    fig_without_facet.update_layout(
        title='Auswertung der Literaturergebnisse',
        xaxis_title='Volt/SOC',
        yaxis_title='rel. Kal. Alterung %/Tag',
        legend_title_text='Chemie',
        font=dict(
            family='Arial',
            size=12,
            color='black'
        ),
        height=1400,  # Set the height of the plot
        width=3000  # Set the width of the plot
    )

    # Scatter Plot mit facet_row
    fig_with_facet = px.scatter(
        filtered_df,
        x='Volt/SOC',
        y='(rel. Kal. Alterung %)/Tag',
        color='Temperatur in ',
        symbol='Paper',
        labels={'(rel. Kal. Alterung %)/Tag': '(rel. Kal. Alterung %)/Tag'},
        hover_data={'Chemie': True},
        facet_row="Zelle"
    )
    fig_with_facet.update_traces(marker=dict(size=15))
    fig_with_facet.update_layout(
        title='rel. Kal. Alterung in % / Tag | Untergliedert je Zelle',
        xaxis_title='Volt/SOC',
        yaxis_title='rel. Kal. Alterung %/Tag',
        legend_title_text='Chemie',
        font=dict(
            family='Arial',
            size=12,
            color='black'
        ),
        height=2000,  # Set the height of the plot
        width=3000,
        yaxis=dict(range=[y / 10 ** 6 for y in y_axis_range])  # Set the y-axis range based on the slider input
    )

    return fig_without_facet, fig_with_facet


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
