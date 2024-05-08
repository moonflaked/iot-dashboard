from dash import Dash, html, Input, Output, callback, dcc, no_update
from dash.exceptions import PreventUpdate
import RPi.GPIO as GPIO
import light_switch as light
import dash_daq as daq
import Freenove_DHT as DHT
import email_send_receive as email_module
import Motor as motor
import dash_bootstrap_components as dbc
import paho.mqtt.client as mqtt
import mqtt_light_intensity as mli
from datetime import datetime
motor.turn_off()

app = Dash(__name__,
           external_stylesheets=[dbc.themes.GRID, 
                                dbc.themes.BOOTSTRAP,
                                 "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
                                 ],
)
iot_dashboard_title = dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H1(
                                    "IoT Dashboard",
                                ),
                                className="dashboard-title inter-title"
                            )
                        )
                    )

temperature_card = dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                html.H2(
                                    "Temperature",    
                                ),
                                className="card-title default-border-color inter-card-title"
                            ),
                            html.Div(
                                daq.Gauge(
                                    id="temperature-gauge",
                                    min=0,
                                    max=50,
                                    size=275,
                                    label="        ",
                                    color={"gradient": True,
                                        "ranges": {
                                            "blue": [0, 15],
                                            "green": [15, 25],
                                            "yellow": [25, 35],
                                            "red": [35, 50]
                                        }
                                        },
                                    showCurrentValue=True,
                                    units="°C",
                                    style={
                                        "fontSize": "1rem"
                                    }
                                )
                            )
                        ],
                        className="card-body default-border-color"
                    ),
                    className="border-0"
                )

humidity_card = dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                html.H2(
                                    "Humidity"
                                ),
                                className="card-title default-border-color inter-card-title"
                            ),
                            html.Div(
                                daq.Gauge(
                                    id="humidity-gauge",
                                    min=20,
                                    max=80,
                                    size=275,
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
                                    label="     ",
                                    color="#3c6bfa",
                                    showCurrentValue=True,
                                    units="%"
                                )
                            ),
                        ],
                        className="card-body default-border-color"
                    ),
                    className="border-0"
                )
light_intensity_card = dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    html.H2(
                                        "Light Intensity"
                                    ),
                                    className="card-title default-border-color inter-card-title"
                                ),
                                html.Div(
                                    [
                                        html.Img(
                                            src="assets/sun-icon.png",
                                        ),
                                        dbc.Progress(value=0, 
                                                        max=1024, 
                                                        style={"minHeight": "30px", "maxWidth": "80%", "fontSize": "2rem"},
                                                        label="0",
                                                        id="light-intensity-bar",
                                                    className="intensity-bar")
                                    ],
                                    className="light-intensity-icon text-align-center"
                                )
                            ],
                            className="card-body default-border-color"

                        ),
                        className="border-0"
                    )

light_status_card = dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    html.H2(
                                        "Light Status"
                                    ),
                                    className="card-title default-border-color inter-card-title"
                                ),
                                html.Div(
                                    [
                                            html.Div(
                                            children=[
                                                html.Img(src="assets/closed-light.png", className="image-icon", id="light-icon-image")
                                            ],
                                            className="image-icon-div"
                                        )
                                    ],
                                    className="text-align-center"
                                )
                            ],
                            className="card-body default-border-color"

                        ),
                        className="border-0"
                    )

fan_status_card = dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                html.H2(
                                    "Fan Status"
                                ),
                                className="card-title default-border-color"
                            ),
                            html.Div(
                                html.Div(
                                    children=[
                                        html.Img(
                                            src="assets/fan.png",
                                            id="fan-icon-image"
                                        )
                                    ],
                                    className="image-icon-div"
                                ),
                                className="text-align-center"
                            )
                        ],
                        className="card-body default-border-color"
                    ),
                    className="border-0"
                )

profile_card = dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                                html.H2(
                                    "Profile"
                                ),
                                className="card-title default-border-color"
                        ),
                        html.Div(
                            [
                                html.Label("RFID ID #:",
                                   
                                    className="header-field-key"
                                ),
                                html.Span(
                                    " aaaaaaa",
                                    id="rfid-id",
                                    className="header-field-rfid-id-value inter-header-field"
                                ),
                            ],
                            className="header-field"
                        ),
                        html.Div(
                            [
                                html.Label("Favorite Temperature:",
                                   
                                    className="header-field-key"
                                ),
                                html.Span(
                                    " aaaaaaa",
                                    id="temperature-id",
                                    className="header-field-value inter-header-field"
                                ),
                            ],
                            className="header-field"
                        ),
                        html.Div(
                            [
                                html.Label("Favorite Light Intensity:",
                                   
                                    className="header-field-key"
                                ),
                                html.Span(
                                    " aaaaaaa",
                                    id="light-id",
                                    className="header-field-value inter-header-field"
                                ),
                            ],
                            className="header-field"
                        ),
                    ],
                    className="card-body default-border-color"
                ),
                className="border-0"
            )            

