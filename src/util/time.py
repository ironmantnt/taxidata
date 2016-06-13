'''
Transfer time stamp to neural network input
	@bolan on 13rd, June
	'''

def time_transfer(time):
	hour, minute = time[:2], time[2:4]
	return round(int(hour) + float(minute) / 60, 2)

if __name__ == '__main__':
	a = '010203'
	b = '093012'
	c = '134520'

	time = [a,b,c]
	print map(time_transfer, time)
