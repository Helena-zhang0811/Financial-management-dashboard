import dash
import pandas as pd
from dash import html, dcc, Input, Output, callback, State, dash_table
import dash_bootstrap_components as dbc
import os
import shutil
from flask import send_file
import plotly.express as px

if os.path.exists('financial_data.csv'):
    df = pd.read_csv('financial_data.csv')
else:
    df = pd.DataFrame(columns=['Date', 'Bond', 'Stock', 'Sport', 'Earning', 'Food Spending', 'Game Spending',
                            'Clothes Spending', 'Travelling Spending', 'Education Spending', 'Other Spending'])
    df.set_index('Date', inplace=True)
    df.to_csv('financial_data.csv')


spending_to_subtract = df[['Food Spending', 'Game Spending', 'Clothes Spending', 'Travelling Spending', 'Education Spending', 'Other Spending']].sum().sum()
earning_return = df[['Bond', 'Stock', 'Sport', 'Earning']].sum().sum()
result = earning_return - spending_to_subtract

data = pd.DataFrame({
    'Category': ['Total Earning', 'Total Spending', 'Total Investment Result', 'Total Saving'],
    'Balance': [10, 20, 30, 2]
})

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    html.Div([
            dbc.Row([dbc.Col(html.H4(""))]),

            dbc.Row([
                    dbc.Col(html.H2(f'Your Financial Account: ${result}'),
                                    style={'font-family': 'Verdana', 'font-size': '24px', 'color': '#000000', 'font-weight': 'bold', 'text-align': 'center'})
                    ],
                    style={"border": "2px solid #000", "height": "60px", "width": "1000px", "margin": "0 auto",
                           "background-image": "linear-gradient(to right, #49BBDA , #F7DE54 )", "padding": "10px"}),

            dbc.Row([dbc.Col(html.H4(""))]),

            dbc.Row([
                    dbc.Col(
                        [
                        html.Div(['Choose Date: ', dcc.Input(id='date_finance', value='YYYY-MM-DD', type='text')]),
                        html.Div('Investment Type: '),
                        dcc.Dropdown(id='select-column1',
                            options=[
                                    {'label': 'Bond Returns/Losses', 'value': 'Bond'},
                                    {'label': 'Stock Returns/Losses', 'value': 'Stock'},
                                    {'label': 'Sport Returns/Losses', 'value': 'Sport'},
                            ],
                            value='Bond', multi=False),

                        html.Div(['Your returns/losses: ',
                                  dcc.Input(id='returns_losses', value='...', type='number')]),
                        dbc.Col([html.Button('Save', id='save-button1',
                                             style={'backgroundColor': '#097A1C', 'color': 'white'}), html.Div(id='output-message1')]),
                        dcc.DatePickerRange(id='date-range1', start_date='2023-01-01', end_date='2023-12-31', display_format='YYYY-MM-DD')

                        ], width=4, style={"background-color": '#DBDCD6', "border": "1.5px solid #000", "margin": "5px"}
                    ),

                    dbc.Col(
                        [
                        html.Div(['Choose Date: ', dcc.Input(id='date_saving', value='YYYY-MM-DD', type='text')]),
                            html.Div('Earning/Spending Type: '),
                        dcc.Dropdown( id='select-column2',
                            options=[
                                    {'label': 'Earning', 'value': 'Earning'},
                                    {'label': 'Food Spending', 'value': 'Food Spending'},
                                    {'label': 'Game Spending', 'value': 'Game Spending'},
                                    {'label': 'Clothes Spending', 'value': 'Clothes Spending'},
                                    {'label': 'Travelling Spending', 'value': 'Travelling Spending'},
                                    {'label': 'Education Spending', 'value': 'Education Spending'},
                                    {'label': 'Other Spending', 'value': 'Other Spending'},
                            ],
                            value='Earning', multi=False),
                        html.Div(['Your Earning/Spending: ',
                                  dcc.Input(id='earning_spending', value='...', type='number')]),
                        dbc.Col([html.Button('Save', id='save-button2',
                                             style={'backgroundColor': '#097A1C', 'color': 'white'}), html.Div(id='output-message2')]),
                        dcc.DatePickerRange(id='date-range2', start_date='2023-01-01', end_date='2023-12-31', display_format='YYYY-MM-DD')
                        ], width=4, style={"background-color": '#DBDCD6', "border": "1.5px solid #000", "margin": "5px"}
                    ),

                    dbc.Col([
                        html.H3('Your Deposit Database: '),
                        dbc.Col(html.A('Download saved data', id='download-link', href='/download')),
                        html.Br(),
                        html.H3('Markets'),
                        html.A('Link to Market index', href = 'https://www.marketindex.com.au/'),
                    ], width=3, style={"background-color": '#DBDCD6 ', "border": "1.5px solid #000", "margin": "5px"}),
            ]),


            dbc.Row([
                dbc.Col([dcc.Graph(id='line-chart', style={'width': '100%', 'height': '400px'}),
                        dcc.DatePickerRange(id='date-range3', start_date='2023-01-01', end_date='2023-12-31',
                                            display_format='YYYY-MM-DD', style={'margin-left': '60px', 'background-color': 'lightblue'}),
            ], width=4),

                dbc.Col([dcc.Graph(id='bar-chart', style={'width': '100%', 'height': '350px'}),
                        html.Div([dash_table.DataTable(id='custom-table',
                                                       columns=[{'name': 'Financial Category', 'id': 'Category'},
                                                                {'name': 'Financial Balance ($)', 'id': 'Balance'}],
                                                       data=data.to_dict('records'), style_cell={'textAlign': 'center'},
                                                       style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#49BBDA','color': 'black'},
                                                                               {'if': {'row_index': 'even'}, 'backgroundColor': '#A2D9F7', 'color': 'black'}]
                                                       )]),
                        html.Br(),
                        ], width=4),


                dbc.Col([
                    html.H3('Latest Financial and Business News'),
                    html.Iframe(src="https://www.bloomberg.com/asia", width="100%", height=480)
                ], width=4),
        ]),

    ]),
    fluid=True,
)

