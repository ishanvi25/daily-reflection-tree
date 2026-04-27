from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""

    if request.method == "POST":
        replay = request.form.get("replay")

        if replay:
            cmd = ["py", "agent/agent.py", "--replay", replay]
        else:
            cmd = ["py", "agent/agent.py"]

        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

    return render_template("index.html", output=output)


if __name__ == "__main__":
    app.run(debug=True)