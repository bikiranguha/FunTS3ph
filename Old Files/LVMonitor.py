# run all the N-2 contingencies (with faults in between) (except for ones which cause topology issues) and see which ones lead to voltages (in one or more buses)
# less than 0.95 pu for more than 10 cycles

# external stuff
from getBusDataFn import getBusData

# LV report class structure
class LVReport(object):
	def __init__(self):
		self.LVBuses = []
		self.minV = []



# files
raw = 'test_cases/savnw/savnw_sol.raw'
topology_inconsistency_file = 'topology_inconsistency_cases_savnw.txt' # lists all the N-2 contingencies which cause topology inconsistencies

# variables
HVBusSet = set()
HVLineSet = set()
rawBusDataDict = getBusData(raw)
topology_inconsistent_set = set()
LVReportDict = {}
outputLines = []

# constants
LVThreshold = 0.95

# generate the HV bus set
for Bus in rawBusDataDict:
    BusVolt = float(rawBusDataDict[Bus].NominalVolt)
    BusType = rawBusDataDict[Bus].type
    if BusVolt >= 34.5: # no need to consider type 4 buses since they are already filtered out in the get Bus Data function
        HVBusSet.add(Bus)

# read the raw file and get the HV line set
with open(raw,'r') as f:
    fileLines = f.read().split('\n')
branchStartIndex = fileLines.index('0 / END OF GENERATOR DATA, BEGIN BRANCH DATA') + 1
branchEndIndex = fileLines.index('0 / END OF BRANCH DATA, BEGIN TRANSFORMER DATA')


# get the N-2 events which cause topology inconsistencies
with open(topology_inconsistency_file,'r') as f:
    fileLines = f.read().split('\n')
    for line in fileLines:
    	if line == '':
    		continue
    	topology_inconsistent_set.add(line.strip())

# extract all the HV lines
for i in range(branchStartIndex,branchEndIndex):
    line = fileLines[i]
    words = line.split(',')
    Bus1 = words[0].strip()
    Bus2 = words[1].strip()
    cktID = words[2].strip("'").strip()
    status = words[13].strip()
    if Bus1 in HVBusSet and Bus2 in HVBusSet and status != '0':
        key = Bus1 + ',' + Bus2 + ',' + cktID
        HVLineSet.add(key)


# run nested loops to see if there are any abnormal low voltages
for line1 in list(HVLineSet):
    for line2 in list(HVLineSet):
        # part to ensure there is no duplication of events
        currentSet = line1+';'+line2
        currentSetReverse = line2 + ';' + line1
        # if case causes topology inconsistencies, continue
        if currentSet in topology_inconsistent_set or currentSetReverse in topology_inconsistent_set:
        	continue

        # simulation already done
        if currentSet in SimulationDoneSet:
            continue
        else:
            currentSetReverse = line2+';'+line1
            SimulationDoneSet.add(currentSet)
            SimulationDoneSet.add(currentSetReverse)

        # event key
        #key = line1 + ';' + line2

        line1Elements = line1.split(',')
        line2Elements = line2.split(',')

        # Line 1 params
        L1Bus1 = line1Elements[0]
        L1Bus2 = line1Elements[1]
        L1cktID = line1Elements[2]

        # Line 2 params
        L2Bus1 = line2Elements[0]
        L2Bus2 = line2Elements[1]
        L2cktID = line2Elements[2]

        # generate the event
		# one line out then a fault
		event1Flag = '-event01'
		event1Param = '0.1,OUT,LINE,'+ L1Bus1 +  ',' + L1Bus2 + ',,' + L1cktID + ',7,,,,,'

		event2Flag = '-event02'
		event2Param = '0.2,FAULTON,ABCG,'+ L2Bus1 + ',,,,1.0e-6,1.0e-6,1.0e-6,0.0,0.0,0.0'

		event3Flag = '-event03'
		event3Param = '0.3,FAULTOFF,ABCG,' + L2Bus1 + '151,,,,,,,,,'

		event4Flag = '-event04'
		event4Param = '0.31,OUT,LINE,'+ L2Bus1 + ',' + L2Bus2 +  ',,'+ L2cktID +',7,,,,,'

		exitFlag = '-event05'
		exitParam = '3,EXIT,,,,,,,,,,,'
		EventList = [event1Flag,event1Param,event2Flag,event2Param,event3Flag,event3Param,event4Flag,event4Param,exitFlag,exitParam]
		Results = runSim(raw,EventList,'TS3phEvent.log')

		# extract LV results if any
		for key in Results:
			if key == 'time':
				continue

			Vmag = list(Results[key].mag)
			LValues = [v for v in Vmag if v < 0.95] # will contain all the LV values in the bus
			if len(LValues) >= 10:
				minV = min(Vmag)
				LVReportDict[currentSet] = LVReport()
				LVReportDict[currentSet].LVBuses.append(key) # get the bus
				LVReportDict[currentSet].minV.append(minV) # get the minimum voltage recorded for that bus


# generate output lines
for event in LVReportDict:
	LVBusList = LVReportDict[event].LVBuses
	minVList = LVReportDict[event].minV
	for i in range(LVBusList):
		Bus = str(LVBusList[i])
		minV = str(minVList[i])
		outputString = event.rjust(25) + ',' + Bus.rjust(6) + ',' + minV.rjust(10)
		outputLines.append(outputString)
				

# write to output file
with open('VoltageReport.txt','w') as f:
	for line in outputLines:
		f.write(line)
		f.write('\n')

			

     
