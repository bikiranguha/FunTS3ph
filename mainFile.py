import matplotlib.pyplot as plt

from batch_get_v_fault import SimResults as Results_Fault
from batch_get_v_nodist import SimResults as Results_NoDist


# plot to see if everything is ok
time = Results_Fault['time']
vMag = Results_Fault[153].mag
plt.plot(time, vMag)
plt.title('Bus 153')
plt.ylabel('Voltage magnitude (pu)')
plt.ticklabel_format(useOffset=False)
plt.xlabel('Time (sec)')
plt.ylim(-0.1,1.5)
plt.savefig('Bus153VMag.png')

time = Results_Fault['time']
DiffInstant ={}
# get the exact time when the results are different
for key in Results_NoDist:
	if key == 'time':
		continue
	Vmag1 = Results_NoDist[key].mag
	Vmag2 = Results_Fault[key].mag
#	print type(Vmag1)
#	print Vmag1.size
#	print Vmag2.size
	i = 0
	while i < Vmag1.size:
		currentVmag1 = Vmag1[i]
		currentVmag2 = Vmag2[i]
		error = abs((currentVmag2 - currentVmag1)/currentVmag2)*100

		if error > 5: # sudden difference detected
			diffStartTime = i
			diffTime = time[i]
			totDiff = 0.0
			for j in range(diffStartTime,diffStartTime+11): # scan the next 10 steps for errors
				currentVmag1 = Vmag1[j]
				currentVmag2 = Vmag2[j]
				error = abs((currentVmag2 - currentVmag1)/currentVmag2)*100
				totDiff += error
			avgError = totDiff/10
			print avgError
			if avgError > 5: # average error more than 5% in the next ten time steps
				DiffInstant[key] = diffTime
				break
			else: # differene was not sustained, skip ahead next 10 time steps and continue analysis
				i+=10
		else:  # error < 5%
			i+=1




for Bus in DiffInstant:
	print str(Bus) + ': ' + str(DiffInstant[Bus]) + 's'




