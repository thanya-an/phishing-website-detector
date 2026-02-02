import os
from flask import Flask, render_template, request
from phishing_detector import predict_single_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = ""
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            prediction = predict_single_url(url)
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
