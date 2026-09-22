from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>🚀 BlogSphere LIVE! Anti-Gravity ON! ✨</h1>"
