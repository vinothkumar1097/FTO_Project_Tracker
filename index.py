import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import dash_auth #for setting passwords (pip install dash-auth)
import base64
import io
#
#
#
USERNAME_PASSWORD_PAIRS = [['vinoth','1996'],['sathish','1992'],['abdul','1991'], ['raj', '1978'], ['aaron','1988']]
#
app = dash.Dash(__name__)
app.title = "FTO Project Tracker"
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server
app.config['suppress_callback_exceptions']=True

#append css
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
#image_url = 'data:image/png;base64,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'
image_url = 'data:image/png;base64,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'
#

# colors for stages
co = {
        # "completed": "#17A05D",
        # "development": "#FF7700",
        # "yet to start": "#4A8AF4",
        # "study":"#FBD45A",
        # "deployed": "#FC0000",
        # "uat":"#FFCD42",
        # "no status":"#1B100C"
        "completed": "#70AD47",
        "development": "#8EA9DB",
        "yet to start": "#A5A5A5",
        "study": "#7030A0",
        "deployed": "#375623",
        "uat": "#FFC000",
        "no status": "#00B0F0",
        "on hold": "#FF0000",
        "pipeline": "#F700B3"
    }

#Dropdown workout
options1 = [{'label':tic, 'value':tic} for tic in ['All']]
options2 = [{'label':tic, 'value':tic} for tic in ['All']]
options3 = [{'label':tic, 'value':tic} for tic in ['All']]
app.layout = html.Div(id='container', children=[
        html.Div(id='header', children=['Project Tracker',
            # html.H1(id='title1', children=['Project Tracker']),
            html.Img(id='pic1', src=image_url)
        ]),
        html.Div(className='clear'),
        # html.Br(),

        html.Div(id='upload-section', children=[
            # html.H4(id='title2', children=['Upload Files']),
            dcc.Upload(id='upload-data', multiple=False,  children=['Drag and Drop or ', html.A('Select a File (accepts *.xlsx, *.csv)')],
                        style={
                            'width': '95%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '2px',
                            'borderStyle': 'dashed',
                            'border-color': 'white',
                            'borderRadius': '15px',
                            'textAlign': 'center',
                            'margin-left':'20px',
                            'margin-right':'0px',
                            'font-size':'20px',
                            'color':'white'
                              })
        ]),
        html.Div(className='clear'),
        html.Br(),

        html.Div(id='choose-list', children=[
            #first dropdown
            html.Div(id='choose-list1', children=[
                html.H5(id='c1', children=['Select GBU :']),
                dcc.Dropdown(id='dd1',
                             options = options1,
                             # value=options1[0]['value'],
                             placeholder='Filter GBU', multi=True)
             ], className='four columns'),

            #second dropdown
            html.Div(id='choose-list2', children=[
                html.H5(id='c2', children=['Select Scrum :']),
                dcc.Dropdown(id='dd2',
                             options = options2,
                             # value=options2[0]['value'],
                             placeholder='Filter Scrum', multi=True)
             ], className='three columns'),

            #third dropdown
            html.Div(id='choose-list3', children=[
                html.H5(id='c3', children=['Select Developer :']),
                dcc.Dropdown(id='dd3',
                             options=options3,
                             # value=options3[0]['value'],
                             placeholder='Filter Developer', multi=True)
             ], className='five columns'),

            #button
            html.Div(id='btn', children=[
                html.Button(
                    id='propagate-button',
                    n_clicks=0,
                    children='a', style={'display':'none'}
                ),
            ])
        ]),
        html.Div(className='clear'),
        html.P('Once you dropped the file, fill all dropdowns to populate the chart and play with it.', style={'color':'white', 'margin-left': '5px'}),
        html.Br(),

        html.Div(id='graph-container', children=[
            html.Div(id='graph-container1', children=[
                html.Div(id='g1', children=[
                    dcc.Graph(id='graph1',
                              figure={
                                  'data': [go.Pie(
                                            visible='legendonly', opacity=0, hoverinfo='none'
                                            )
                                          ],
                                  'layout': go.Layout(
                                    title='<b><i>No combinations found to plot this graph</i></b>',
                                    titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'), #Gravitas One
                                    font={'color': '#DC4D41'},
                                    plot_bgcolor='#000000', paper_bgcolor='#000000'
                                                 )
                                     },
                              config={'displayModeBar':False}
                              )
                ], className='six columns'),
                html.Div(id='g2', children=[
                    dcc.Graph(id='graph2',
                              figure={
                                  'data': [go.Bar(visible=False, marker=dict(opacity=0))],  # datas1,
                                  'layout': go.Layout(
                                        title='<b><i>No combinations found to plot this graph</i></b>',
                                        titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                                        font={'color': '#DC4D41'},
                                        xaxis=dict(showgrid=False,zeroline=False,showline=False,showticklabels=False),
                                        yaxis=dict(showgrid=False,zeroline=False,showline=False,showticklabels=False),
                                        showlegend=False,
                                        plot_bgcolor='#000000', paper_bgcolor='#000000'
                                    )
                                     },
                              config={'displayModeBar':False}
                              )
                ], className='six columns')
                ], className='row'),

            html.Div(id='graph-container2', children=[
                html.Div(id='g3', children=[
                    dcc.Graph(id='graph3',
                              figure={
                                  'data': [go.Bar(visible=False, marker=dict(opacity=0))],  # datas1,
                                  'layout': go.Layout(
                                        title='<b><i>No combinations found to plot this graph</i></b>',
                                        titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                                        font={'color': '#DC4D41'},
                                        xaxis=dict(showgrid=False,zeroline=False,showline=False,showticklabels=False),
                                        yaxis=dict(showgrid=False,zeroline=False,showline=False,showticklabels=False),
                                        showlegend=False,
                                        plot_bgcolor='#000000', paper_bgcolor='#000000'
                                    )
                                     },
                              config={'displayModeBar':False}
                              )
                ], className='four columns'),
                html.Div(id='g4', children=[
                    dcc.Graph(id='graph4',
                              figure={
                                  'data': [go.Bar(visible=False, marker=dict(opacity=0))],  # datas1,
                                  'layout': go.Layout(
                                      title='<b><i>No combinations found to plot this graph</i></b>',
                                      titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                                      font={'color': '#DC4D41'},
                                      xaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
                                      yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
                                      showlegend=False,
                                      plot_bgcolor='#000000', paper_bgcolor='#000000'
                                  )
                              },
                              config={'displayModeBar': False}
                              )
                ], className='eight columns')
            ], className='row')
        ]),


        # html.Button(
        #     id='propagate-button',
        #     n_clicks=0,
        #     children='Propagate Table Data'
        # ),


        # html.Br(),
        # html.H5("Filter Column"),
        # dcc.Dropdown(id='dropdown_table_filterColumn',
        #     multi = False,
        #     placeholder='Filter Column'),

        html.Br(id='clear'),
        html.Div(id='excel-table', children=[
            html.Div(dt.DataTable(rows=[{}], id='table', max_rows_in_viewport=8))
        ]),
        html.Div(className='clear'),
        html.Br(),

        html.Footer(id='notes', children=html.Div([
                                            html.Span('Developed by VK.  ', style={'color':'white'}),
                                            html.A('Click here to mail', href='mailto:vinol1097@gmail.com', title='Vinod L')])
                    )

        # dcc.ConfirmDialog(
        #     id='confirm',
        #     message='No Possible Combinations to plot graphs. Please try with different combinations.',
        #     submit_n_clicks=1,
        #     cancel_n_clicks=1
        # )

        ])

