import logging

import dash
import dash_core_components as dcc
import dash_html_components as html
#import cufflinks as cf
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os
import pickle

from cmps_dash_lyt.layout_comp_central_map import get_central_map
from cmps_dash_lyt.layout_comp_dashboard import get_dashboard_layout
#from analysis.dash_clicable_map.cmps_dash_lyt.layout_comp_sidebar import get_sidebar_layout
from utils.multiple_lane_graph import get_mock_fig_tt_comparison


def get_current_pickle_precom_file():
    return os.path.join(os.getcwd(), "precomputed_data_v1.pickle")

def fetch_precomp_data(pickle_fnm=get_current_pickle_precom_file()):
    with open(pickle_fnm, "rb") as fp:  # Unpickling
        res_data = pickle.load(fp)
    return res_data

mapbox_access_token = open(".mapbox_token").read()
px.set_mapbox_access_token(mapbox_access_token)

# logging
log_name = "logfile.log"
logging.basicConfig(filename=log_name, format='%(asctime)s  %(levelname)-8s %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filemode='w')  # ,
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info("Script is starting...\n")

# initiate app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# get the precomputed values
pickle_fnm = get_current_pickle_precom_file()
prec_data = fetch_precomp_data(pickle_fnm)  # precoumputed in prepare_variables() method
df_scorer_dstrbn = prec_data["scorer_distribution"]

# preset the values
updated_user_inputs = dict()


def design_layout_components(prec_data):
    # sidebar (left)
    # sidebar = get_sidebar_layout()
    sidebar = []

    # map (central)
    central_map = get_central_map(prec_data)

    # dashboard (right)
    dashboard = get_dashboard_layout(prec_data)


    return sidebar, central_map, dashboard




app = dash.Dash(__name__)
server = app.server



'''
~~~~~~~~~~~~~~~~
~~ APP LAYOUT ~~
~~~~~~~~~~~~~~~~
'''
# get app layout components
sidebar, central_map, dashboard = design_layout_components(prec_data)
#app.layout = html.Div(children=[sidebar, central_map, dashboard])

#app.layout = html.Div(children=[central_map, dashboard])
app.layout =  dbc.Col(
    [
        dbc.Row(central_map,style={"height":'60%'}),
       dashboard],style={"height":'100vh'})


import plotly.graph_objects as go
import random

def _get_asset_num(lst_asts):
    res = []
    for item in lst_asts:
        res.append(item['customdata'][0])
    return res

# # CALL BACKS
@app.callback(
    Output('dash_fig1', 'figure'),
    [Input('main_fig', 'selectedData')])
def update_graph_1(sel_fig):

    assets = _get_asset_num(sel_fig["points"])
    assets.sort()
    assets = [str(x) for x in assets]
    print(assets)

    data = []
    for ii in range(3):
        x1 = [random.randint(10,40) for x in range(len(assets))]
        data.append(x1)

    fig = go.Figure(data=go.Heatmap(
                    z = data,
                    x=assets,
                    y=['Morning', 'Afternoon', 'Evening'],
                    hoverongaps = False))

    return fig


# # CALL BACKS
@app.callback(
    Output('dash_fig2', 'figure'),Input('main_fig', 'clickData'))
def update_graph_2(sel_fig):
    asset = sel_fig["points"][0]['customdata'][0]
    print(asset)
    fig = get_mock_fig_tt_comparison(asset=asset)
    for key, value in sel_fig.items():
        print(key, ': fig 2', value)
    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')


# a =  [{'curveNumber': 1, 'pointNumber': 770, 'pointIndex': 770, 'lon': -80.1224, 'lat': 25.92242, 'marker.color': 1, 'bbox': {'x0': 2080.2519817769594, 'x1': 2082.2519817769594, 'y0': 477.6836927609566, 'y1': 479.6836927609566}, 'customdata': [3993, 'Bayview Dr & Collins Av', 7, 1, 23, 'SCOOT', 'D170', '552 Signal Control Cabinet', 'State', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.92242, -80.1224, 'SCOOT', 'NO SCOOT', 'NO SCOOT', 0, 'darkgreen']}]
# b = [{'curveNumber': 1, 'pointNumber': 201, 'pointIndex': 201, 'lon': -80.12197, 'lat': 25.931328, 'marker.color': 1, 'customdata': [5433, 'Collins Av / 167 St / 168 St', 7, 1, 23, 'SCOOT', 'D170', '552 Signal Control Cabinet', 'County', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.931328, -80.12197, 'SCOOT', 'NO SCOOT', 'NO SCOOT', 0, 'darkgreen']},
#     {'curveNumber': 1, 'pointNumber': 768, 'pointIndex': 768, 'lon': -80.12203, 'lat': 25.929892, 'marker.color': 1, 'customdata': [2995, 'Collins Av & SR-826 S', 7, 1, 23, 'SCOOT', 'D170', '552 Signal Control Cabinet', 'State', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.929892, -80.12203, 'SCOOT', 'NO SCOOT', 'SCOOT', 0, 'darkgreen']},
#     {'curveNumber': 1, 'pointNumber': 769, 'pointIndex': 769, 'lon': -80.12237, 'lat': 25.923798, 'marker.color': 1, 'customdata': [3490, 'Collins Av & 159 St', 7, 1, 23, 'SCOOT', 'D170', '552 Signal Control Cabinet', 'State', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.923798, -80.12237, 'SCOOT', 'NO SCOOT', 'NO SCOOT', 0, 'darkgreen']},
#     {'curveNumber': 1, 'pointNumber': 773, 'pointIndex': 773, 'lon': -80.12227, 'lat': 25.926996, 'marker.color': 1, 'customdata': [4900, 'Atlantic Av & Collins Av', 7, 1, 23, 'SCOOT', 'D170', '552 Signal Control Cabinet', 'State', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.926996, -80.12227, 'SCOOT', 'NO SCOOT', 'NO SCOOT', 0, 'darkgreen']},
#     {'curveNumber': 1, 'pointNumber': 774, 'pointIndex': 774, 'lon': -80.12509, 'lat': 25.92977, 'marker.color': 1, 'customdata': [4990, 'SR-826 @ 300 Blk', 7, 1, 23, 'SCOOT', 'D170E', '552 Signal Control Cabinet', 'State', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.92977, -80.12509, 'SCOOT', 'NO SCOOT', 'NO SCOOT', 0, 'darkgreen']},
#     {'curveNumber': 1, 'pointNumber': 775, 'pointIndex': 775, 'lon': -80.12201, 'lat': 25.93056, 'marker.color': 1, 'customdata': [5253, 'Collins Av & SR-826 WB', 7, 1, 23, 'SCOOT', 'D170', '552 Signal Control Cabinet', 'County', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.93056, -80.12201, 'SCOOT', 'NO SCOOT', 'NO SCOOT', 0, 'darkgreen']},
#     {'curveNumber': 1, 'pointNumber': 887, 'pointIndex': 887, 'lon': -80.12176, 'lat': 25.934149, 'marker.color': 1, 'customdata': [4733, 'Collins Av & 170 St', 7, 1, 91, 'SCOOT', 'D170', '552 Signal Control Cabinet', 'State', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.934149, -80.12176, 'SCOOT', 'NO SCOOT', 'SCOOT', 0, 'darkgreen']},
#     {'curveNumber': 1, 'pointNumber': 889, 'pointIndex': 889, 'lon': -80.12187, 'lat': 25.9326, 'marker.color': 1, 'customdata': [5727, 'Collins Av @ 16900 Blk', 7, 1, 91, 'SCOOT', 'D170', '552 Signal Control Cabinet', 'County', 'ATMS', 'Existing', 'Sunny Isles Beach', 25.9326, -80.12187, 'SCOOT', 'NO SCOOT', 'SCOOT', 0, 'darkgreen']}]
