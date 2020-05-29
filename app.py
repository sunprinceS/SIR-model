from scipy import interpolate
import dash_table
import mydcc
import dash_bootstrap_components as dbc
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
from scipy.integrate import odeint

### Marcos ###
GAMMA =1.0/10

##############

### Model ###
def sir_diff_eq(y, t, r0, gamma, N, t_y_interpolated):
    S, I, R = y

    def beta(t):
        try:
            return t_y_interpolated[int(t)] * r0 * gamma 
        except:
            return t_y_interpolated[-1] * r0 * gamma

    dSdt = -beta(t) * I * S / N
    dIdt = beta(t) * I * S/N - gamma * I
    dRdt = gamma * I

    return dSdt, dIdt, dRdt

def Model(init_cases, init_date, r0, N, t_y_interpolated=None):
    last_date = np.datetime64("2020-12-31")
    days = int((last_date - np.datetime64(init_date)) / np.timedelta64(1,"D"))

    diff = int((np.datetime64("2020-01-01") - np.datetime64(init_date)) / np.timedelta64(1, "D"))
    t_y_interpolated = t_y_interpolated[(-diff):]

    missing_days_t = int((last_date - np.datetime64("2020-09-01")) / np.timedelta64(1, "D"))
    t_y_interpolated += [t_y_interpolated[-1] for _ in range(missing_days_t+1)]
    

    y0 = N-init_cases , init_cases , 0.0
    t = np.linspace(0,len(t_y_interpolated),len(t_y_interpolated))
    ret = odeint(sir_diff_eq, y0, t, args=( r0, GAMMA, N, t_y_interpolated))
    
    dates = pd.date_range(start=np.datetime64(init_date), periods=days, freq="D")

    S, I, R = ret.T
    r_interpolated = S/N * t_y_interpolated * r0


    return dates, S, I, R, r_interpolated, t_y_interpolated
################################################################################

### CONTROL BOARD ###

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label('疫情開始日'),
                html.Br(),
                dcc.DatePickerSingle(
                    day_size=39,  # how big the date picker appears
                    display_format="MM/DD, YYYY",
                    date='2020-01-21',
                    id='initial_date',
                    min_date_allowed=dt(2019, 12, 31),
                    max_date_allowed=dt(2020, 5, 31),
                    placeholder="initial date"
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("初始病例數"),
                dbc.Input(
                    id="initial_cases", type="number", placeholder="initial_cases",
                    min=0, max=1_000_000, step=1, value=10,
                )
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("人口數 (N)"),
                dbc.Input(
                    id="population", type="number", placeholder="population",
                    min=10_000, max=1_000_000_000, step=10_000, value=24_000_000,
                )
            ]
        ),

        dbc.Alert(f"平均感染週期 D = {int(1 / GAMMA)}"),
        dbc.FormGroup(
            [
                dbc.Label("R0"),
                dbc.Input(
                    id="r0", type="number", placeholder="r0",
                    min = 0, max=5.0, step=0.1, value= 2.5,
                )
            ]
        ),
        dbc.Alert("R = R0 x T x (S/N)", color="success"),

        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/01/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_1',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/02/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_2',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/03/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_3',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/04/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_4',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/05/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_5',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/06/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_6',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/07/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_7',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/08/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_8',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label('傳染率 T at 2020/09/01'),
                html.Br(),
                dcc.Slider(
                    id='t_data_9',
                    min=0.00,
                    max=1.00,
                    step=0.05,
                    value=1.0,
                    tooltip={'always_visible': True, "placement": "bottom"}
                ),
            ]
        ),
        dbc.Button("提交", id="submit-button-state",
                   color="primary", block=True)
    ],
    body=True,
)

######################################################################


