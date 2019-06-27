from aiohttp import web
from application.modules.db.DB import DB
from application.modules.mediator.Mediator import Mediator
from application.modules.userManager.UserManager import UserManager
from application.modules.sensors.SensorManager import SensorManager
from application.router.Router import Router
from settings import SETTINGS

db = DB(SETTINGS['DB'])
mediator = Mediator(SETTINGS['TYPES'])
UserManager(db, mediator)
SensorManager(db, mediator)

app = web.Application()

Router(app, web, mediator)

web.run_app(app)