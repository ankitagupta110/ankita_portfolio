import os
from flask import Flask, render_template

# Create Flask application using the project root as the template folder
app = Flask(__name__, template_folder=".")
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