### LAYOUT ###
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "科普寫作期末專題 - 瘟疫的傳播"
app.layout = dbc.Container(
    [
        dbc.Jumbotron(
            [
                dbc.Container(
                    [
                        html.H1("一場瘟疫的誕生與消亡", className="display-3"),
                        html.P(
                            "從 SIR model 來模擬疾病的傳播",
                            className="lead",
                        ),
                        html.Hr(className="my-2"),
                    ],
                    fluid=True,
                )
            ],
            fluid=True,
            className="jumbotron bg-white text-dark"
        ),

        dbc.Row(
            [
                # here we place the controls we just defined,
                # and tell them to use up the left 3/12ths of the page.
                dbc.Col(controls, md=3),
                # now we place the graphs on the page, taking up
                # the right 9/12ths.
                dbc.Col(
                    [
                        # the main graph that displays coronavirus over time.
                        dcc.Graph(id='main_graph'),
                        # the graph displaying the R values the user inputs over time.
                        # dcc.Graph(id='t_graph'),
                        # dcc.Graph(id='r_graph'),
                        # the next two graphs don't need as much space, so we
                        # put them next to each other in one row.
                        dbc.Row(
                            [
                                # the graph for the fatality rate over time.
                                dbc.Col(dcc.Graph(id='t_graph'), md=6),
                                # the graph for the daily deaths over time.
                                dbc.Col(dcc.Graph(id="r_graph"), md=6)

                            ]
                        ),
                    ],
                    md=9
                ),
            ],
            align="top",
        ),

        dbc.Jumbotron(
            [
                dbc.Container(
                    [
                        html.P(
                            "Thanks Henri Froese for his great work (https://github.com/hf2000510/infectious_disease_modelling) as my reference",
                            className="lead",
                        ),
                        html.P(
                            "Check the code here: https://gist.github.com/sunprinceS/8af98e7d8f419bc9fbc4cf76f10cfe5a"
                    ),
                    ],
                    fluid=True,
                )
            ],
            fluid=True,
            className="jumbotron bg-white text-dark"
        ),
    ],
    fluid=True,
)


############################################ the dash app callbacks ################################################

@app.callback(
    [dash.dependencies.Output('main_graph', 'figure'),
     dash.dependencies.Output('t_graph', 'figure'),
     dash.dependencies.Output('r_graph', 'figure'),
     ],
     
    [dash.dependencies.Input('submit-button-state', 'n_clicks')],

    [dash.dependencies.State('initial_cases', 'value'),
     dash.dependencies.State('initial_date', 'date'),
     dash.dependencies.State('r0', 'value'),
     dash.dependencies.State('population', 'value'),
     dash.dependencies.State("t_data_1", "value"),
     dash.dependencies.State("t_data_2", "value"),
     dash.dependencies.State("t_data_3", "value"),
     dash.dependencies.State("t_data_4", "value"),
     dash.dependencies.State("t_data_5", "value"),
     dash.dependencies.State("t_data_6", "value"),
     dash.dependencies.State("t_data_7", "value"),
     dash.dependencies.State("t_data_8", "value"),
     dash.dependencies.State("t_data_9", "value"),
     ]
)

def update_graph(_, init_cases, init_date, r0, population,t1,t2,t3,t4,t5,t6,t7,t8,t9):
    last_init_date, last_population = "2020-01-01", 1_000_000

    if not (init_date and population):
        init_date, population = last_init_date, last_population

    t_data_y = [t1, t2, t3, t4, t5, t6, t7, t8, t9]

    f = interpolate.interp1d([0, 1, 2, 3, 4, 5, 6, 7, 8], t_data_y, kind='linear')
    t_dates = pd.date_range(start=np.datetime64(init_date), end=np.datetime64("2020-09-01"), freq="D")
    t_y_interpolated = f(np.linspace(0, 8, num=len(t_dates))).tolist()

    dates, S, I, R, r_over_time, t_over_time = Model(init_cases,init_date, r0, population, t_y_interpolated)

    return {  # return graph for compartments, graph for fatality rates, graph for reproduction rate, and graph for deaths over time
        'data': [
            {'x': dates, 'y': S.astype(int), 'type': 'line', 'name': 'susceptible'},
            {'x': dates, 'y': I.astype(int), 'type': 'line', 'name': 'infected'},
            {'x': dates, 'y': R.astype(int), 'type': 'line', 'name': 'removed'},
        ],
        'layout': {
            'title': 'Compartments over time'
        }
        },{
        'data': [
            {'x': dates, 'y': t_over_time, 'type': 'line', 'name': 'transmission rate'}
        ],
        'layout': {
            'title': 'T over time',
            }
        }, {
        'data': [
            {'x': dates, 'y': r_over_time, 'type': 'line', 'name': 'reproduction number'}
        ],
        'layout': {
            'title': 'R over time',
            }
        }

if __name__ == '__main__':
    app.run_server()
