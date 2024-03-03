from dash import Dash, html, Input, Output, callback
import light_switch as light
dashboard_external_stylesheets = [
    'dashboard.css'
]
app = Dash(__name__, external_stylesheets=dashboard_external_stylesheets)

app.layout = html.Div([
    html.Button(children=[
        html.Img(src="assets/off-button.png", className="image-icon", id="button-image")
    ], 
    id="light-button", 
    n_clicks=0),
    html.Div(
        children=[
            html.Img(src="assets/closed-light.png", className="image-icon", id="light-icon-image")
        ],
        id="light-icon"
    )
])



@callback(
    [
        Output(component_id="button-image", component_property="src"),
        Output(component_id="light-icon-image", component_property="src"),
    ],
    Input(component_id="light-button", component_property="n_clicks")
)    
def change_light_state(n_clicks):
    # Toggles light state from 0 or 1 indicating whether light is open or closed
    # The real LED state from the output of the LED pin determines the light state on the dashboard
    # because we do not want to show a "fake state" to the user
    calculated_led_state = n_clicks % 2
    real_led_state = light.switch_state(calculated_led_state)

    if real_led_state:
        return "assets/on-button.png", "assets/open-light.png"
    else:
        return "assets/off-button.png", "assets/closed-light.png"
if __name__ == '__main__':
    app.run(debug=True)