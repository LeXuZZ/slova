import os
import random
import tornado.web
import tornado.ioloop
import tornado.websocket
from one_more_algorithm import OMA

global grid

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ws_html.html")


# def generate_field(ws):
#     for num in xrange(10):
#         time.sleep(1)
#         ws.write_message(message={"letter": str(num)})

def _generate_field(ws):
    oma = OMA()
    oma.ggenerate_field()
    oma.print_grid_to_console()
    ws.write_message(message=oma.grid.to_dict())

class Websocket(tornado.websocket.WebSocketHandler):
    users = {}

    def open(self):
        _generate_field(self)
        # uid = self.get_cookie("uid")
        # if uid is None:
        #     uid = str(random.randint(0, 100000))
        #     self.write_message("uid:" + uid)
        # print("WebSocket opened for " + uid)
        # Websocket.users[uid] = self

    def on_message(self, message):
        print(message)
        self.write_message("server: " + message)

    def on_close(self):
        for uid, user in Websocket.users.iteritems():
            if user == self:
                del Websocket.users[uid]
            print("WebSocket closed for " + uid)
            return


application = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r"/ws", Websocket),
    ],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
)

__author__ = 'lxz'
if __name__ == '__main__':
    application.listen(8888)
    print '* app started on http://127.0.0.1:8888'
    tornado.ioloop.IOLoop.instance().start()