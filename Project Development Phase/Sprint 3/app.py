from flask import Flask, render_template, redirect, url_for, request
import requests,joblib

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

        X =[[Serial_No,gre,tofel,university_rating,sop,lor,cgpa,yes_no_radio]]
        model = joblib.load('model.pkl')
        result = model.predict(X)[0]

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