from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import light_switch as light
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
    led_state = n_clicks % 2
    light.switch_state(led_state)

    if led_state:
        return "background-color-green"
    else:
        return "background-color-red"
if __name__ == '__main__':
    app.run(debug=True)