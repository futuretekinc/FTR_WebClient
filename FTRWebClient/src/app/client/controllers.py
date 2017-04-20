# -*- coding : utf-8 -*-
from app import db, render_template, send_from_directory
from flask import Response, jsonify, request,Blueprint,flash,redirect
from app.client.views import KAFKA_PRODUCER,KAFKA_CONSUMER

client = Blueprint('client', __name__, url_prefix='/client')

client.add_url_rule('/kaf_prod',view_func=KAFKA_PRODUCER().as_view('kaf_prod'))
client.add_url_rule('/kaf_poll',view_func=KAFKA_CONSUMER().as_view('kaf_poll'))
