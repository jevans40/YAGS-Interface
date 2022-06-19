from flask import Flask, render_template, request
from json import dumps, loads
import requests

app = Flask(__name__)

class GPTquery(object):
    def __init__(self, 
                inputText : str, 
                maxGen = 120, 
                rep_pen = 1.1,
                top_p = 0.9, 
                top_k = 0, 
                tfs = 1.0, 
                temperature = 0.55,
                seq = 1):

        self.inputText = inputText 
        self.maxGen = maxGen if maxGen >= 1 else 1
        self.rep_pen = rep_pen if rep_pen > 0 else 0
        self.top_p = top_p if top_p > 0 else 0
        self.top_k = top_k if top_k > 0 else 0
        self.tfs = tfs if tfs > 0 else 0
        self.temperature = temperature if temperature > 0 else 0
        self.seq = seq if seq >= 1 else 1

class GPTreturn(object):
    def __init__(self,OutputText):
        self.OutputText = OutputText

@app.route("/", methods=["GET","POST"])
def index():
    defaultOptions = GPTquery("")
    return render_template('index.html',options=defaultOptions)

@app.route("/backend/",methods=["GET","POST"])
def backend():
    CurrentOptions = GPTquery("",
                               maxGen = int(request.form['mGen']),
                               temperature = float(request.form['temp']),
                               rep_pen= float(request.form['rPen']),
                               top_p=float(request.form['topP']),
                               top_k=float(request.form['topK']),
                               tfs=float(request.form['tailFS']),
                               seq=int(request.form['num']))
    if request.method == "POST":
        prompt = request.form['prompt']
        CurrentOptions.inputText = prompt
        query = CurrentOptions
        res = requests.post("http://localhost:5001/query/",json=query.__dict__)
        print(f"Got response! {res}")
        if res.status_code == 200:
            txt = GPTreturn(**loads(res.text))
            returnText = prompt + txt.OutputText[0]
        else: 
            returnText = prompt
        return render_template('index.html',prompt = returnText,options=CurrentOptions)
    else:
        return render_template('index.html', prompt = request.form['prompt'], options = CurrentOptions)



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")