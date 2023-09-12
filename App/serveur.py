from flask import Flask, render_template, request
import re
from simpletransformers.ner import NERModel,NERArgs

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    output = request.form.to_dict()
    inputField = apply_model(output['inputField'])
    
    return render_template('index.html', name = inputField)

def apply_model(sentence):
    dict_color_labal = {
        'B-attitude_constructive' : 'bg-custom-green',
        'I-attitude_constructive' : 'bg-custom-green',
        'B-pensee' : 'bg-custom-orange',
        'I-pensee' : 'bg-custom-orange',
        'B-ethique_pro' : 'bg-custom-purple',
        'I-ethique_pro' : 'bg-custom-purple',
        'B-travail_equipe' : 'bg-custom-yellow',
        'I-travail_equipe' : 'bg-custom-yellow',
        'B-leadership' : 'bg-custom-red',
        'I-leadership' : 'bg-custom-red',
        'B-communication' : 'bg-custom-blue',
        'I-communication' : 'bg-custom-blue',
    }    
    # Apply model
    model = NERModel('camembert', '../model_soft_skills/', use_cuda=False)
    prediction = model.predict([str(sentence)])
    print(prediction)
    balise_html = "<p><span class='text'>"

    for words in prediction[0] :
        for word in words :
            for key, value in word.items():
                if value == 'O' :
                    balise_html += key + ' '  
                else :
                    span_string = '<span class='+dict_color_labal[value]+'>'+str(key)+'</span> '
                    balise_html += span_string
    
    balise_html += "</span></p>"
    return balise_html


# Je suis rigoureux, de, confiance, je suis attentif et à l'écoute, j'aime le management
if (__name__ == '__main__'):
    app.run()
