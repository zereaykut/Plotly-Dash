import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

ski_resorts = pd.read_csv("Data/European_Ski_Resorts.csv").drop("Unnamed: 0", axis=1)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

app.layout = html.Div(
    [
        html.H2(id="title", style={"text-align": "center"}),
        html.P("Select Options Below:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=ski_resorts["Country"].unique(),
            value="Andorra",
            className="dbc",
        ),
        dcc.Slider(
            id="Elevation Slider",
            min=0,
            max=4000,
            step=500,
            value=500,
            marks={
                i: {"label": f"{i}m", "style": {"fontSize": 16}}
                for i in range(0, 4000, 500)
            },
            className="dbc",
        ),
        html.Div(id="output-div"),
    ]
)


@app.callback(
    Output("title", "children"),
    Output("output-div", "children"),
    Input("country-dropdown", "value"),
    Input("Elevation Slider", "value"),
)
def elevation_table(country, elevation):
    if not country and elevation:
        raise PreventUpdate

    title = f"Ski Resorts in {country} with peaks above {elevation}M"

    df = ski_resorts.query("HighestPoint > @elevation and Country == @country")

    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        filter_action="native",
        sort_action="native",
        export_format="xlsx",
        style_header={
            "backgroundColor": "rgb(30, 30, 30)",
            "color": "lightgrey",
            "font-family": "Arial",
        },
        style_data={
            "backgroundColor": "rgb(50, 50, 50)",
            "color": "grey",
            "font-family": "Arial",
        },
    )

    return title, table


if __name__ == "__main__":
    app.run_server(mode="inline", debug=True, port=8334)
