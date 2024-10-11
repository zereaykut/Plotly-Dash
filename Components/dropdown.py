import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

# Docs:     [dcc.Dropdown](https://dash.plotly.com/dash-core-components/dropdown)

app = dash.Dash(__name__)

df = pd.read_csv("Data/Urban_Park_Ranger_Animal_Condition.csv")

app.layout = html.Div(
    [
        html.Div([dcc.Graph(id="our_graph")], className="nine columns"),
        html.Div(
            [
                html.Br(),
                html.Div(id="output_data"),
                html.Br(),
                html.Label(
                    ["Choose column:"],
                    style={"font-weight": "bold", "text-align": "center"},
                ),
                dcc.Dropdown(
                    id="my_dropdown",
                    options=[
                        {"label": "Species", "value": "Animal Class"},
                        {
                            "label": "Final Ranger Action",
                            "value": "Final Ranger Action",
                        },
                        {"label": "Age", "value": "Age", "disabled": True},
                        {"label": "Animal Condition", "value": "Animal Condition"},
                        {"label": "Borough", "value": "Borough"},
                        {"label": "Species Status", "value": "Species Status"},
                    ],
                    optionHeight=35,  # height/space between dropdown options
                    value="Borough",  # dropdown value selected automatically when page loads
                    disabled=False,  # disable dropdown value selection
                    multi=False,  # allow multiple dropdown values to be selected
                    searchable=True,  # allow user-searching of dropdown values
                    search_value="",  # remembers the value searched in dropdown
                    placeholder="Please select...",  # gray, default text shown when no option is selected
                    clearable=True,  # allow user to removes the selected value
                    style={
                        "width": "100%"
                    },  # use dictionary to define CSS styles of your dropdown
                    # className="select_box",           #activate separate CSS document in assets folder
                    # persistence=True,                 #remembers dropdown value. Used with persistence_type
                    # persistence_type="memory"         #remembers dropdown value selected until...
                ),  # "memory": browser tab is refreshed
                # "session": browser tab is closed
                # "local": browser cookies are deleted
            ],
            className="three columns",
        ),
    ]
)


@app.callback(
    Output(component_id="our_graph", component_property="figure"),
    [Input(component_id="my_dropdown", component_property="value")],
)
def build_graph(column_chosen):
    dff = df
    fig = px.pie(dff, names=column_chosen)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(
        title={
            "text": "NYC Calls for Animal Rescue",
            "font": {"size": 28},
            "x": 0.5,
            "xanchor": "center",
        }
    )
    return fig


# ---------------------------------------------------------------
# For tutorial purposes to show the user the search_value


@app.callback(
    Output(component_id="output_data", component_property="children"),
    [Input(component_id="my_dropdown", component_property="search_value")],
)
def build_graph(data_chosen):
    return f"""Search value was: ' {data_chosen} '"""


# ---------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)
