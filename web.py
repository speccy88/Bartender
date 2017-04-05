# -*- coding: utf-8 -*-
import tornado.autoreload
import tornado.ioloop
import tornado.web

import sockjs.tornado


class ViewerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('viewer.html')

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin.html')        

class ViewerConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()

    def on_open(self, info):
        # Send that someone joined
        self.broadcast(self.participants, "Someone joined.")

        # Add client to the clients list
        self.participants.add(self)

    def on_message(self, message):
        # Broadcast message
        self.broadcast(self.participants, message)

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)

        self.broadcast(self.participants, "Someone left.")

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create websocket router
    ViewerRouter = sockjs.tornado.SockJSRouter(ViewerConnection, '/viewer')

    # 2. Create Tornado application
    app = tornado.web.Application(
            [(r"/", ViewerHandler), (r"/admin", AdminHandler)] + ViewerRouter.urls
    )

    # 3. Make Tornado app listen on port 8080
    app.listen(8080, "0.0.0.0")

    # 4. Start IOLoop
    print("test")

    tornado.autoreload.start()
    tornado.autoreload.watch('viewer.html')
    tornado.autoreload.watch('base.html')
    tornado.ioloop.IOLoop.instance().start()



"""
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
    print("valve")
    print(request.args["val"])
    return  ""

@app.route("/api/move")
def _move():
    print("move")
    print(request.args["val"])
    return  ""
    
@app.route("/api/test")
def _test():
    data = request.args
    return jsonify(data="success")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
"""