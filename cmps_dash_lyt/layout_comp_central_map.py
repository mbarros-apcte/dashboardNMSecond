from dash import dcc, html


def get_central_map(prec_data):
    cent_fig = prec_data["multi_layer_fig"]

    # central_map = dcc.Graph(id='main_fig', figure=fig, style={'margin-left':'15%', "align":"left", "width":"58%", "height":"80vh" }) #style=get_content_style())
    central_map = dcc.Graph(id='main_fig', figure=cent_fig,
                                      style={'margin-left': '0%', "align": "left", "width": "100%", "height": "100%"})

    return central_map

