import dash
import time
import dash_core_components as dcc
import plotly.graph_objs as go
from getdata import getData
from datetime import date
from dash.dependencies import Input, Output, State
import dash_html_components as html
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
from functools import reduce
from operator import getitem


times = [];
nums = [];

def get_show_scatter():
    if dayValue != 4:
        global startTime;
        global endTime;
        startTime = int(time.time() * 1000) - dayValue* 1000*60*60*24
        endTime = int(time.time() * 1000)
    # 接口数据
    global times;
    global nums;
    times = [];
    nums = [];
    for item in getData():
        if int(item['time']) > startTime and int(item['time']) < endTime:
            times.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(item['time'])/1000)));
            nums.append(int(item['num']));
    sctx = times;
    scty = nums;
    trace = go.Scatter(
        x=sctx,
        y=scty,
        name='活跃用户',
    )

    layout=go.Layout(
        title='每日新增用户',
        yaxis={
            'hoverformat': '' #如果想显示小数点后两位'.2f'，显示百分比'.2%'
        },
    )

    df = px.data.stocks()
    fig = go.Figure(
        data = [trace],
        layout = layout
    )
    # print(1,times[int(len(times)/2)])
    fig.add_trace(
        go.Scatter(
            x=[position,position],
            y=[0,1100],
            mode='lines',
            name='AAPL'
        ))

    return fig

# 通用CSS格式
cardStyle = {"width": "100%","margin":"20px 20px"};


# 创建app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# formdata
dayValue = 2;
startTime = 1;
endTime = 1921462506;
limitValue = 0;
isSubmit = 0;
position = '2022-11-20 15:02:26';
# 时间区间快速定义
timeSelectorComp = html.Div(
    [
        dbc.RadioItems(
            id="input-radio",
            options=[
                    {"label": "1 Days", "value": 1},
                    {"label": "2 Days", "value": 2},
                    {"label": "3 Days", "value": 3},
                    {"label": "自定义区间", "value": 4},
            ],
            value=dayValue,
            inline=True,
            style={"width": "90%","margin-left":"30px"}
        ),
        html.Div(id="radioitems-checklist-output",style={"opacity":"0"}),
    ],
    className="mb-2",
)
@app.callback(
    Output("radioitems-checklist-output", "children"),
    [Input('input-radio', 'value')],
)
def on_radio_change(value):
    global dayValue;
    dayValue = value;
    return value


# 日期选择器物
dataPickComp = html.Div(
    [
        dcc.DatePickerRange(
            id="input-time",
            month_format='MMM Do, YY',
            end_date_placeholder_text='MMM Do, YY',
            start_date=date(2022, 11, 21),
            end_date=date(2022, 11, 22),
            style = cardStyle
        ),
        html.Div(id="DatePickerRange-output",style={"opacity":"0"}),
    ]
)
@app.callback(
    Output("DatePickerRange-output", "children"),
    [Input('input-time', 'start_date'),
    Input('input-time', 'end_date'),],
)
def on_time_change(start_date,end_date):
    global startTime
    global endTime
    startTime = int(time.mktime(time.strptime(start_date+' 00:00:00', "%Y-%m-%d %H:%M:%S")))*1000
    endTime = int(time.mktime(time.strptime(end_date+' 23:59:59', "%Y-%m-%d %H:%M:%S")))*1000
    return  start_date + '-' + end_date


# 范围内样本数目
limitComp = html.Div(
    [
        dbc.Input(type="number", min=0, max=10, step=1,value=0,disabled="True"),
        html.Br(),
        html.P(id="limit-output"),
    ]
)

# 弹窗
Modal = [
            html.H1("历史时间范围设定", className="card-title",style=cardStyle),
            dbc.ModalHeader('历史时间范围设定'),
            dbc.ModalBody(
                html.Div(
                    [
                        dbc.Card([
                            html.H4("时间区间快速定义", className="card-title1",style = cardStyle),
                            timeSelectorComp,
                        ]),
                        dbc.Card([
                            html.H4("自定义区间", className="card-title2",style = cardStyle),
                            dataPickComp
                        ], style={"width": "100%","margin-top":"20px"}),
                        dbc.Card([
                            html.H4("范围内样本数目", className="card-title3",style = cardStyle),
                            limitComp
                        ], style={"width": "100%","margin-top":"20px"}),
                    ]
                ),
                style={"width": "100%"}
            ),
            dbc.ModalFooter([
                dbc.Button(
                    "cancel", id="cancel",color="secondary", className="ms-auto", n_clicks=0
                ),
                dbc.Button(
                    "submit", id="submit",color="primary", className="ms-auto", n_clicks=0
                )
            ]),
        ]
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("cancel", "n_clicks"), Input("submit", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2,n3, is_open):
    global isSubmit
    if n3 > isSubmit:
        isSubmit = n3
        return not is_open
    if n1 or n2:
        return not is_open
    return is_open


layout = dbc.Card(
    [
        dbc.Button("高级设定", id="open",color="primary", n_clicks=0,
                    style={"width": "18rem","margin":"auto"}),
        dcc.Graph(
            id='show_scatter',
            figure=get_show_scatter()
        ),
        html.Div(id="fig-opacity",style={"opacity":"0"}),
        dbc.Modal(
            Modal,
            id="modal",
            is_open=False,
        ),
    ],
    style={"width": "100%","margin":"auto"}
)

app.layout = layout


@app.callback(
    Output("show_scatter", "figure"),
    [Input("submit", "n_clicks"),Input('show_scatter','hoverData')]
)
def uptView(n_clicks,hov_data):
    if (type(hov_data).__name__=='dict'):
        global position
        print(position)
        position = hov_data['points'][0]['x']
    return get_show_scatter();

if __name__ == '__main__':
    app.run_server(debug=True)