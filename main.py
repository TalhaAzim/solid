from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """<html>
    <head>
        <title>Solid Blog Simulation</title>
        <body>
            <h1>Solid Blog Simulation</h1>
            <p>Colonel, it's Snake. Do you read me?</p>
        </body>
    </head>
    </html>
    """

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)