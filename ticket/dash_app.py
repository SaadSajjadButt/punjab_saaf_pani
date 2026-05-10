from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output
from .models import Tickets, Zone, Division, District, City, Categories, Feedback, SatisfactionStatus
import pandas as pd

# Initialize Dash app
app = DjangoDash("ComplaintDashboard")  # Safe: only imported in apps.py.ready()

# Layout
app.layout = html.Div([
    html.H1("Complaint Dashboard"),

    html.Div([
        html.Label("Select Zone:"),
        dcc.Dropdown(id='zone-dropdown', placeholder='All Zones')
    ], style={'width': '24%', 'display': 'inline-block', 'margin-right': '1%'}),

    html.Div([
        html.Label("Select Division:"),
        dcc.Dropdown(id='division-dropdown', placeholder='All Divisions')
    ], style={'width': '24%', 'display': 'inline-block', 'margin-right': '1%'}),

    html.Div([
        html.Label("Select District:"),
        dcc.Dropdown(id='district-dropdown', placeholder='All Districts')
    ], style={'width': '24%', 'display': 'inline-block', 'margin-right': '1%'}),

    html.Div([
        html.Label("Select City:"),
        dcc.Dropdown(id='city-dropdown', placeholder='All Cities')
    ], style={'width': '24%', 'display': 'inline-block'}),

    html.Hr(),

    html.Div(id='kpi-cards', style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px'}),

    dcc.Graph(id='tickets-by-category'),

    dcc.Graph(id='feedback-satisfaction')
])

# Populate Zone Dropdown
@app.callback(
    Output('zone-dropdown', 'options'),
    Input('zone-dropdown', 'value')  # dummy input to trigger
)
def populate_zones(_):
    zones = Zone.objects.filter(is_active=1)
    return [{'label': z.description, 'value': z.id} for z in zones]

# Populate dependent dropdowns
@app.callback(
    Output('division-dropdown', 'options'),
    Output('district-dropdown', 'options'),
    Output('city-dropdown', 'options'),
    Input('zone-dropdown', 'value'),
    Input('division-dropdown', 'value'),
    Input('district-dropdown', 'value')
)
def update_dependent_dropdowns(zone_id, division_id, district_id):
    divisions = Division.objects.filter(is_active=1)
    districts = District.objects.filter(is_active=1)
    cities = City.objects.filter(is_active=1)

    if zone_id:
        divisions = divisions.filter(zone_id=zone_id)
    if division_id:
        districts = districts.filter(division_id=division_id)
    if district_id:
        cities = cities.filter(district_id=district_id)

    return (
        [{'label': d.description, 'value': d.id} for d in divisions],
        [{'label': d.description, 'value': d.id} for d in districts],
        [{'label': c.description, 'value': c.id} for c in cities],
    )

# Update KPIs and Charts
@app.callback(
    Output('kpi-cards', 'children'),
    Output('tickets-by-category', 'figure'),
    Output('feedback-satisfaction', 'figure'),
    Input('zone-dropdown', 'value'),
    Input('division-dropdown', 'value'),
    Input('district-dropdown', 'value'),
    Input('city-dropdown', 'value')
)
def update_dashboard(zone_id, division_id, district_id, city_id):
    tickets = Tickets.objects.all()
    if zone_id:
        tickets = tickets.filter(zone_id=zone_id)
    if division_id:
        tickets = tickets.filter(division_id=division_id)
    if district_id:
        tickets = tickets.filter(district_id=district_id)
    if city_id:
        tickets = tickets.filter(city_id=city_id)

    # KPI cards
    total = tickets.count()
    resolved = tickets.filter(resolution_status=1).count()
    open_tickets = tickets.filter(resolution_status=0).count()

    kpi_cards = [
        html.Div(f"Total Tickets: {total}", style={'padding': '10px', 'border': '1px solid black', 'flex': '1'}),
        html.Div(f"Resolved Tickets: {resolved}", style={'padding': '10px', 'border': '1px solid black', 'flex': '1'}),
        html.Div(f"Open Tickets: {open_tickets}", style={'padding': '10px', 'border': '1px solid black', 'flex': '1'}),
    ]

    # Tickets by category chart
    df_cat = pd.DataFrame(list(tickets.values('complaint_category__description')))
    if not df_cat.empty:
        cat_counts = df_cat['complaint_category__description'].value_counts()
    else:
        cat_counts = pd.Series(dtype=int)

    tickets_fig = {
        'data': [{
            'x': cat_counts.index.tolist(),
            'y': cat_counts.values.tolist(),
            'type': 'bar'
        }],
        'layout': {'title': 'Tickets by Category'}
    }

    # Feedback satisfaction chart
    feedbacks = Feedback.objects.filter(ticket__in=tickets)
    df_feedback = pd.DataFrame(list(feedbacks.values('satisfaction_status__description')))
    if not df_feedback.empty:
        fb_counts = df_feedback['satisfaction_status__description'].value_counts()
    else:
        fb_counts = pd.Series(dtype=int)

    feedback_fig = {
        'data': [{
            'x': fb_counts.index.tolist(),
            'y': fb_counts.values.tolist(),
            'type': 'bar'
        }],
        'layout': {'title': 'Feedback Satisfaction'}
    }

    return kpi_cards, tickets_fig, feedback_fig