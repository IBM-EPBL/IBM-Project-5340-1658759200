from flask import Flask, render_template, redirect, url_for, request
import requests, joblib

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("index"))
            arr.append(float(val))
        Serial_No =1
        
        gre = float(request.form['gre'])
        tofel = float(request.form['tofel'])
        university_rating = float(request.form['university_rating'])
        sop = float(request.form['sop'])
        lor = float(request.form['lor'])
        cgpa = float(request.form['cgpa'])
        yes_no_radio = float(request.form['yes_no_radio'])

        X =[[gre,tofel,university_rating,sop,lor,cgpa,yes_no_radio]]


        # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
        API_KEY = "6S922LYgmx66Kf31p7WQqCjc9jyywHJwB9IXjJKdGdW6"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
        API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR ","CGPA", "Research"]], "values": X}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/4d27e05d-bdd3-4437-aa02-e0989a1ed38c/predictions?version=2022-11-18', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        response_scoring = response_scoring.json()

        #model = joblib.load('model.pkl')
        #result = model.predict(X)[0]
        result = response_scoring['predictions'][0]['values'][0][0][0]
        if result> 0.5:
            return redirect((f'/chance/{round(result*100)}'))
        else:
            return redirect((f'/no_chance/{round(result*100)}'))
    else:
        return redirect(url_for("demo"))


@app.route("/home")
def demo():
    return render_template("index.html")

@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", percent=percent)

@app.route("/no_chance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", percent=percent)

if __name__ == "__main__":
    app.run(debug=True)