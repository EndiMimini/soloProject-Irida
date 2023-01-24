from flask_app import app
from flask_app.controllers import organizations
from flask_app.controllers import developers
from flask_app.controllers import positions
from flask_app.controllers import skills



if __name__ == "__main__":
    app.run(debug=True)