import os
from dash import Dash, html, dcc, callback, Input, Output, State, no_update
from embedchain import App
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

# Create a bot instance
os.environ["OPENAI_API_KEY"]
ai_bot = App.from_config(config_path="config.yaml")

# Embed resources: websites, PDFs, videos
ai_bot.add("https://www.wildbirdfund.org/page-sitemap.xml", data_type="sitemap")
ai_bot.add("https://nycaudubon.org/our-work/conservation/project-safe-flight")
ai_bot.add("Birds Flying Into Windows.pdf", data_type='pdf_file')
ai_bot.add("https://www.youtube.com/watch?v=l8LDTRxc0Bc")
ai_bot.add("https://wildbirdrehab.com/sitemap.xml", data_type="sitemap")
ai_bot.add("How to find a wildlife rehabilitator _ The Humane Society of the United States.pdf", data_type='pdf_file')
ai_bot.add("https://www.avianandanimal.com/bird-nutrition.html")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Submit button 
submit_icon = DashIconify(icon="guidance:down-angle-arrow", style={"marginLeft": 5})
submit_button = dbc.Button(id='submit-btn', children=['Submit', submit_icon], style={'margin-bottom': '20px'})

# Speak button
speak_icon = DashIconify(icon="mdi:speak", style={"marginLeft": 5})
speak_button = dbc.Button(id='speak-btn', children=['Speak', speak_icon], style={'margin-top': '20px', 'margin-bottom': '20px'})

# Visitor count
visitor_count = 0

# Layout
app.layout = dbc.Container([
    dbc.Container([
        html.H1('WILD BIRD FUND', style={'text-align': 'center', 'color': 'red'}),
        html.H2('Hello birds lovers and rescuers!'), 
        html.H3('This AI Chatbot can provide answers to all your questions ranging from wild bird rescuing organizations near you '
                'to how to keep the city birds safe and take care of them when injured.'),
        html.Label(['Currently the Wild Bird Fund have office only in ', 
                html.A('Manhattan.', href='https://maps.app.goo.gl/3cgmsobhkp5SFtuk8', target='_blank')]),
        html.Br(),
        html.Hr(),      
        html.Label('Ask your question:', style={'margin-bottom': '20px'}),
        html.Br(),
        dcc.Textarea(id='question-area', value=None, style={'width': '25%', 'height': 100, 'margin-bottom': '20px'}),
        html.Br(),
        submit_button,
        dcc.Loading(id="load", children=html.Div(id='response-area', children='')),
        html.Hr()
        ]),
    dbc.Container([
        html.Footer(
            children=[
                html.Label(['If you wish to get pictorial responses to your questions click ', 
                        html.A('here.', href='https://images.google.com', target='_blank')]),
                html.Br(),
                html.Hr(),
                html.Label(['To avail the text-to-speech feature of the response, run the app through the ', 
                        html.A('GitHub repo.', href='https://github.com/jmanali1996/WBF-Chatbot.git', target='_blank')], 
                        style={'margin-bottom': '50px'}),
                html.Br(),
                html.P(id='visitor_count_display', style={'text-align': 'right'}),
                html.Hr(),
                html.I('An app by Manali Jain', style={'color': 'darkgrey'}),
                html.Br(),
                html.I(['Reach out for feedback at ',
                    html.A('jmanali1996@gmail.com', href='mailto:jmanali1996@gmail.com', target="_blank")],
                    style={'color': 'darkgrey'})
            ]
        )
    ])
])

# Submit callback
@callback(
    Output('response-area', 'children'),
    Input('submit-btn', 'n_clicks'), 
    State('question-area', 'value'),
    prevent_initial_call=True
)
def create_response(_, question):
    # What kind of glass should I use to keep birds safe from window collisions?
    if not question:
        return f'Please enter your question.'
    else:
        answer = ai_bot.query(question)
        return answer

# Visitor count callback
@app.callback(
    Output('visitor_count_display', 'children'),
    Input('visitor_count_display', 'children')
)
def update_visitor_count(value):
    global visitor_count
    visitor_count += 1
    return f'Total visitors: {visitor_count}'


if __name__ == '__main__':
    app.run_server(debug=False)
