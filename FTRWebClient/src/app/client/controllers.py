# -*- coding : utf-8 -*-
from app import db, render_template, send_from_directory
from flask import Response, jsonify, request,Blueprint,flash,redirect
from app.client.views import KAFKA_PRODUCER

client = Blueprint('client', __name__, url_prefix='/client')

client.add_url_rule('/kaf_prod',view_func=KAFKA_PRODUCER().as_view('kaf_prod'))
