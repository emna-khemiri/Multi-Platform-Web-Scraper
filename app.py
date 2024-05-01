from flask import Flask, render_template, request

from main import process_user, setup_logging


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_info = {
        "first_name": request.form['first_name'].strip(),
        "last_name": request.form['last_name'].strip(),
        "email": request.form['email'].strip(),
        "company_name": request.form['company_name'].strip(),
        "linkedin_username": request.form['linkedin_username'].strip(),
        "behance_username": request.form['behance_username'].strip(),
        "github_username": request.form['github_username'].strip()
    }
    logger = setup_logging()
    process_user(user_info, logger)
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)