@app.callback(
    Output('custom-table', 'data'),
    Input('date-range3', 'start_date'),
    Input('date-range3', 'end_date')
)
def update_table_data(start_date, end_date):
    filtered_data0 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    earning_total = filtered_data0['Earning'].sum()
    spending_columns = ['Food Spending', 'Game Spending', 'Clothes Spending',
                        'Travelling Spending', 'Education Spending', 'Other Spending']
    spending_total = filtered_data0[spending_columns].sum().sum()
    investment_columns = ['Bond', 'Stock', 'Sport']
    investment_total = filtered_data0[investment_columns].sum().sum()
    spending_to_subtract1 = filtered_data0[
        ['Food Spending', 'Game Spending', 'Clothes Spending', 'Travelling Spending', 'Education Spending',
         'Other Spending']].sum().sum()
    earning_return1 = filtered_data0[['Bond', 'Stock', 'Sport', 'Earning']].sum().sum()
    saving_total = earning_return1 - spending_to_subtract1

    data.loc[data['Category'] == 'Total Earning', 'Balance'] = earning_total
    data.loc[data['Category'] == 'Total Spending', 'Balance'] = spending_total
    data.loc[data['Category'] == 'Total Investment Result', 'Balance'] = investment_total
    data.loc[data['Category'] == 'Total Saving', 'Balance'] = saving_total
    return data.to_dict('records')


@callback(
    Output('output-message1', 'children'),
    Output('output-message2', 'children'),
    Input('save-button1', 'n_clicks'),
    Input('save-button2', 'n_clicks'),
    State('date_finance', 'value'),
    State('returns_losses', 'value'),
    State('date_saving', 'value'),
    State('earning_spending', 'value'),
    Input('select-column1', 'value'),
    Input('select-column2', 'value')
)
def save_data_to_csv(n_clicks1, n_clicks2, date_finance, returns_losses, date_saving, earning_spending, select_column1, select_column2):
    if n_clicks1 or n_clicks2:
        global df
        if n_clicks1:
            new_row = {'Date': date_finance}
            new_row[select_column1] = returns_losses
            new_row[select_column2] = None
        elif n_clicks2:
            new_row = {'Date': date_saving}
            new_row[select_column1] = None
            new_row[select_column2] = earning_spending

        df = pd.concat([df, pd.DataFrame([new_row])])
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values(by='Date', ascending=True, inplace=True)
        df.to_csv('financial_data.csv',
                  columns=['Date', 'Bond', 'Stock', 'Sport', 'Earning', 'Food Spending', 'Game Spending',
                           'Clothes Spending', 'Travelling Spending', 'Education Spending', 'Other Spending'], index=False)

    return f'{select_column1}: ${returns_losses} saved', f'{select_column2}: ${earning_spending} saved'


@app.callback(
    Output('line-chart', 'figure'),
    Input('date-range1', 'start_date'),
    Input('date-range1', 'end_date')
)
def update_line_chart(start_date, end_date):
    filtered_df1 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    filtered_df1 = filtered_df1.groupby('Date').agg({'Stock': 'sum', 'Bond': 'sum', 'Sport': 'sum'}).reset_index()
    fig = px.line(filtered_df1, x='Date', y=['Stock', 'Bond', 'Sport'], line_shape='linear')
    fig.update_yaxes(title_text='Financial Returns/Losses ($)')
    fig.update_xaxes(title_text='')
    fig.update_layout(
        xaxis_title_font=dict(size=1),
        yaxis_title_font=dict(size=12)
    )
    return fig


@app.callback(
    Output('bar-chart', 'figure'),
    Input('date-range2', 'start_date'),
    Input('date-range2', 'end_date')
)
def update_bar_chart(start_date, end_date):
    filtered_df2 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    total_values = filtered_df2[['Earning', 'Food Spending', 'Game Spending', 'Clothes Spending', 'Travelling Spending',
                                 'Education Spending', 'Other Spending']].sum()
    total_values.index = ['Earning', 'Food', 'Game', 'Clothes', 'Travelling', 'Education', 'Other']
    color_sequence = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    fig = px.bar(x=total_values.index, y=total_values, color=total_values.index, color_discrete_sequence=color_sequence)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='Earning/Spending ($)')
    fig.update_layout(
        xaxis_title_font=dict(size=1),
        yaxis_title_font=dict(size=12)
    )
    fig.update_xaxes(tickfont=dict(size=10))
    return fig


def download_file():
    current_path = os.path.abspath('financial_data.csv')
    desktop_path = os.path.expanduser("~/Desktop/financial_data.csv")
    shutil.copy(current_path, desktop_path)

    return send_file(desktop_path, as_attachment=True, cache_timeout=0)


if __name__ == '__main__':
    app.run_server(debug=True)

