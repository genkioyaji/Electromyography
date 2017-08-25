import pyaudio
import sys
import pylab
import numpy
import time
#import src
import serial
import pylab
import string
import csv
start = time.time()
#----- Gyro inisialize------------------------------
ser = serial.Serial('/dev/cu.usbserial-A104WPYL',115200)
time.sleep(5)

time_dev  = 3

f = open('test.txt','w')
InitiallLoop = 0
DoFunctionFlag = 0

for loop in range(10):
	l = ser.readline()
	line0       = l.decode('utf-8')
	line1       =  line0.strip("^M")

	refer = 'Send'
	if  refer in line0 :
		ser.write(b'2')

	startFlagWrds = 'DMP ready! Waiting for first'
	InitiallLoop = InitiallLoop + 1
#	print(InitiallLoop)
	print(line1)

#startTime = time.time()

#------- End  Gyro inisialize -------------------------

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 6
#WAVE_OUTPUT_FILENAME = "output.wav"
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

print("* recording")
all = []
starttime = time.time()
#for i in range(0, RATE / chunk * RECORD_SECONDS):
for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
#for i in range(0, int(RATE / chunk *30)):
    data = stream.read(chunk)
#	data =data0
    all.append(data)

#	result0 = numpy.frombuffer(data,dtype="int16") / float(2**15)
#	ptint(result0)
#------------ Gyro functin --------------------

    l = ser.readline()
    #print(l)
    line0      = l.decode('utf-8')
    line01     = line0.strip("^M")
    line1      = str(line01[0:])
    line01     = line1.replace("	"," ")
    line02     = line01.split(' ')
#    line02a    = float(line02[3])
#    line2     = "".join(line01)
#    line20    = line2.split(" ")
#    print(line20[1])
#    sys.exit()
    timeNow   = time.time()-starttime
    line02_noCL = float(line02[3].rstrip())
    line02_noCL_math = line02_noCL/2.0

#    line3     = str(timeNow) + " " + str(line2)
#    timeNow0  = timeNow.strip("")
#    line3     = str(line2) + " " +str(timeNow)
#    line3     = str(line02a/10) + " " +str(timeNow)+str('/r/n')
#    line3     = str(line02a/2) + " " +str(timeNow)
#    line3     = str(timeNow) + " " + str(line02a/2)
#    line3     = str(timeNow) + ": " + str(line02) + ":" + str(float(line02[3]))
#    line3     = str(timeNow) + ": " + str(line02[1]) + str(": ")+str(line02[2]) +str(":")+ str(float(line02[3]/2))
    line3     = str(timeNow) + ": " + str(line02[1]) + str(": ")+str(line02[2]) +str(":")+ str(float(line02_noCL_math))+":"+str(line02[3])
    print(line3)

    f.write(line3)
#--------- End Gyro functin
f.close()
print("* done recording")

stream.close()
p.terminate()

# write data to WAVE file
data = b''.join(all)
#data = b''.join(all).decode()
#data = b''.join(all).decode()
#data = b''.join(comments).decode()
#data = "".join([b'www', b'www'])
result = numpy.frombuffer(data,dtype="int16") / float(2**15)
print(result)
pylab.plot(result)
pylab.ylim([-0.05,0.05])
pylab.show()
elapsed_time = time.time() - start
print (("elapsed_time:{0}".format(elapsed_time)) + "[sec]")

outfile = open('fin_ids.csv','w')
out = csv.writer(outfile)
out.writerows(map(lambda x: [x], result))
outfile.close()

#header = ['masclesignal']
#with open('sample.csv', 'w') as f:

# writer = csv.writer(f)
#  writer.writerow(header)
#  writer.writerows(result)



#filename = 'Data.CSV'
#f = open(filename,'w')
#f.write("{},{}\n".format(result))
#f.close()
