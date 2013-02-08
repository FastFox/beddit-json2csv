import json

json_file = open('results.json').read()
json = json.loads(json_file)

ihr_file = open('ihr.csv', 'w')
respiration_file = open('respiration.csv', 'w')
ihr = 'Timestamp,Instant heart rate value\n'
respiration = 'Timestamp,Channel,Min,Max,Amplitude\n'

for item in json['ihr']:
	ihr += str(item[0]) + ',' + str(item[1]) + '\n'

for item in json['respiration']:
	respiration += str(item[0]) + ',' + item[1] + ',' + str(item[2]) + ',' + str(item[3]) + ',' + str(item[4]) + '\n'

ihr_file.write(ihr)
respiration_file.write(respiration)

ihr_file.close()
respiration_file.close()

#print json['presence']
#print json

#print json['respiration']
#print json['ihr']
