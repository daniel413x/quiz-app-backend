from flask import Flask
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv

from blueprints.api.domain.quiz_category.routes import domain_quiz_category_bp
from blueprints.api.domain.quiz_instance.routes import domain_quiz_instance_bp
from blueprints.api.domain.quiz_question.routes import domain_quiz_question_bp
from blueprints.api.domain.quiz.routes import domain_quiz_bp
from blueprints.api.domain.routes import domain_bp
from blueprints.api.domain.user_answer.routes import domain_user_answer_bp
from blueprints.api.domain.quiz_results.routes import domain_quiz_results_bp
from blueprints.test.routes import test_bp
from extensions import db
from consts.routes import API_ROUTE, TEST_ROUTE, QUIZ_ROUTE, QUIZ_CATEGORY_ROUTE, QUIZ_QUESTION_ROUTE, \
    DOMAIN_ROUTE, QUIZ_INSTANCE_ROUTE, USER_ANSWER_ROUTE, QUIZ_RESULTS_ROUTE

load_dotenv()

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
        }
    },
)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(domain_quiz_category_bp, url_prefix=f"/{API_ROUTE}/{DOMAIN_ROUTE}/<domain_slug>/{QUIZ_CATEGORY_ROUTE}")
app.register_blueprint(domain_quiz_question_bp, url_prefix=f"/{API_ROUTE}/{DOMAIN_ROUTE}/<domain_slug>/{QUIZ_QUESTION_ROUTE}")
app.register_blueprint(domain_quiz_bp, url_prefix=f"/{API_ROUTE}/{DOMAIN_ROUTE}/<domain_slug>/{QUIZ_ROUTE}")
app.register_blueprint(domain_quiz_instance_bp, url_prefix=f"/{API_ROUTE}/{DOMAIN_ROUTE}/<domain_slug>/{QUIZ_INSTANCE_ROUTE}")
# need to improve consistency in routing here
# suggest f"/{API_ROUTE}/{DOMAIN_ROUTE}/<domain_slug>/{QUIZ_INSTANCE_ROUTE}/<instance_id>/{USER_ANSWER_ROUTE}"
# domain_quiz_instance_user_answer_bp
app.register_blueprint(domain_user_answer_bp, url_prefix=f"/{API_ROUTE}/{DOMAIN_ROUTE}/<domain_slug>/{USER_ANSWER_ROUTE}/<instance_id>")
app.register_blueprint(domain_quiz_results_bp, url_prefix=f"/{API_ROUTE}/{DOMAIN_ROUTE}/<domain_slug>/{QUIZ_RESULTS_ROUTE}")

app.register_blueprint(domain_bp, url_prefix=f"/{API_ROUTE}/{DOMAIN_ROUTE}")
app.register_blueprint(test_bp, url_prefix=f"/{API_ROUTE}/{TEST_ROUTE}")


@app.cli.command("init-db")
def init_db():
    db.create_all()