# Functions

# file upload function
global df1
def parse_contents(contents, filename):
    global df1
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df1 = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        elif 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df1 = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return None

    df1 = df1.drop_duplicates()
    df1['GBU'].fillna('Unknown', inplace=True)
    df1['Scrum Master'].fillna('Unknown', inplace=True)
    df1['Status'].fillna('No Status', inplace=True)
    df1['Developer Name'].fillna('No Developer', inplace=True)
    return df1

def dataset(i, dfs):
    datas = []
    if i==1: gbus = dfs['GBU'].unique().tolist()
    elif i==2: gbus = dfs['Scrum Master'].unique().tolist()
    elif i==3: gbus = dfs['Developer Name'].unique().tolist()
    stats = df1['Status'].unique().tolist()
    for status in stats:
        ydata = []
        filtered_df2 = dfs[(dfs['Status']==status)]
        for gbu in gbus:
            if i==1: row_count = filtered_df2[(filtered_df2['GBU'] == gbu)].shape[0]
            elif i==2: row_count = filtered_df2[(filtered_df2['Scrum Master'] == gbu)].shape[0]
            elif i==3: row_count = filtered_df2[(filtered_df2['Developer Name'] == gbu)].shape[0]
            if row_count >= 0: ydata.append(row_count)
            else: ydata.append(0)
        if (i==1) or (i==3): trace = go.Bar(x=gbus, y=ydata, name=status, marker=dict(color=co[status.lower()]))
        if (i==2): trace = go.Bar(x=ydata,y=gbus,name=status, orientation='h', marker=dict(color=co[status.lower()]))
        if i==1: datas.append(trace)
        elif i==2: datas.append(trace)
        elif i==3: datas.append(trace)
    return datas

    return fig

