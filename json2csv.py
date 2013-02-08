import json

json_file = open('results.json').read()
json = json.loads(json_file)

ihr_file = open('ihr.csv', 'w')
respiration_file = open('respiration.csv', 'w')
presence_file = open('presence.csv', 'w')
binary_actigram_file = open('binary_actigram.csv', 'w')

ihr = 'Timestamp,Instant heart rate value\n'
respiration = 'Timestamp,Channel,Min,Max,Amplitude\n'
presence = 'Timestamp, present\n'
binary_actigram = 'Timestamp\n'

for item in json['ihr']:
	ihr += str(item[0]) + ',' + str(item[1]) + '\n'

for item in json['respiration']:
	respiration += str(item[0]) + ',' + item[1] + ',' + str(item[2]) + ',' + str(item[3]) + ',' + str(item[4]) + '\n'

for item in json['presence']:
	presence += str(item[0]) + ',' + str(item[1]) + '\n'

for item in json['binary_actigram']:
	binary_actigram += str(item) + '\n'

ihr_file.write(ihr)
respiration_file.write(respiration)
presence_file.write(presence)
binary_actigram_file.write(binary_actigram)

ihr_file.close()
respiration_file.close()
presence_file.close()
binary_actigram_file.close()

#print json['presence']
#print json

#print json['respiration']
#print json['ihr']
