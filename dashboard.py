
from dash import Dash, html, Input, Output, callback, dcc
import light_switch as light
import dash_daq as daq
import DHT11 as dht11





dashboard_external_stylesheets = [
    'dashboard.css'
]
app = Dash(__name__, external_stylesheets=dashboard_external_stylesheets)


temperature_read_interval = dcc.Interval(
    id="temperature-read-interval",
    interval=2000,
    n_intervals=0
)

temperature_gauge = daq.Gauge(
    id="temperature-gauge",
    min=0,
    max=50,
    label="Temperature",
    color={"gradient": True,
           "ranges": {
               "blue": [0, 15],
               "green": [15, 25],
               "yellow": [25, 35],
               "red": [35, 50]
           }
           },
    showCurrentValue=True,
    units="°C"
)

humidity_read_interval = dcc.Interval(
    id="humidity-read-interval",
    interval=2000,
    n_intervals=0
)

humidity_gauge = daq.Gauge(
    id="humidity-gauge",
    min=20,
    max=80,
    scale={
        "custom": {
            20: {"label": "20"},
            30: {"label": "30"},
            40: {"label": "40"},
            50: {"label": "50"},
            60: {"label": "60"},
            70: {"label": "70"},
            80: {"label": "80"},
        }
    },
    label="Humidity",
    color="#3c6bfa",
    showCurrentValue=True,
    units="%",
)

app.layout = html.Div([
    html.Div(
        className="displayInlineBlock verticalAlignTop",
        children=[
            html.Div(
                children=[
                    html.Button(children=[
                        html.Img(src="assets/off-button.png", className="image-icon", id="button-image")
                    ],
                        id="light-button",
                        n_clicks=0),
                ]
            ),
            html.Div(
                children=[
                    html.Img(src="assets/closed-light.png", className="image-icon", id="light-icon-image")
                ],
                id="light-icon"
            ),
        ]
    ),
    html.Div(
        className="displayInlineBlock",
        children=[
            temperature_gauge,
            humidity_gauge,
            temperature_read_interval,
            humidity_read_interval
        ]
    ),
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


@callback(
    Output(component_id="temperature-gauge", component_property="value"),
    Input(component_id="temperature-read-interval", component_property="n_intervals")
)
def get_temperature(_):
    sensor = dht11.DHT11(pin=11)#the pin11 is in the physicl this means that in the GPIO is the 17
    temperature = sensor.read_temperature()
    return temperature


@callback(
    Output(component_id="humidity-gauge", component_property="value"),
    Input(component_id="humidity-read-interval", component_property="n_intervals")
)
def get_humidity(_):
     sensor = dht11.DHT11(pin=11) #the pin11 is in the physicl this means that in the GPIO is the 17
     humidity = sensor.read_humidity()  # Call the method to get humidity
     return humidity


if __name__ == '__main__':
    app.run(debug=True)
