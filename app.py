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
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def auto():
	q = 'STATE'
	result = db.session.execute("SELECT bank_name FROM bank_branches WHERE (bank_name LIKE :q) LIMIT 3", {"q": q + "%"}).fetchall()
	return jsonify({"result": [dict(row) for row in result]})

@app.route("/api/branches/autocomplete")
def autocomplete():
	q = request.args.get('q').upper()
	limit = request.args.get('limit')
	offset = request.args.get('offset')
	if not offset:
		offset = 0
	if not limit:
		limit = 0
	if not q:
		q = 'A'
	result = db.session.execute("SELECT * FROM bank_branches WHERE (branch LIKE :q) ORDER BY ifsc ASC LIMIT (:limit) OFFSET (:offset)", {"q": q + "%", "limit": int(limit), "offset": int(offset)}).fetchall()
	return jsonify({"result": [dict(row) for row in result]})

@app.route("/api/branches")
def searchapi():
	q = request.args.get('q').upper()
	limit = request.args.get('limit')
	offset = request.args.get('offset')
	if not offset:
		offset = 0
	if not limit:
		limit = 0
	if not q:
		q = 'A'
	result = db.session.execute("SELECT * FROM bank_branches WHERE (branch LIKE :q) OR (address LIKE :q) OR (city LIKE :q) OR (district LIKE :q) OR (state LIKE :q) ORDER BY ifsc ASC LIMIT (:limit) OFFSET (:offset)", {"q": q + "%", "limit": int(limit), "offset": int(offset)}).fetchall()
	return jsonify({"result": [dict(row) for row in result]})