# callback table creation
@app.callback(Output('table', 'rows'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename'),
               Input('dd1', 'value'),
               Input('dd2', 'value'),
               Input('dd3', 'value')]
              )
def update_output(contents, filename, gbu, scrum, dev):
    if contents is not None:
        df1 = parse_contents(contents, filename)
        print(df1.shape[0], df1.columns)
        if df1 is not None:
            filtered_frame = df1.copy()
            try:
                if len(gbu) > 0: filtered_frame = filtered_frame[filtered_frame.GBU.isin(list(gbu))]
                if (len(scrum) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[filtered_frame['Scrum Master'].isin(list(scrum))]
                if (len(dev) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[filtered_frame['Developer Name'].isin(list(dev))]
                if filtered_frame.shape[0] > 0:
                    return filtered_frame.to_dict('records')
                else:
                    print('No records to bounce back')
                    return df1.to_dict('records')
            except:
                print('No records to bounce back-Error cache')
                return df1.to_dict('records')
        else:
            return [{}]
    else:
        return [{}]

# @app.callback(Output('dd1', 'options'),
#               [Input('table', 'rows'),
#                Input('upload-data', 'contents')])
# def update_dropdown1(tablerows, contents):
#     if contents is not None:
#         dff1 = pd.DataFrame(tablerows)
#         if 'GBU' in dff1.columns:
#             options1 = [{'label': tic, 'value': tic} for tic in dff1['GBU'].unique()]
#             return options1
#         else:
#             return []
#     else:
#         return []
#
#
# @app.callback(Output('dd2', 'options'),
#               [Input('table', 'rows'),
#                Input('upload-data', 'contents')])
# def update_dropdown2(tablerows, contents):
#     if contents is not None:
#         dff1 = pd.DataFrame(tablerows)
#         if 'Scrum Master' in dff1.columns:
#             options2 = [{'label': tic, 'value': tic} for tic in dff1['Scrum Master'].unique()]
#             return options2
#         else:
#             return []
#     else:
#         return []
#
# @app.callback(Output('dd3', 'options'),
#               [Input('table', 'rows'),
#                Input('upload-data', 'contents')])
# def update_dropdown3(tablerows, contents):
#     if contents is not None:
#         dff1 = pd.DataFrame(tablerows)
#         if 'Developer Name' in dff1.columns:
#             options3 = [{'label': tic, 'value': tic} for tic in dff1['Developer Name'].unique()]
#             return options3
#         else:
#             return []
#     else:
#         return []

@app.callback(Output('dd1', 'options'),
              [Input('upload-data', 'contents'),  Input('upload-data', 'filename')])
def update_dropdown1(contents, filename):
    if contents is not None:
        df1 = parse_contents(contents, filename)
        print(df1.shape[0], df1.columns)
        try:
            if df1 is not None:
                dff1 = df1.copy()
                if 'GBU' in dff1.columns:
                    options1 = [{'label': tic, 'value': tic} for tic in dff1['GBU'].unique()]
                    return options1
                else:
                    return []
            else:
                return []
        except:
            return []
    else:
        return []


@app.callback(Output('dd2', 'options'),
              [Input('upload-data', 'contents'),  Input('upload-data', 'filename')])
def update_dropdown2(contents, filename):
    if contents is not None:
        df1 = parse_contents(contents, filename)
        print(df1.shape[0], df1.columns)
        try:
            if df1 is not None:
                dff1 = df1.copy()
                if 'Scrum Master' in dff1.columns:
                    options2 = [{'label': tic, 'value': tic} for tic in dff1['Scrum Master'].unique()]
                    return options2
                else:
                    return []
            else:
                return []
        except:
            return []
    else:
        return []

@app.callback(Output('dd3', 'options'),
              [Input('upload-data', 'contents'),  Input('upload-data', 'filename')])
def update_dropdown3(contents,filename):
    if contents is not None:
        df1 = parse_contents(contents, filename)
        print(df1.shape[0], df1.columns)
        try:
            if df1 is not None:
                dff1 = df1.copy()
                if 'Developer Name' in dff1.columns:
                    options3 = [{'label': tic, 'value': tic} for tic in dff1['Developer Name'].unique()]
                    return options3
                else:
                    return []
            else:
                return []
        except:
            return []
    else:
        return []


@app.callback(Output('graph1', 'figure'),
              [Input('dd1', 'value'),
               Input('dd2', 'value'),
               Input('dd3', 'value')])
def update_graph1(gbu, scrum, dev):
    filtered_frame = df1.copy()
    print('df1 has rows : ', df1.shape[0])
    if (len(gbu) > 0) : filtered_frame = filtered_frame[filtered_frame.GBU.isin(list(gbu))]
    if (len(scrum) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[filtered_frame['Scrum Master'].isin(list(scrum))]
    if (len(dev) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[filtered_frame['Developer Name'].isin(list(dev))]
    print('Filtered frame has rows : ', filtered_frame.shape[0])
    #update graph
    if filtered_frame.shape[0] > 0:
        filtered_frame = filtered_frame
        print('l2')
        # Workaround for Graph1
        track1 = pd.value_counts(filtered_frame['GBU'].values, sort=False).to_dict()
        labels1 = list(track1.keys())
        values1 = list(track1.values())

        fig = {
            'data': [go.Pie(
                labels=labels1, values=values1,
                hoverinfo='label+value', textinfo='label',
                textfont=dict(size=15),
                hole=0.5,
                opacity=1,
                visible=True,
                marker=dict(line=dict(color='#000000', width=0.5)))
                     ],
            'layout': go.Layout(
                title='<b><i>GBU vs Count</i></b>',
                titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                font={'color': '#DC4D41'},
                plot_bgcolor='#000000', paper_bgcolor='#000000'
                                 )
             }
        print('l3')
        return fig
    else:
        print('No combinations found on graph1')
        fig = {
            'data': [go.Pie(
                 labels=['A','B'], values=['1','2'],
                 visible=True, opacity=0, showlegend=False, hoverinfo='none'
                )],
            'layout': go.Layout(
                title='<b><i>No Points to plot.<br>Try with different combinations....</i></b>',
                titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                font={'color': '#DC4D41'},
                annotations=None,grid=None,plot_bgcolor='#000000', paper_bgcolor='#000000'

            )
        }
        return fig

@app.callback(Output('graph2', 'figure'),
              [Input('dd1', 'value'),
               Input('dd2', 'value'),
               Input('dd3', 'value')
               ])
def update_graph2(gbu, scrum, dev):
    filtered_frame = df1.copy()
    if len(gbu) > 0: filtered_frame = filtered_frame[filtered_frame.GBU.isin(list(gbu))]
    if (len(scrum) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[
        filtered_frame['Scrum Master'].isin(list(scrum))]
    if (len(dev) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[
        filtered_frame['Developer Name'].isin(list(dev))]
    print('Filtered frame has rows : ', filtered_frame.shape[0])

    # update graph
    if filtered_frame.shape[0] > 0:
        filtered_frame = filtered_frame

        fig = {
            'data': dataset(1,filtered_frame),#datas1,
            'layout': go.Layout(
                title='<b><i>GBU vs Status</i></b>',
                titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                xaxis=dict(title='GBU', showgrid=False),
                yaxis=dict(title='No. Of Projects', showgrid=False),
                font={'color': '#DC4D41'},
                barmode='stack',plot_bgcolor='#000000', paper_bgcolor='#000000'
            )
        }

        return fig
    else:
        print('No Combinations found for this points')
        fig = {
            'data': [go.Bar(visible=False, marker=dict(opacity=0))],  # datas1,
            'layout': go.Layout(
                title='<b><i>No Points to plot.<br>Try with different combinations....</i></b>',
                titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                xaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
                annotations=None,
                font={'color': '#DC4D41'},plot_bgcolor='#000000', paper_bgcolor='#000000'
            )
        }

        return fig


@app.callback(Output('graph3', 'figure'),
              [Input('dd1', 'value'),
               Input('dd2', 'value'),
               Input('dd3', 'value')
               ])
def update_graph3(gbu, scrum, dev):
    filtered_frame = df1.copy()
    if len(gbu) > 0: filtered_frame = filtered_frame[filtered_frame.GBU.isin(list(gbu))]
    if (len(scrum) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[
        filtered_frame['Scrum Master'].isin(list(scrum))]
    if (len(dev) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[
        filtered_frame['Developer Name'].isin(list(dev))]

    # update graph
    if filtered_frame.shape[0] > 0:
        filtered_frame = filtered_frame
        fig = {
            'data': dataset(2, filtered_frame),  # datas1,
            'layout': go.Layout(
                    title='<b><i>Scrum vs Status</i></b>',
                    titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                    xaxis=dict(title='No. Of Projects', showgrid=False),
                    yaxis=dict(title='Scrum', showgrid=False),
                    font={'color': '#DC4D41'},
                    barmode='stack',plot_bgcolor='#000000', paper_bgcolor='#000000'
                                 )
        }
        return fig
    else:
        print('No Combinations found for this points')
        fig = {
            'data': [go.Bar(visible=False, marker=dict(opacity=0))],  # datas1,
            'layout': go.Layout(
                title='<b><i>No Points to plot.<br>Try with different combinations....</i></b>',
                titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                xaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
                annotations=None,
                font={'color': '#DC4D41'},plot_bgcolor='#000000', paper_bgcolor='#000000'
            )
        }

        return fig

@app.callback(Output('graph4', 'figure'),
              [Input('dd1', 'value'),
               Input('dd2', 'value'),
               Input('dd3', 'value')
               ])
def update_graph4(gbu, scrum, dev):
    filtered_frame = df1.copy()
    if len(gbu) > 0: filtered_frame = filtered_frame[filtered_frame.GBU.isin(list(gbu))]
    if (len(scrum) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[
        filtered_frame['Scrum Master'].isin(list(scrum))]
    if (len(dev) > 0) and (filtered_frame.shape[0] > 0): filtered_frame = filtered_frame[
        filtered_frame['Developer Name'].isin(list(dev))]

    # update graph
    if filtered_frame.shape[0] > 0:
        filtered_frame = filtered_frame
        fig = {
            'data': dataset(3, filtered_frame),  # datas1,
            'layout': go.Layout(
                                title='<b><i>Developer vs Status</i></b>',
                                titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                                xaxis=dict(title='Developer', showgrid=False),
                                yaxis=dict(title='No. Of Projects', showgrid=False),
                                font={'color': '#DC4D41'},
                                barmode='stack',plot_bgcolor='#000000', paper_bgcolor='#000000'
                              )
             }

        return fig
    else:
        print('No Combinations found for this points')
        fig = {
            'data': [go.Bar(visible=False, marker=dict(opacity=0))],  # datas1,
            'layout': go.Layout(
                title='<b><i>No Points to plot.<br>Try with different combinations....</i></b>',
                titlefont=dict(size=25, family='Times New Roman, Monospace', color='#DC4A3E'),
                xaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
                annotations=None,
                font={'color': '#DC4D41'},plot_bgcolor='#000000', paper_bgcolor='#000000'
            )
        }

        return fig

if __name__ == '__main__':
    app.run_server(debug=True)

