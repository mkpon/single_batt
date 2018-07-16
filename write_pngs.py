#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python

import datetime
import rrdtool
import sys

start_time_str = sys.argv[1]
end_time_str = sys.argv[2]

def convert_to_epoch_time_int(time_str):
	time_str_fixed = time_str.split('.')[0]
	epoch_datetime = datetime.datetime.strptime(time_str_fixed,'%Y/%m/%d %H:%M:%S')
	return int(epoch_datetime.timestamp())

# create rrd files
rrd_filesetups = [None]*140
rrd_filesetups[43] = ('i43_pos_to_gnd_ohms', 'DS:Ohms:GAUGE:300:0:5000', 'RRA:AVERAGE:0.5:1:864000')
rrd_filesetups[44] = ('i44_neg_to_gnd_ohms', 'DS:Ohms:GAUGE:300:0:5000', 'RRA:AVERAGE:0.5:1:864000')
for i in range(100,131):
	rrd_filesetups[i] = ('i%d_cell_%d_volts'%(i,(i-99)), 'DS:Volts:GAUGE:300:0:5', 'RRA:AVERAGE:0.5:1:864000')

epoch_start_time = convert_to_epoch_time_int(start_time_str)
epoch_end_time = convert_to_epoch_time_int(end_time_str)

rrd_path = '/Users/mpon/Downloads/job_search_2018/Mercedes/'
png_path = '/Users/mpon/Downloads/job_search_2018/Mercedes/one_ev/one_ev/png_viewer/static/png_viewer/'

for filesetup in rrd_filesetups:
	if filesetup:
		png_filename = '%s%s.png' % (png_path,filesetup[0])
		units = filesetup[1].split(':')[1]
		stream_name = 'my%s' % units
		theDEF = 'DEF:%s=%s.rrd:%s:AVERAGE' % (stream_name,filesetup[0],units)
		theLINE = 'LINE2:%s#FF0000' % stream_name
		rrdtool.graph(png_filename, '--start', '%d' % epoch_start_time, '--end', '%d' % epoch_end_time, theDEF, theLINE)