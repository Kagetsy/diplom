import time
from urllib.request import urlopen # comment this line if you don't need ThinkSpeak connection
from urllib.request import HTTPError
import SDL_Pi_HDC1000 # comment this line if you don't use HDC sensor

from application.modules.sensors.CO2.CCS811_RPi import CCS811_RPi

class CCS811:

	def __init__(self):
		self.ccs811 = CCS811_RPi()

		# Do you want to send data to thingSpeak? If yes set WRITE API KEY, otherwise set False
		self.THINGSPEAK      = False # or type 'YOURAPIKEY'

		# Do you want to preset sensor baseline? If yes set the value here, otherwise set False
		self.INITIALBASELINE = False

		# Do you want to use integrated temperature meter to compensate temp/RH (CJMCU-8118 board)?
		# If not pre-set sensor compensation temperature is 25 C and RH is 50 %
		# You can compensate manually by method ccs811.setCompensation(temperature,humidity) 
		self.HDC1080         = False

		'''
		MEAS MODE REGISTER AND DRIVE MODE CONFIGURATION
		0b0       Idle (Measurements are disabled in this mode)
		0b10000   Constant power mode, IAQ measurement every second
		0b100000  Pulse heating mode IAQ measurement every 10 seconds
		0b110000  Low power pulse heating mode IAQ measurement every 60
		0b1000000 Constant power mode, sensor measurement every 250ms
		'''
		# Set MEAS_MODE (measurement interval)
		self.configuration = 0b100000

		# Set read interval for retriveving last measurement data from the sensor
		self.pause = 60

	def thingSpeak(self, eCO2,TVOC,baseline,temperature,humidity):
		print('Sending to ThingSpeak API...')
		url = "https://api.thingspeak.com/update?api_key="
		url += self.THINGSPEAK
		url += "&field1="
		url += str(eCO2)
		url += "&field2="
		url += str(TVOC)
		url += "&field3="
		url += str(baseline)
		url += "&field4="
		url += str(temperature)
		url += "&field5="
		url += str(humidity)
    #print url
		try: 
			self.content = urlopen(url).read()
		except HTTPError:
			print("Invalid HTTP response")
			return False
		print('Done')
		#print content



	print('Checking hardware ID...')
	hwid = self.ccs811.checkHWID()
	if(hwid == hex(129)):
			print('Hardware ID is correct')
	else: print('Incorrect hardware ID ',hwid, ', should be 0x81')




	#print 'MEAS_MODE:',ccs811.readMeasMode()
	self.ccs811.configureSensor(configuration)
	print('MEAS_MODE:',self.ccs811.readMeasMode())
	print('STATUS: ',bin(self.ccs811.readStatus()))
	print('---------------------------------')

	# Use these lines if you need to pre-set and check sensor baseline value
	if(self.INITIALBASELINE > 0):
			self.ccs811.setBaseline(self.INITIALBASELINE)
			print(self.ccs811.readBaseline())


	# Use these lines if you use CJMCU-8118 which has HDC1080 temp/RH sensor
	if(HDC1080):
			hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()
			hdc1000.turnHeaterOff()
			hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
			hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)


	while(1):
			if(HDC1080):
					humidity = hdc1000.readHumidity()
					temperature = hdc1000.readTemperature()
					ccs811.setCompensation(temperature,humidity)
			else:
					humidity = 50.00
					temperature = 25.00
        
			statusbyte = ccs811.readStatus()
			print('STATUS: ', bin(statusbyte))

			error = ccs811.checkError(statusbyte)
			if(error):
					print('ERROR:',ccs811.checkError(statusbyte))
                
			if(not ccs811.checkDataReady(statusbyte)):
				print('No new samples are ready')
				print('---------------------------------')
				time.sleep(pause)
				continue
			result = ccs811.readAlg()
			if(not result):
				#print 'Invalid result received'
				time.sleep(pause)
				continue
			baseline = ccs811.readBaseline()
			print('eCO2: ',result['eCO2'],' ppm')
			print('TVOC: ',result['TVOC'], 'ppb')
			print('Status register: ',bin(result['status']))
			print('Last error ID: ',result['errorid'])
			print('RAW data: ',result['raw'])
			print('Baseline: ',baseline)
			print('---------------------------------')

			if (self.THINGSPEAK is not False):
					self.thingSpeak(result['eCO2'],result['TVOC'],baseline,temperature,humidity)
			time.sleep(self.pause)



