# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from SAQ import Bottle
import subprocess
import os

app = Flask(__name__)

code_list = ["00255091",
             "00012195",
             "00005215",
             "00268714",
             "00323972",
             "00117101",
             "00195370",
             "10757154"]

@app.route("/")
def Index():
    pass
    return render_template("index.html")

@app.route("/list")
def List():
    bottles = []
    for code in code_list:
        bottles.append(Bottle(code))
    return render_template("list.html", bottles=bottles)    

@app.route("/api/valve")
def _valve():
    print "valve"
    print request.args["val"]
    return  ""

@app.route("/api/move")
def _move():
    print "move"
    print request.args["val"]
    return  ""
    
@app.route("/api/test")
def _test():
    data = request.args
    return jsonify(data="success")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
