from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

#from plotly_utils._test_figures import #get_test_fig_hor_bar, test_figure_conf_matr, #test_fig_scatterbox

def get_placeholder_for_precomputed_score_fig():
	res = html.Div([
		html.P("Attributes (x-axis):"),
		dcc.Checklist(
			id='x-axis',
			options=[{'value': x.replace("_"," "), 'label': f' {x.replace("_"," ")}'}
					 for x in ["week_plans",  "wknd_plans",  "week_tods",  "wknd_tods",  "week_free", 'wknd_free',
					 'max_cycle', 'min_cycle', 'veh_phs', 'ped_nc_phs',
					 'spec_ped_treat', 'preemption', 'ovrlps', 'lead_lag', 'distance_to_ramp',
					 "tot_num_nearby_assets"]],
			value=['week plans'],
			style={"margin-left": "15px"}
			#labelStyle={'float': 'left'}
		),
		html.P("Distribution of scorers (y-axis):"),
		dcc.RadioItems(
			id='y-axis',
			options=[{'value': x, 'label': y}
					 for x,y in zip(["scorer_val", "weigthed_score_val"],[" scorer   ", " weighted scorer   "])],
			value='scorer_val',
			labelStyle={'display': 'inline-block'}
		),
		dcc.Graph(id="box-plot"),
	])
	return res

def get_dashboard_layout(prec_data):
	dashboard = dbc.Row([
		dbc.Col(
			dcc.Graph(
				id='dash_fig1',
				figure={},
				style={
					'background-color': '#f8f9fa'
				}
			)
		),
		dbc.Col(
			dcc.Graph(
				id='dash_fig2',
				figure={},
				style={
					'background-color': '#f8f9fa'
				}
			)
		)	
	])
	return dashboard