# provide an event
# plot all HV bus voltages in TS3ph

import platform
currentOS = platform.system()
from runSimFn import runSim
from getBusDataFn import getBusData
import numpy as np
import matplotlib.pyplot as plt
HVBusSet = set()

# Functions and classes
def convertFileLinux(file,currentOS):
	# function to convert file from crlf to lf (if needed)
	if currentOS == 'Linux':
		text = open(file, 'rb').read().replace('\r\n', '\n')
		open(file, 'wb').write(text)


rawPath = 'test_cases/savnw/savnw_sol.raw'



# convert raw file crlf to lf (needed for linux)
convertFileLinux(rawPath,currentOS)
rawBusDataDict = getBusData(rawPath)
# generate the HV bus set
for Bus in rawBusDataDict:
	BusVolt = float(rawBusDataDict[Bus].NominalVolt)
	BusType = rawBusDataDict[Bus].type
	if BusVolt >= 34.5: # no need to consider type 4 buses since they are already filtered out in the get Bus Data function
		HVBusSet.add(Bus)

# specify the event

"""
# N-2 line outage contingency
event1Flag = '-event01'
event1Param = '0.1,OUT,LINE,151,152,,1,7,,,,,'

event2Flag = '-event02'
event2Param = '0.1,OUT,LINE,151,152,,2,7,,,,,'
"""

# load shed
event1Flag = '-event01'
event1Param = '0.1,OUT,LOAD,205,,,1,7,,,,,'


exitFlag = '-event02'
exitParam = '0.2,EXIT,,,,,,,,,,,'

#EventList = [event1Flag,event1Param,event2Flag,event2Param,exitFlag,exitParam]
EventList = [event1Flag,event1Param,exitFlag,exitParam]
Results = runSim(rawPath,EventList,'TS3phLoadOut.log')


# get plots for all the buses in the HV set
# plot to see if everything is ok
for Bus in list(HVBusSet):

	time = Results['time']
	vMag = Results[int(Bus)].mag
	plt.plot(time, vMag)
	titleStr = 'Bus ' + Bus
	plt.title(titleStr)
	plt.ylabel('Voltage magnitude (pu)')
	plt.ticklabel_format(useOffset=False)
	plt.xlabel('Time (sec)')
	plt.ylim(-0.1,1.5)
	figName = 'Bus'+ Bus+'VMag.png'
	plt.savefig(figName)
	plt.close()