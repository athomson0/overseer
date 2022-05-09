from dataclasses import dataclass, field
import sys
import pathlib
from typing import Dict, List
sys.path.insert(1, str(pathlib.Path(__file__).parent.parent))
sys.path.insert(1, str(pathlib.Path(__file__).parent.parent / "monitor"))

import json
from flask import Flask, jsonify
from common.database import Database
from models.service import Service

app = Flask(__name__)
database = Database(no_init=True)

@app.after_request
def set_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def serialize(sa_query):
    return [r.serialize() for r in sa_query]

@dataclass
class ApiResponse:
    results: dict = field(default_factory=dict)
    error: bool = False
    error_messages: list = field(default_factory=list)

@app.route("/services", methods=["GET"])
def get_services():
    resp = ApiResponse()
    
    try:
        all_services = database.session.query(Service).all()
    except Exception as e:
        resp.error = True
        resp.error_messages.append(str(e))
        return jsonify(resp)

    if not all_services:
        resp.error = True
        resp.error_messages.append("No services found")
        print(resp)
        return jsonify(resp)

    resp.results = serialize(all_services)

    return jsonify(resp)
  