email_sent_toast = dbc.Toast(
                        "An email has been sent!",
                        id="positioned-toast",
                        header="Light Intensity Threshold Reached",
                        is_open=False,
                        dismissable=True,
                        icon="info",
                        duration=4000,
                        # top: 66 positions the toast below the navbar
                        style={"position": "fixed", "width": 220, "height": 70},
                    )

humidity_read_interval = dcc.Interval(
    id="humidity-read-interval",
    interval=15000,
    n_intervals=0
)

temperature_read_interval = dcc.Interval(
    id="temperature-read-interval",
    interval=2000,
    n_intervals=0
)

mqtt_sub_interval = dcc.Interval(
    id="mqtt-sub-interval",
    interval=5000,
    n_intervals=0
)

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        iot_dashboard_title
                    ]
                ),
                className="g-0"
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    temperature_card,
                                    className="dashboard-card-left dashboard-card",
                                    width={"size":6}
                                ),
                                dbc.Col(
                                    humidity_card,
                                    className="dashboard-card-right dashboard-card",
                                    width={"size":6}
                                   
                                )
                            ],
                           
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            light_intensity_card
                                        ],
                                    ),
                                    className="dashboard-card-left dashboard-card ",
                                    width=6
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            light_status_card
                                        ],
                                       
                                    ),
                                    className="dashboard-card-right ",
                                    width=6
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            fan_status_card
                                        ],
                                       
                                    ),
                                    className="dashboard-card-left",
                                    width=6
                                ),
                                dbc.Col(
                                    html.Div(
                                        [

                                        ],
                                        #className="dev-color-4"
                                    ),
                                    className="dashboard-card-right",
                                    width=6
                                )
                            ]
                        ),
                    ],
                    width=8,
                    #className="dev-color-1"
                ),
                dbc.Col(
                    html.Div(
                        [
                            profile_card
                        ],
                       # className="dev-color-2"
                    ),
                    width=4
                ),
            ],
            className="card-container"
        ),
        email_sent_toast,
        temperature_read_interval,
        humidity_read_interval,
        mqtt_sub_interval
    ],
    className="g-0",
    fluid=True
)


# @callback(
#     [
#         Output(component_id="button-image", component_property="src"),
#         Output(component_id="light-icon-image", component_property="src"),
#     ],
#     Input(component_id="light-button", component_property="n_clicks")
# )
# def change_light_state(n_clicks):
#     # Toggles light state from 0 or 1 indicating whether light is open or closed
#     # The real LED state from the output of the LED pin determines the light state on the dashboard
#     # because we do not want to show a "fake state" to the user
#     calculated_led_state = n_clicks % 2
#     real_led_state = light.switch_state(calculated_led_state)

#     if real_led_state:
#         return "assets/on-button.png", "assets/open-light.png"
#     else:
#         return "assets/off-button.png", "assets/closed-light.png"

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

@callback(
    [
        Output(component_id="light-intensity-bar", component_property="value"),
        Output(component_id="light-intensity-bar", component_property="label"),
        Output(component_id="light-icon-image", component_property="src"),                                           
        Output(component_id="positioned-toast", component_property="is_open"),
        Input(component_id="mqtt-sub-interval", component_property="n_intervals")
    ]
)
def update_light_intensity(_):
    if(mli.curr_light_intensity == None):
        # Do not update the light intensity bar if the light intensity does not exist
        # Because we only want to updte when there is data
        raise PreventUpdate
    else:
        if(int(mli.curr_light_intensity) < 400 and email_module.email_sent_intensity == False):
            sender_email = 'loganluo288@gmail.com'
            sender_password = 'criz nbpq zyrz ahjw'
            receiver_email = "vladtivig@gmail.com"
            receiver_password = "lkxc dvpr mrfb mroy"
            current_time = datetime.now().strftime("%H:%M:%S")
            
            text = f"\nThe Light is ON at {current_time}."
            email_module.send_email(sender_email, sender_password, text, sender_email, receiver_email, email_module.EmailSentSelect.INTENSITY_EMAIL_SEND)
            email_module.email_sent_intensity = True
            light.turn_on()
            return int(mli.curr_light_intensity), mli.curr_light_intensity, "assets/open-light.png", True
        elif(int(mli.curr_light_intensity) < 400 and email_module.email_sent_intensity == True):
            return int(mli.curr_light_intensity), mli.curr_light_intensity, "assets/open-light.png", no_update
        return int(mli.curr_light_intensity), mli.curr_light_intensity, "assets/closed-light.png", no_update




if __name__ == '__main__':
    app.run(debug=True)
    
    
    
