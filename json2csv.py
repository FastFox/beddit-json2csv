import sys, getopt, json, urllib2, datetime
import settings
from operator import itemgetter, attrgetter

#ACCESS_TOKEN = 'becHtgs9r7sw81gr04htyvkU' 

class Beddit:
	# result.json from 5.7
	def results(self):
		print 'Results'

		# Open input file
		json_file = open('results.json').read()
		json_obj = json.loads(json_file)

		# Make the output files writable
		ihr_file = open('ihr.csv', 'w')
		respiration_file = open('respiration.csv', 'w')
		presence_file = open('presence.csv', 'w')
		binary_actigram_file = open('binary_actigram.csv', 'w')

		# Column names
		ihr = 'Timestamp,Datetime,Instant heart rate value\n'
		respiration = 'Timestamp,Datetime,Channel,Min,Max,Amplitude\n'
		presence = 'Timestamp,Datetime,present\n'
		binary_actigram = 'Timestamp\n'

		interval_start = datetime.datetime.strptime( json_obj['interval_start'], "%Y-%m-%dT%H:%M:%S" )

		# Loop for every value for every attribute
		print 'ihr'
		for item in json_obj['ihr']:
			ihr += str(item[0]) + ',' + str(interval_start + datetime.timedelta(0, item[0])) + ',' + str(item[1]) + '\n'

		print 'respiration'
		for item in json_obj['respiration']:
			respiration += str(item[0]) + ',' + str(interval_start + datetime.timedelta(0, item[0])) + ',' + item[1] + ',' + str(item[2]) + ',' + str(item[3]) + ',' + str(item[4]) + '\n'

		print 'presence'
		for item in json_obj['presence']:
			presence += str(item[0]) + ',' + str(interval_start + datetime.timedelta(0, item[0])) + ',' + str(item[1]) + '\n'

		print 'binary_actigram'
		for value in json_obj['binary_actigram']:
			binary_actigram += str(value) + ',' + str(interval_start + datetime.timedelta(0, item[0])) + '\n'

		# Write the files
		ihr_file.write(ihr)
		respiration_file.write(respiration)
		presence_file.write(presence)
		binary_actigram_file.write(binary_actigram)

		# Close the files
		ihr_file.close()
		respiration_file.close()
		presence_file.close()
		binary_actigram_file.close()

	def download_results(self):
		print 'Download results'
		download = urllib2.urlopen('https://api.beddit.com/api2/user/liacs2/2013/01/26/results?access_token=' + settings.ACCESS_TOKEN)
		file = open('results.json', 'w')
		file.write(results_download.read())
		file.close()

	# sleep.json from 5.5
	def sleep(self):
		print 'Sleep'
		
		json_file = open('sleep.json').read()
		json_obj = json.loads(json_file)
	
		actigram_file = open('minutely_actigram.csv', 'w')
		noise_file = open('noise.csv', 'w')
		luminosity_file = open('luminosity.csv', 'w')
		stages_file = open('stages.csv', 'w')

		actigram = 'Datetime,Minutely actigram\n'
		noise = 'Datetime,dB\n'
		luminosity = 'Datetime,Lux\n'
		stages = 'Datetime,Stage\n'

		interval_start = datetime.datetime.strptime( json_obj['local_start_time'], "%Y-%m-%dT%H:%M:%S" )

		print 'Minutely actigram'
		for index, value in enumerate(json_obj['minutely_actigram']):
			actigram += str(interval_start + datetime.timedelta(0, index * 60)) +',' + str(value) + '\n'


		print 'Noise'
		for item in json_obj['noise_measurements'][0]:
			noise += str(item[0]) + ',' + str(item[1]) + '\n'

		print 'Luminosity'
		for item in json_obj['luminosity_measurements'][0]:
			luminosity += str(item[0]) + ',' + str(item[1]) + '\n'

		print 'Stages'
		for item in json_obj['sleep_stages']:
			stages += str(item[0]) + ','
			if item[1] == 'M':
				stages += '0'
			elif item[1] == 'A':
				stages += '1'
			elif item[1] == 'W':
				stages += '2'
			elif item[1] == 'L':
				stages += '3'
			elif item[1] == 'D':
				stages += '4'

			stages += '\n'

		actigram_file.write(actigram)
		noise_file.write(noise)
		luminosity_file.write(luminosity)
		stages_file.write(stages)

		actigram_file.close()
		noise_file.close()
		luminosity_file.close()
		stages_file.close()

	def download_sleep(self):
		print 'Download sleep'
		download = urllib2.urlopen('https://api.beddit.com/api2/user/liacs2/2013/01/26/sleep?access_token=' + settings.ACCESS_TOKEN)
		file = open('sleep.json', 'w')
		file.write(sleep_download.read())
		file.close()

	# signal.bson from 5.9
	def signal(self):
		print 'Signal'
		"""
		import bson, numpy
		data = bson.loads(bson_data)
		channel_1 = numpy.fromstring(data["channels"]["lo_gain"]["sample_data"], numpy.int16)
		channel_1
		"""

	def download_signal(self):
		print 'Download Signal'
		download = urllib2.urlopen('https://api.beddit.com/api2/user/liacs2/2013/01/26/signal.bson?access_token=' + settings.ACCESS_TOKEN)
		file = open('signal.bson', 'w')
		file.write(sleep_download.read())
		file.close()

	def timeline(self):
		print 'Timeline'
		json_file = open('timeline.json').read()
		json_obj = json.loads(json_file)
		json_obj = sorted(json_obj, key=itemgetter('date'))

		timeline = "Date,Time in bed,Time sleeping,Time light sleep,Time deep sleep,resting heartrate,sleep_efficiency\n"

		for day in json_obj:
			timeline += str(day["date"]) + "," + str(day["time_in_bed"]) + "," + str(day["time_sleeping"]) + "," + str(day["time_light_sleep"]) + "," + str(day["time_deep_sleep"]) + "," + str(day["resting_heartrate"]) + "," + str(day["sleep_efficiency"]) + "\n"

		file = open('timeline.csv', 'w')
		file.write(timeline)
		file.close()

	def download_timeline(self):
		print 'Download timeline'
		download = urllib2.urlopen('https://api.beddit.com/api2/user/liacs2/timeline?start=2013-01-19&end=2013-01-27&access_token=' + settings.ACCESS_TOKEN)
		file = open('timeline.json', 'w')
		file.write(download.read())
		file.close()

def main():
	B = Beddit()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "rsgtd", ["results", "sleep", "signal", "timeline", "download"])
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	
	results = False
	sleep = False
	signal = False
	timeline = False
	download = False

	for o, a in opts:
		if o == "-d":
			download = True
		if o == "-r":
			results = True
		if o == "-s":
			sleep = True
		if o == "-g":
			signal = True
		if o == "-t":
			timeline = True

	if results:
		if download:
			B.download_results()
		B.results()
	
	if sleep:
		if download:
			B.download_sleep()
		B.sleep()

	if signal:
		if download:
			B.download_signal()
		B.signal()

	if timeline:
		if download:
			B.download_timeline()
		B.timeline()

if __name__ == "__main__":
	main()
