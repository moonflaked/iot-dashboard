
from dash import Dash, html, Input, Output, callback, dcc
import RPi.GPIO as GPIO
import light_switch as light
import dash_daq as daq
import Freenove_DHT as DHT
import email_send_receive as email_module
import Motor as motor

motor.turn_off()
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
    interval=15000,
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
        className="displayInlineBlock verticalAlignTop",
        children=[
            temperature_gauge,
            humidity_gauge,
            temperature_read_interval,
            humidity_read_interval
        ]
    ),
    html.Div(
        className="displayInlineBlock",
        children=[
            html.Div(
                children=[
                    html.Img(
                        src="assets/fan.png",
                        id="fan-icon-image"
                    )
                ]
            )
        ]
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

@callback(
    Output(component_id="temperature-gauge", component_property="value"),
    Input(component_id="temperature-read-interval", component_property="n_intervals")
)
def get_temperature(_):
    sensor = DHT.DHT(pin=12)#the pin12 is in the physicl this means that in the GPIO is the 18
    chk = sensor.readDHT11()
    if(chk is sensor.DHTLIB_OK):
        return sensor.temperature

@callback(
    Output(component_id="fan-icon-image", component_property="src"),
    Input(component_id="temperature-gauge", component_property="value")
)
def check_temperature(sensor_temperature):
    if(email_module.response_received == True and email_module.yes_response_received == False):
        motor.turn_off()
        email_module.response_received = False
        return "assets/fan.png"
    elif(email_module.response_received == True and email_module.yes_response_received == True):
        motor.turn_on()
        return "assets/fan-spin.png"
    elif(sensor_temperature > 24):  
        sender_email = 'loganluo288@gmail.com'
        sender_password = 'criz nbpq zyrz ahjw'
        receiver_email = "vladtivig@gmail.com"
        receiver_password = "lkxc dvpr mrfb mroy"
        temperature_exceeded_message = f"The current temperature is {sensor_temperature}. Would you like to turn on the fan?"
        email_module.send_email(sender_email, sender_password, temperature_exceeded_message, sender_email, receiver_email)
        
        email_module.email_sent = True
        message_response = email_module.receive_email(sender_email, sender_password)
        if(email_module.email_sent and message_response != None):
            if("yes" in message_response.split()[0].lower() and email_module.response_received == False):
                motor.turn_on()
                email_module.response_received = True
                email_module.yes_response_received = True
                email_module.email_sent = False
                return "assets/fan-spin.png"
            elif("yes" not in message_response.split()[0].lower() and email_module.response_received == False):
                motor.turn_off()
                email_module.response_received = True
                email_module.yes_response_received = False
                email_module.email_sent = False
                return "assets/fan.png"
        else:
            motor.turn_off()
            return "assets/fan.png"
    elif(sensor_temperature <= 24 and email_module.email_sent == True):
        sender_email = 'loganluo288@gmail.com'
        sender_password = 'criz nbpq zyrz ahjw'
        receiver_email = "vladtivig@gmail.com"
        message_response = email_module.receive_email(sender_email, sender_password)
        if(message_response != None):
            if("yes" in message_response.split()[0].lower() and email_module.response_received == False):
                motor.turn_on()
                email_module.response_received = True
                email_module.yes_response_received = True
                email_module.email_sent = False
                return "assets/fan-spin.png"
            elif("yes" not in message_response.split()[0].lower() and email_module.response_received == False):
                motor.turn_off()
                email_module.response_received = True
                email_module.yes_response_received = False
                email_module.email_sent = False
                return "assets/fan.png"
        else:
            motor.turn_off()
            return "assets/fan.png"
    else:
        motor.turn_off()
        return "assets/fan.png"

@callback(
    Output(component_id="humidity-gauge", component_property="value"),
    Input(component_id="humidity-read-interval", component_property="n_intervals")
)
def get_humidity(_):
    sensor = DHT.DHT(pin=12)#the pin12 is in the physicl this means that in the GPIO is the 18
    chk = sensor.readDHT11()
    if(chk is sensor.DHTLIB_OK):
        humidity = sensor.humidity  # Call the method to get humidity
        return humidity


if __name__ == '__main__':
    app.run(debug=True)
