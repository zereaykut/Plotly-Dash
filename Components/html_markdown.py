from dash import Dash, dcc, html

app = Dash(__name__)

app.layout = html.Div(
    style={
        "font-family": "Arial",
        "backgroundColor": "black",
        "color": "lightGrey",
        "horizontal-align": "center",
    },
    children=[
        html.H1("Hello!!!"),
        html.P(
            [
                "Welcome to the ",
                html.Span(
                    "BEST",
                    style={"color": "Red", "font-weight": "Bold", "fontSize": 32},
                ),
                " website in the world!",
            ]
        ),
        html.Br(),
        html.Div(
            [
                dcc.Markdown(
                    """
            # Section 1
            ### Shopping List
            * Apples
            * Salad Tongs
            * Jumbo Couch

            **Note to self**: Don"t forget to bring shopping bag!
        """
                ),
                html.Br(),
                dcc.Markdown(
                    """
            # Section 2
            ### Learning List
            1. Python
            2. More Python
            3. A bit of HTML

            **Note to self**: *Be kind to yourself if you get stuck.*
            """,
                    style={"color": "limegreen"},
                ),
            ]
        ),
    ],
)


app.run_server(debug=True, mode="inline", port=8649)

