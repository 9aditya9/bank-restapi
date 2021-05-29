# import os
# from flask import Flask, request, jsonify
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# # from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# engine = create_engine(os.getenv("DATABASE_URI"))
# db = scoped_session(sessionmaker(bind=engine))


# @app.route("/", methods=["GET"])
# def autocomplete():
# 	q = request.args.get('q')
# 	if not q:
# 		q = 'STATE'
# 	result = db.execute("SELECT bank_name FROM bank_branches WHERE (bank_name LIKE :q) LIMIT 3", {"q": q + "%"})
# 	# return jsonify({"result": [dict[row] for row in result]})
# 	return jsonify({'result': [dict(row) for row in result]})


import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def auto():
	q = 'STATE'
	result = db.session.execute("SELECT bank_name FROM bank_branches WHERE (bank_name LIKE :q) LIMIT 3", {"q": q + "%"}).fetchall()
	return jsonify({"result": [dict(row) for row in result]})
