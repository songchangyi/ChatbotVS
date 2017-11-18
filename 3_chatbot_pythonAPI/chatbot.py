from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from flask import Flask, render_template, request, jsonify

# *******************************************************************
# Initialize chatbot :
# *******************************************************************
chatbot = ChatBot("myBot")
chatbot.set_trainer(ChatterBotCorpusTrainer)

## train with corpus
chatbot.train("chatterbot.corpus.english")
chatbot.train("chatterbot.corpus.chinese")
chatbot.train("chatterbot.corpus.custom")

# *******************************************************************
# Chatting online using Flask :
# *******************************************************************

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # user inputs
        first = request.form.get('first')
        # get response
        res_reply = str(chatbot.get_response(first))
        #print(res_reply)
        return jsonify(res_reply)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
