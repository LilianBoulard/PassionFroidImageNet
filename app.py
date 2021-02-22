"""

For this app to work, two environment variables need to be set:
`PFIN_SERVER`: The endpoint leading to the MongoDB server.
`PFIN_SECRET`: A secret key used by Flask.

"""

import os

from flask import Flask, render_template


app = Flask(__name__)

# Get Flask secret
secret_env_var = 'PFIN_SECRET'
secret = os.getenv(secret_env_var)
if not secret:
    raise ValueError(f'{secret_env_var} environment variable is not set')
app.secret_key = secret.encode()


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
