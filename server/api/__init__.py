from bottle import Bottle, TEMPLATE_PATH

app = Bottle()
TEMPLATE_PATH.append("./api/views/")
TEMPLATE_PATH.remove("./views/")


from api.controllers import *
