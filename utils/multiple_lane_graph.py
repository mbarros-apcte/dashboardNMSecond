import os

import plotly.graph_objects as go

import random

def _get_input_data_multiple_line_graph_no_dt(lngth=20, num_plans=3):
	res = dict()
	res["x_axis"] = [x for x in range(lngth)]

	res["lst1"] = [random.randint(30,40) for x in range(lngth)]
	res["lst2"] = [random.randint(25, 45) for x in range(lngth)]

	plans = [random.randint(0,lngth) for x in range(num_plans)]
	plans.sort()
	res["plns"] = plans

	# get date for plans
	plnsy = [x for x in range(max(max(res["lst1"]), max(res["lst2"])))]
	plnsy.append(None)

	res["plnsy"]=plnsy
	all_plans_x = []
	all_plans_y= []

	for ii in range(num_plans):
		all_plans_x.extend(plans[ii] for x in range(len(plnsy)))
		all_plans_y.extend(plnsy)

	res["all_plans_x"] = all_plans_x
	res["all_plans_y"] = all_plans_y
	return res

def get_mock_fig_tt_comparison(asset=1):
	input_data = _get_input_data_multiple_line_graph_no_dt(lngth=random.randint(30,40), num_plans=random.randint(3,6))

	# Create traces
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=input_data['x_axis'], y=input_data["lst1"],
							 mode='lines',
							 name='segment 1',
							 line=dict(color='royalblue', width=10, dash='dash')))
	fig.add_trace(go.Scatter(x=input_data['x_axis'], y=input_data["lst2"],
							 mode='lines+markers',
							 name='segment 2',
							 line=dict(color='firebrick', width=10)))

	fig.add_trace(go.Scatter(x=input_data['all_plans_x'], y=input_data["all_plans_y"],
							 mode='lines',
							 name='TOD Plans',
							 line=dict(color='green', width=7, dash='dash')))

	# Edit the layout
	fig.update_layout(title=f'Selected asset {asset}',title_font_size=50,
					   xaxis_title='Time [hh:mm]',
					   yaxis_title='Travel time [s]')
	return fig

if __name__ == '__main__':
	fig = get_mock_fig_tt_comparison(asset=1100)
	#fig.write_html(os.path.join(os.getcwd(),"test.html"))