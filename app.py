import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go

from textwrap import dedent
from pyarrow import feather
import numpy as np
import pandas as pd


app = dash.Dash()
app.config.supress_callback_exceptions=True

#####load and process data#####

data = feather.read_feather(source='data/aeolus_top5drugs.feather',nthreads=16)

uniq_drugs = data.drug_concept_name.unique()
uniq_drugs = uniq_drugs[np.argsort(uniq_drugs)]

all_age_cat_counts = (data.groupby(['age_cat'])
						  .apply(lambda x : x.shape[0])
					 )
all_age_cat_counts_x = all_age_cat_counts.index.tolist()
all_age_cat_counts_y = all_age_cat_counts.values
all_age_cat_counts_y_norm = np.round((all_age_cat_counts_y / all_age_cat_counts.sum()) * 100,0)


##########

app.layout = html.Div(

	children=[

		dcc.Location(id='url', refresh=True),
		html.Div(id='page-content')
		]
	)	
	
	
index_page = html.Div(
	children=[

		html.H1('Visualizing Drug Safety Data in a Web Framework: Interacting with, understanding, and communicating using Python',
			style={'text-align' : 'center','font-size' : 48}
			),

		dcc.Link('Go to ADR age relation Page', href='/age_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate Drugs',
			href = '/feature_drugs_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate Adverse Reactions',
			href = '/feature_outcomes_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate ADRs',
			href = '/feature_drugs_and_outcomes_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		html.Hr(),

		html.H4("The Food and Drug Administration's Adverse Event Reporting System provides population-level information on drug usage and adverse reactions to drugs (ADRs). We present a standardized, processed version of this ADR data for the public."),

		html.Br(),

		html.H4("Feel free to use the Jupyter notebooks in our github repository SafeDrugs (www.github/NCBI-Hackathons/SafeDrugs) for the data wrangling and code implementation."),

		html.Br(),

		html.H4("Check out the individual fveature links to investigate frequent drugs, adverse reactions, and ADRs. Post issues on our github SafeDrugs (www.github/NCBI-Hackathons/SafeDrugs) for additional features or bugs."),

		html.Br()
		]
	)

feature_drugs_page = html.Div(

	children=[

		html.H1('Investigating Drug usage \nin ADR data',
			style={'text-align' : 'center'}),

		dcc.Link('Go to Home Page', href='/',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate Adverse Reactions',
			href = '/feature_outcomes_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate ADRs',
			href = '/feature_drugs_and_outcomes_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		html.Hr(),

		html.Div(style={},children=[])
		]
	),

feature_outcomes_page = html.Div(

	children=[

		html.H1('Investigating Adverse Reactions from drug usage \nin ADR data',
			style={'text-align' : 'center'}),
		
		dcc.Link('Go to Home Page', href='/',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate Drugs',
			href = '/feature_drugs_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate ADRs',
			href = '/feature_drugs_and_outcomes_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		html.Hr(),

		html.Div(style={},children=[])
		]
	),

feature_drugs_and_outcomes_page = html.Div(

	children=[

		html.H1('Investigating ADRs',
			style={'text-align' : 'center'}),
		
		dcc.Link('Go to Home Page', href='/',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate Drugs',
			href = '/feature_drugs_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Investigate Adverse Reactions',
			href = '/feature_outcomes_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		html.Hr(),

		html.Div(style={},children=[])
		]
	),

age_page = html.Div(

	children=[

		html.H1('ADR age relation'),

		dcc.Link('Go to Home Page', href='/',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Br(),

		dcc.Link('Go to ADR table Page', href='/table_page',
			style={'font-size' : 16,'color' : 'blue'}),

		html.Hr(),

		html.Div(
			style={'class' : "col-sm-4",'border' : '2px solid black',
			'float' : 'left'},
			children=[
			
			html.H1('How many patients are taking these drugs?',
				style={'text-align' : 'center','font-size' : 18}),
			
			dcc.Dropdown(
				id='drug_count',
				options=[{'label' : i, 'value' : i} for i in uniq_drugs],
				value=uniq_drugs[0]),

			html.Div(id='drug_output',
				style={'text-align' : 'center'})

			]),

		dcc.Graph(
			id='drug-reports-at-ages',
			style={'class' : 'col-sm-4','float' : 'right'},
		)

		]
	)


# Update the index
# This callback constantly looks at the page location with id="url",
# and gives the pathname to the function immediately following the callback.
# The function then gives what it returns, which is a new layout.
# That new layout itself has a url! So the new url is displayed
# Every time we click the link, the pathname changes (href) and we get returned the 
# corresponding page. 
@app.callback(
	dash.dependencies.Output('page-content', 'children'),
			  [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/age_page':
		return age_page
	if pathname == '/feature_drugs_page':
		return feature_drugs_page
	if pathname == '/feature_outcomes_page':
		return feature_outcomes_page
	if pathname == '/feature_drugs_and_outcomes_page':
		return feature_drugs_and_outcomes_page
	else:
		return index_page


#Show number of patients taking selected drug in dataset
@app.callback(
	dash.dependencies.Output('drug_output', 'children'),
	[dash.dependencies.Input('drug_count', 'value')])
def callback_drug(value):
	return 'There are {} patients that reported taking {}'.format(
		data.query('drug_concept_name==@value').count().values[0],
		value)

#Update bar graph for drug
@app.callback(
	dash.dependencies.Output('drug-reports-at-ages','figure'),
	[dash.dependencies.Input('drug_count','value')])
def callback_drug_reports_at_ages_bars(value):

	series = (data.query('drug_concept_name == @value')
						   .groupby(['age_cat'])
						   .apply(lambda x : x.shape[0])
						   )
	x = series.index.tolist()
	y = series.values
	y_norm = np.round((series.values / series.sum()) * 100,0)

	drug_trace = go.Bar(
						x=x,
						y=y_norm,
						name='{}'.format(value),
						text=['{} reports'.format(i) for i in y],
						marker=go.Marker(
							color='rgb(55, 83, 109)'
						)
					)

	all_trace = go.Bar(
						x=all_age_cat_counts_x,
						y=all_age_cat_counts_y_norm,
						name='All drugs',
						text=['{} reports'.format(i) for i in all_age_cat_counts_y],
						marker=go.Marker(
							color='rgb(180,180,180)'
						)
					)
	return { 'data' : [
					all_trace,drug_trace
					],
				'layout' : go.Layout(
					title='Patients taking {} at different age intervals'.format(value),
					showlegend=True,
					yaxis = dict(
						title="Percentage of reports",
						type='-'
					),
					xaxis = dict(
						title="Age category"
					),
					legend=go.Legend(
						x=0,
						y=1.0
					),
					margin=go.Margin(l=40, r=20, t=40, b=100)
				)
			}

#enable bootstrap styling
external_css = [["https://bootswatch.com/3/paper/bootstrap.css"]]

for css in external_css:
	app.css.append_css({"external_url": css})


if __name__ == '__main__':
	app.run_server(debug=True)