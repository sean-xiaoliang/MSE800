from flask import Flask, request

app = Flask(__name__)

PAGE = """
<h1>BMI Calculator</h1>
<form method="post">
    Weight (kg): <input type="text" name="weight"><br><br>
    Height (cm): <input type="text" name="height"><br><br>
    <input type="submit" value="Calculate">
</form>
<h2>{result}</h2>
"""


@app.route("/", methods=["GET", "POST"])
def bmi():
    result = ""
    if request.method == "POST":
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        bmi = weight / (height / 100) ** 2
        result = "Your BMI is {:.2f}".format(bmi)
    return PAGE.format(result=result)


if __name__ == "__main__":
    app.run()
