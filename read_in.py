
#reading weirde dateiformate clusters?.txt
#Idee:
#zeile für zeile durchgehen
#wenn TriggerID: mache neuen Dump auf
#sammle bei nachfolgenden Zeilen den Dump auf
#wenn erneut TriggerID: 
# Dump speichern und wiederholen



def read_from_raw_data(filename):
    import numpy as np

    #reads from clusters1 file
    #input: string: filename
    #output: int: number of empty_events, number
    out_events = []
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    dump = []
    for line in Lines:
        if "TriggerId" in line:
            out_events.append(dump)
            dump=[]
        else:
            line = line[:-1] #remove \n
            line = line.split(',') #makes list with numbers
            if line[1] == 'bottom':
                line[1] = 0
            elif line[1] == 'top':
                line[1] = 1
            else:
                raise ValueError('Problem with file format')
            line = [int(line[i]) if i !=2 else float(line[i]) for i in range(len(line))]
            dump.append(line)
    return out_events

def filter_array(out_events):
    filtered_events = []
    empty_events = 0
    event_counter = 0
    for event in out_events:
        if event == []:
            empty_events+=1
        else:
            filtered_events.append(event)
            event_counter+=1


    return empty_events,event_counter, filtered_events

print(filter_array(read_from_raw_data('clusters1.txt'))[0:3])

