import os
from dash import Dash, html, dcc, callback, Input, Output, State
from embedchain import App
from gtts import gTTS
import playsound
#pip install -r requirements.txt

# Create a bot instance
os.environ["OPENAI_API_KEY"] = "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"
ai_bot = App.from_config(config_path="config.yaml")

# Embed resources: websites, PDFs, videos
ai_bot.add("https://www.wildbirdfund.org/page-sitemap.xml", data_type="sitemap")
ai_bot.add("https://nycaudubon.org/our-work/conservation/project-safe-flight")
ai_bot.add("Birds Flying Into Windows.pdf", data_type='pdf_file')
ai_bot.add("https://www.youtube.com/watch?v=l8LDTRxc0Bc")
ai_bot.add("https://wildbirdrehab.com/sitemap.xml", data_type="sitemap")
ai_bot.add("How to find a wildlife rehabilitator _ The Humane Society of the United States.pdf", data_type='pdf_file')
ai_bot.add("https://www.avianandanimal.com/bird-nutrition.html")
ai_bot.add("https://glassdoctor.com/sites/default/files/content/blog/images/mdg_ouw_how_to_keep_birds_from_hitting_windows_bloghero_may19_20190205_1-compress.jpg")

app = Dash()
app.layout = html.Div([
    html.Div([
        html.H1('WILD BIRD FUND', style={'text-align': 'center', 'color': 'red'}),
        html.H2('Hello birds lovers and rescuers!'), 
        html.H3('This AI Chatbot can provide answers to all the queries ranging from wild bird rescuing organizations near you '
                'to how how to keep city birds safe and take care of them when injured.'),
        html.Label(['Currently the Wild Bird Fund have office only in ', 
                html.A('Manhattan.', href='https://maps.app.goo.gl/3cgmsobhkp5SFtuk8', target='_blank')]),
        html.Br(),
        html.Hr(),      
        html.Label('Ask your question:', style={'margin-bottom': '20px'}),
        html.Br(),
        dcc.Textarea(id='question-area', value=None, style={'width': '25%', 'height': 100, 'margin-bottom': '20px'}),
        html.Br(),
        html.Button(id='submit-btn', children='Submit', style={'margin-bottom': '20px'}),
        dcc.Loading(id="load", children=html.Div(id='response-area', children='')),
        html.Button(id='speak-btn', children='Speak', style={'margin-bottom': '20px'}),
        html.Hr()
        ]),
    html.Footer([
        html.Label(['If you wish to get pictorial responses to your queries, click ', 
                html.A('here.', href='https://images.google.com', target='_blank')])
        ])
])

@callback(
    Output('response-area', 'children'),
    [Input('submit-btn', 'n_clicks'), 
    Input('speak-btn', 'n-clicks')],
    State('question-area', 'value'),
    prevent_initial_call=True
)
def create_response(_, question):
    # What kind of glass should I use to keep birds safe from window collisions?
    answer = ai_bot.query(question)
    return answer

def speak_text(n_clicks, answer):
    recite = gtts.gTTS(answer, lang='en')
    playsound.playsound(recite)

def update_output(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run_server(debug=False)
