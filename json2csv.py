import sys, getopt, json, urllib2, datetime
import settings
from operator import itemgetter, attrgetter

#ACCESS_TOKEN = 'becHtgs9r7sw81gr04htyvkU' 

class Beddit():
	# result.json from 5.7
	class Help():
			def avgResp(self):
				print 'avg resp'
				file = open('results.json').read()
				obj = json.loads(file)
				respAmpCount = 0
				respAmp = 0
				
				ihrCount = 0
				ihr = 0

				for item in obj['respiration']:
					respAmp += item[4];
					respAmpCount += 1

				for item in obj['ihr']:
					ihr += item[1]
					ihrCount += 1


				#print count, total
				print obj
				return respAmp / count

	def __init__(self):
		self.Help = self.Help()
	
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
		date = '2013/01/26'

		download = urllib2.urlopen('https://api.beddit.com/api2/user/' + settings.USERNAME + '/' + date + '/results?access_token=' + settings.ACCESS_TOKEN)
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
			else:
				stages += '-1'

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
		date = '2013/01/06'

		print 'Download sleep'
		download = urllib2.urlopen('https://api.beddit.com/api2/user/' + settings.USERNAME + '/' + date + '/sleep?access_token=' + settings.ACCESS_TOKEN)
		file = open('sleep.json', 'w')
		file.write(sleep_download.read())
		file.close()

	def extend_timeline(self):
		print 'Extend timeline'
		with open('timeline.csv', 'r') as file:
			data = file.readlines()
			
		data[0] = data[0][0:-2] + ',average respiration amplitude\n'
		#length = len(data) - 1
		print	self.Help.avgResp()
		with open('timeline_extended.csv', 'w') as file:
			file.writelines(data)


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
		download = urllib2.urlopen('https://api.beddit.com/api2/user/' + settings.USERNAME + '/2013/01/26/signal.bson?access_token=' + settings.ACCESS_TOKEN)
		file = open('signal.bson', 'w')
		file.write(sleep_download.read())
		file.close()

	# Timeline from 5.4
	def timeline(self):
		print 'Timeline'

		start = "2013-01-19"
		end = "2013-01-27"

		json_file = open('timeline.json').read()
		json_obj = json.loads(json_file)
		json_obj = sorted(json_obj, key=itemgetter('date'))

		timeline = "Date,Time in bed,Time sleeping,Time light sleep,Time deep sleep,Resting heartrate,Sleep efficiency,Stress\n"

		for day in json_obj:
			timeline += str(day["date"]) + "," + str(day["time_in_bed"]) + "," + str(day["time_sleeping"]) + "," + str(day["time_light_sleep"]) + "," + str(day["time_deep_sleep"]) + "," + str(day["resting_heartrate"]) + "," + str(day["sleep_efficiency"]) + "," + str(day["stress_percent"]) + "\n"

		file = open('timeline.csv', 'w')
		file.write(timeline)
		file.close()

	def download_timeline(self):
		print 'Download timeline'
		download = urllib2.urlopen('https://api.beddit.com/api2/user/' + settings.USERNAME + '/timeline?start=' + start + '&end=' + end + '&access_token=' + settings.ACCESS_TOKEN)
		file = open('timeline.json', 'w')
		file.write(download.read())
		file.close()


def main():
	B = Beddit()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "rsgted", ["results", "sleep", "signal", "timeline", "download", "extend"])
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	
	results = False
	sleep = False
	signal = False
	timeline = False
	extend = False
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
		if o == "-e":
			extend = True

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

	if extend:
		B.extend_timeline()

if __name__ == "__main__":
	main()
