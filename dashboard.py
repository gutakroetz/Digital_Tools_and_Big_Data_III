import plotly.graph_objects as go # or plotly.express as px
figure = go.Figure()
fig1 = go.Figure()# or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


import pandas as pd

df = pd.read_csv('data/alldata_wgs846.csv')#.query("bld_age == '2015'")
app = Dash(__name__)

figure = px.scatter_mapbox(df, lat="y1", lon="x1", hover_name="ogc_fid", hover_data=["ogc_fid"],
                             zoom=15, height=500,opacity=0.5, color=df["bld_age"], color_continuous_scale=px.colors.sequential.matter,
                           title="MAP"
                           )
figure.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
figure.update_layout(mapbox_style="carto-positron")
figure.update_layout(margin={"r":60,"t":10,"l":60,"b":10})

app.layout = html.Div([
    html.Div(
        className="a",
        children=[
            html.Div(
                className="two columns",
                children=[
                    html.Div(
                        children=dcc.Graph(
                            figure=figure,
                            id='map',
                            hoverData={'points': [{'customdata': 2}]},
                        )
                    )
                ]
            )
        ]
     ),
    html.Div(
        className="b",
        children=[
            html.Div(
                className="aaa columns",
                children=[
                    html.Div(
                        children=dcc.Graph(id='histogram')
                    )

                ]

            )
        ]
    )
])

# app.layout = html.Div([
#     dcc.Graph(
#         figure=figure,
#         id='map',
#         hoverData={'points': [{'customdata': 2}]},
#         ),
#     dcc.Graph(id='histogram')
#     ])




@app.callback(
    Output('histogram', 'figure'),
    Input('map', 'hoverData'))
def histogram(hoverData):
    id = hoverData['points'][0]['hovertext']
    print(id)
    print(hoverData)
    dff = df[df["ogc_fid"] == id]
    print(dff)
    # Use `hole` to create a donut-like pie chart
    histogram = px.pie(dff, values='ogc_fid', names=['bcn_mate_1','bcn_mate_2'], color_discrete_sequence=px.colors.sequential.RdBu)
    #histogram = px.histogram(dff, x='ogc_fid',
                        #y=["bcn_mate_1","bcn_mate_2","bcn_mate_3","bcn_mate_4","bcn_mate_5","bcn_mate_6"],
                        #labels={'ogc_fid':'building'},)

    return histogram


if __name__ == '__main__':
    app.run_server(debug=True)
