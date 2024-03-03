from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import light_switch
dashboard_external_stylesheets = [
    'dashboard.css'
]
app = Dash(__name__, external_stylesheets=dashboard_external_stylesheets)

app.layout = html.Div([
    html.Button("Light Button", id="light-button", n_clicks=0),
    html.Div(
        id="light-icon",
        className="background-color-red"
    )
])
@callback(
    Output(component_id="light-icon", component_property="className"),
    Input(component_id="light-button", component_property="n_clicks")
)
def change_light_state(n_clicks):
    # Sets the light status state to 0 or 1 indicating whether light is open or closed
    light_state = n_clicks % 2

    if light_state == 0:
        return "background-color-red"
    else:
        return "background-color-green"
if __name__ == '__main__':
    app.run(debug=True)