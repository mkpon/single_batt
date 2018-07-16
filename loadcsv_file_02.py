#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python

import datetime
import rrdtool
import sys

battery_data_filename = sys.argv[1]
battery_data_file = open(battery_data_filename, "r")

column_names = battery_data_file.readline()
column_names_list = column_names.split(',')
for i, name in enumerate(column_names_list):
	print(f'index: {i}, column_name: {name}')


def convert_to_epoch_time_int(time_str):
	time_str_fixed = time_str.split('.')[0]
	epoch_datetime = datetime.datetime.strptime(time_str_fixed,'%Y/%m/%d %H:%M:%S')
	return int(epoch_datetime.timestamp())


# skip the blank line
battery_data_file.readline()

# get the first data record
one_record = battery_data_file.readline()
first_record_list = one_record.split(',')
time_str = first_record_list[0]
first_timestamp = convert_to_epoch_time_int(time_str)
print('first_timestamp:%d' % first_timestamp)

# create rrd files
rrd_filesetups = [None]*len(column_names_list)
rrd_filesetups[43] = ('i43_pos_to_gnd_ohms', 'DS:Ohms:GAUGE:300:0:5000', 'RRA:AVERAGE:0.5:1:864000')
rrd_filesetups[44] = ('i44_neg_to_gnd_ohms', 'DS:Ohms:GAUGE:300:0:5000', 'RRA:AVERAGE:0.5:1:864000')
for i in range(100,131):
	rrd_filesetups[i] = ('i%d_cell_%d_volts'%(i,(i-99)), 'DS:Volts:GAUGE:300:0:5', 'RRA:AVERAGE:0.5:1:864000')

for filesetup in rrd_filesetups:
	if filesetup:
		rrdtool.create('%s.rrd' % filesetup[0], '--start', '%d' % (first_timestamp-10), filesetup[1], filesetup[2])
		print('created rrd file: %s.rrd' % filesetup[0])

while one_record:
	record_list = one_record.split(',')
	time_str = record_list[0]
	timestamp = convert_to_epoch_time_int(time_str)
	for i, filesetup in enumerate(rrd_filesetups):
		if filesetup:
			rrd_filename = '%s.rrd' % filesetup[0]
			rrdtool.update(rrd_filename, '%d:%s' % (timestamp,record_list[i]))
#			print('time_str: %s, i: %d, value: %s' %(time_str, i, record_list[i]))
	one_record = battery_data_file.readline()

last_timestamp = timestamp
print('last_timestamp:%d' % last_timestamp)

for filesetup in rrd_filesetups:
	if filesetup:
		png_filename = '%s.png' % filesetup[0]
		units = filesetup[1].split(':')[1]
		stream_name = 'my%s' % units
		theDEF = 'DEF:%s=%s.rrd:%s:AVERAGE' % (stream_name,filesetup[0],units)
		theLINE = 'LINE2:%s#FF0000' % stream_name
		rrdtool.graph(png_filename, '--start', '%d' % first_timestamp, '--end', '%d' % last_timestamp, theDEF, theLINE)