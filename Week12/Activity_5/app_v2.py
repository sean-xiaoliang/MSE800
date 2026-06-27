from flask import Flask, request

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BMI Calculator</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: "Segoe UI", system-ui, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .card {{
            background: #fff;
            width: 100%;
            max-width: 380px;
            padding: 40px 32px;
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
        }}
        h1 {{
            text-align: center;
            color: #333;
            font-size: 26px;
            margin-bottom: 4px;
        }}
        .subtitle {{
            text-align: center;
            color: #999;
            font-size: 13px;
            margin-bottom: 28px;
        }}
        label {{
            display: block;
            color: #555;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        input[type="text"] {{
            width: 100%;
            padding: 12px 14px;
            margin-bottom: 18px;
            border: 2px solid #e2e2e2;
            border-radius: 10px;
            font-size: 15px;
            transition: border-color 0.2s;
        }}
        input[type="text"]:focus {{
            outline: none;
            border-color: #667eea;
        }}
        button {{
            width: 100%;
            padding: 13px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.1s, box-shadow 0.2s;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }}
        .result {{
            margin-top: 26px;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            background: {bg};
            color: {fg};
            display: {show};
        }}
        .result .value {{ font-size: 34px; font-weight: 700; }}
        .result .category {{ font-size: 15px; margin-top: 4px; }}
        .error {{
            margin-top: 22px;
            text-align: center;
            color: #e53935;
            font-size: 14px;
            display: {err_show};
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>BMI Calculator</h1>
        <p class="subtitle">Body Mass Index</p>
        <form method="post">
            <label>Weight (kg)</label>
            <input type="text" name="weight" placeholder="e.g. 70">
            <label>Height (m)</label>
            <input type="text" name="height" placeholder="e.g. 1.75">
            <button type="submit">Calculate</button>
        </form>
        <div class="result">
            <div class="value">{value}</div>
            <div class="category">{category}</div>
        </div>
        <p class="error">{error}</p>
    </div>
</body>
</html>
"""


def category_style(bmi):
    if bmi < 18.5:
        return "Underweight", "#e3f2fd", "#1565c0"
    if bmi < 25:
        return "Normal", "#e8f5e9", "#2e7d32"
    if bmi < 30:
        return "Overweight", "#fff8e1", "#f9a825"
    return "Obese", "#ffebee", "#c62828"


@app.route("/", methods=["GET", "POST"])
def bmi():
    fields = {
        "value": "", "category": "", "error": "",
        "bg": "transparent", "fg": "#333",
        "show": "none", "err_show": "none",
    }
    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            if weight <= 0 or height <= 0:
                fields["error"] = "Please enter positive numbers."
                fields["err_show"] = "block"
            else:
                value = weight / height ** 2
                category, bg, fg = category_style(value)
                fields.update(
                    value="{:.1f}".format(value),
                    category=category, bg=bg, fg=fg, show="block",
                )
        except ValueError:
            fields["error"] = "Please enter valid numbers."
            fields["err_show"] = "block"
    return PAGE.format(**fields)


if __name__ == "__main__":
    app.run(port=5001)
