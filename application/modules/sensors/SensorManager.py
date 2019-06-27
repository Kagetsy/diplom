#from application.modules.sensors.CO.ccs811 import CCS811

class SensorManager:

    def __init__(self, db, mediator):
        self.db = db
        self.mediator = mediator

        #self.ccs811 = CCS811()
    