import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import datetime
import os

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Creating TS Domain"

app.layout = html.Div([
    html.Div([
        html.H1("Creating TS Domain"),
        html.Div([
            dcc.Markdown('''
                **Simplified ts.xpt Creation Guide**
            '''),
            html.Br(),
            dcc.Markdown('''
                **About phuse Package**
            '''),
            html.Br(),
            html.A('Source Code', href='https://github.com/TuCai/phuse/blob/master/inst/examples/07_genTS/app.R', target='_blank'),
        ], className='list-group'),
    ], className='jumbotron text-center'),
    
    html.Div([
        html.Div([
            dcc.Tabs(id='tabs', value='create-tab', children=[
                dcc.Tab(label='Create', value='create-tab', children=[
                    html.Div([
                        html.Label('Study ID (STUDYID)'),
                        dcc.Input(
                            id='studyid',
                            type='text',
                            placeholder='Enter Study ID',
                            required=True,
                            minLength=1,
                            maxLength=200,
                        ),
                        html.Br(),
                        html.Label('Study Type Parameter (TSPARMCD)'),
                        dcc.Dropdown(
                            id='tsparmcd',
                            options=[
                                {'label': 'Clinical (SSTDTC)', 'value': 'SSTDTC'},
                                {'label': 'Nonclinical (STSTDTC)', 'value': 'STSTDTC'},
                            ],
                            value='STSTDTC',
                            required=True,
                        ),
                        html.Br(),
                        html.Label('Study Start Date (TSVAL)'),
                        dcc.DatePickerSingle(
                            id='tsval',
                            display_format='YYYY-MM-DD',
                            min_date_allowed=datetime.datetime(1960, 1, 1),
                            max_date_allowed=datetime.datetime.now(),
                            placeholder='Select a date',
                        ),
                        html.Br(),
                        html.Label('Exception Code (TSVALNF)'),
                        dcc.Dropdown(
                            id='tsvalnf',
                            options=[
                                {'label': 'NA', 'value': 'NA'},
                                {'label': '__Blank__', 'value': ''},
                            ],
                            value='',
                        ),
                    ]),
                    html.Br(),
                    html.Div([
                        html.Button('Download', id='download', className='btn btn-primary', disabled=True),
                    ], className='text-center'),
                ]),
                dcc.Tab(label='View', value='view-tab', children=[
                    html.Br(),
                    html.Div([
                        html.Div(id='table-container'),
                    ]),
                ]),
            ]),
        ], className='col-8'),
        html.Div([
            html.Button(
                'Show/Hide Sidebar',
                id='toggle-sidebar',
                className='btn btn-info btn-block',
            ),
            html.Br(),
            html.Div([
                html.Ul([
                    html.Li(html.A('Simplified ts.xpt Creation Guide', href='https://www.fda.gov/industry/study-data-standards-resources/study-data-submission-cder-and-cber', target='_blank')),
                    html.Li(html.A('About phuse Package', href='https://github.com/TuCai/genTS/blob/master/inst/apps/07_genTS/www/install_phuse_pkg.png', target='_blank')),
                    html.Li(html.A('Source Code', href='https://
