'''
Transfer time stamp to neural network input
	@bolan on 13rd, June
'''

def time_transfer(time):
	hour, minute = time[:2], time[2:4]
	minute = round(float(minute) / 60, 1)
	if 0 <= minute < 0.2:
		minute = 0.0
	elif 0.2 <= minute < 0.4:
		minute = 0.2
	elif 0.4 <= minute < 0.6:
		minute = 0.4
	elif 0.6 <= minute < 0.8:
		minute = 0.6
	else:
		minute = 0.8
	return int(hour) + minute

if __name__ == '__main__':
	a = '010203'
	b = '093012'
	c = '134520'

	time = [a,b,c]
	print map(time_transfer, time)
