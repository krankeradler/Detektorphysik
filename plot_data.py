import numpy as np
import read_in
import matplotlib.pyplot as plt
from tqdm import tqdm

list_with_distances = [0, 0.18, 2.8, 3.2, 5.7, 6.1]
color_for_y_position = ['green','red']

empty_events, events_number, event_list = read_in.filter_array(read_in.read_from_raw_data('clusters1.txt'))
print(f"There are {empty_events} Empty Events and {events_number} recorded events. \n \t ==> {100*events_number/(events_number+empty_events)}% hits")


def transform_to_position(module_number,bottom_top_position):
    import math
#    print(module_number,int(module_number/2)+bottom_top_position)
    z_position = (math.ceil((1+module_number)/2)-1)*2+bottom_top_position
    #print(module_number,z_position)
    y_position = module_number%2
    return z_position,y_position


def resort(event_list):
    event_new=[]
    for event in event_list:
        event = np.array(event)
        z_pos_list = []
        for cluster in event:
            z_pos,y_pos = transform_to_position(cluster[0],cluster[1])
            z_pos_list.append(z_pos)
        
        event_new.append(np.array(event)[np.argsort(z_pos_list)])
    return event_new

def resort_and_stuff(event_list):
    event_new=[]
    for event in event_list:
        #event = np.array(event)
        z_pos_list = []
        new_single_event=[]
        for cluster in event:
            z_pos,y_pos = transform_to_position(cluster[0],cluster[1])
            z_pos_list.append(z_pos)
            cluster.append(z_pos)
            cluster.append(y_pos)
            new_single_event.append(cluster)
        event_new.append(np.array(new_single_event)[np.argsort(np.array(z_pos_list))])
    return event_new #a list of 2d np arrays



def easy_plotter(data,step=40):
    #plots stuff
    plt.hlines(list_with_distances,0,1024,color='black')

    for event in tqdm(data[::step]):
        x_vals,y_vals,z_vals = list_to_line(event)
        plt.scatter(x_vals,z_vals,marker='+',color=y_vals)
        plt.plot(x_vals,z_vals)
    plt.show()




def list_to_line(event):
    #generates a line for each event
    #uses 
    x_vals,y_vals,z_vals = [],[],[]
    for cluster in event:
        x_vals.append(cluster[2])
        z_position,y_position = transform_to_position(cluster[0],cluster[1]) #könnte man auch vereinfachen
        y_vals.append(color_for_y_position[y_position])
        z_vals.append(list_with_distances[z_position])

    return x_vals,y_vals,z_vals



def statistics(event_list):
    number_of_clusters = []
    y_position = []
    number_of_clusters_in_same_sensor = []
    number_of_clusters_in_same_level = []
    strip_number = []
    unique_strip_number = []
    cluster_thickness = []
    unique_sensor_number = []
    level_num = []

    

    for event in tqdm(event_list):
        number_of_clusters.append(len(event))
        level_list_per_event = []
        unique_sensor_number_per_event=[]
        for cluster in event:
            z_pos,y_pos = transform_to_position(cluster[0],cluster[1])
            unique_sensor_number.append(z_pos+6*y_pos)
            unique_sensor_number_per_event.append(z_pos+6*y_pos)
            y_position.append(y_pos)
            level_list_per_event.append(z_pos)
            level_num.append(z_pos)
            strip_number.append(cluster[2])
            unique_strip_number.append(cluster[2]+cluster[0]*1040+cluster[1]*8000)
            cluster_thickness.append(cluster[3])
        number_of_clusters_in_same_level.append(len(level_list_per_event)-len(list(set(level_list_per_event))))
        number_of_clusters_in_same_sensor.append(len(unique_sensor_number_per_event)-len(list(set(unique_sensor_number_per_event))))

        

    return number_of_clusters,y_position,level_num,strip_number,unique_strip_number,unique_sensor_number,number_of_clusters_in_same_level,number_of_clusters_in_same_sensor,cluster_thickness

def my_filter(event_list):
    new_list = []
    save_event = True
    for event in event_list:
        unique_sensor_number_per_event=[]
        level_list_per_event=[]
        for cluster in event:
            if cluster[2] ==0 or cluster[2]==1015:
                save_event = False
                break


            z_pos,y_pos = transform_to_position(cluster[0],cluster[1])
            unique_sensor_number_per_event.append(z_pos+6*y_pos)
            level_list_per_event.append(z_pos)

        if (len(unique_sensor_number_per_event)-len(list(set(unique_sensor_number_per_event))))!=0:
            save_event=False
        if (len(level_list_per_event)-len(list(set(level_list_per_event))))!=0:
            save_event=False
        if len(event)==1:
            save_event=False
        if save_event:
            new_list.append(event)
        save_event=True
    return new_list


def hist_from_statistics(stuff,filtered=True):
    fig,axs = plt.subplots(nrows=3,ncols=3)
    axs = axs.flatten()
    axs[0].hist(stuff[0],bins=100)
    axs[0].set_xlabel('Number of Clusters per Event')
    axs[1].hist(stuff[1],bins=10)
    axs[1].set_xlabel('Position in y-Direction')
    axs[2].hist(stuff[2],bins=6)
    axs[2].set_xlabel('Position in z-Direction')
    axs[3].hist(stuff[3],bins=1015)
    axs[3].set_xlabel('Position in x-Direction')
    axs[4].hist(stuff[4],bins=10000)
    axs[4].set_xlabel('Unique Strip Position')
    axs[5].hist(stuff[5],bins=12)
    axs[5].set_xlabel('Unique Sensor Position')
    axs[6].hist(stuff[6],bins=60)
    axs[6].set_xlabel('Number of Clusters on same Level')
    axs[7].hist(stuff[7],bins=60)
    axs[7].set_xlabel('Number of Clusters on same sensor')
    axs[8].hist(stuff[8],bins=4)
    axs[8].set_xlabel('Cluster Thickness')
    plt.show()


def splitter(event_list):
    one_event=[]
    two_event=[]
    three_event=[]
    four_event=[]
    five_event=[]
    six_event=[]
    for event in event_list:
        if len(event)==1:
            one_event.append(event)
        elif len(event)==2:
            two_event.append(event)
        elif len(event)==3:
            three_event.append(event)
        elif len(event)==4:
            four_event.append(event)
        elif len(event)==5:
            five_event.append(event)
        elif len(event)==6:
            six_event.append(event)
        else:
            raise LookupError('Somethings wrong')
            exit(1)
    return one_event,two_event,three_event,four_event,five_event,six_event




#hist_from_statistics(statistics(my_filter(event_list)))
one_event_list,two_event_list,three_event_list,four_event_list,five_event_list,six_event_list = splitter(my_filter(resort_and_stuff(event_list)))
easy_plotter(event_list)


#easy_plotter(six_event_list[0:1],1)



def alignment(event_list,make_alignment_plot=True):
    
    offset_list = np.zeros((len(event_list),12))
    if len(event_list[0])!=6:
        print('Wrong length of event_list. Use events with 6 long')
        return offset_list
    for i,event in enumerate(event_list):
        angles = angle_finder(event,offset_list[i])
        for j in range(len(event)-2):
            offset_list[i][j+2+6*int(event[j+2][5])] = np.tan(angles[0])*(list_with_distances[j+2]-list_with_distances[j+1])/0.09 +offset_list[i][j+1+6*int(event[j+1][5])]+event[j+1][2]-event[j+2][2]
    
    if make_alignment_plot:
        fig,axs = plt.subplots(nrows=3,ncols=4)
        axs=axs.flatten()

        for i in range(12):
            axs[i].hist(offset_list.T[i],bins=1000)
            axs[i].set_xlim(-40,40)
            axs[i].set_title(np.mean(offset_list.T[i]))
        plt.show()
    return np.mean(offset_list,axis=0)


def angle_finder(event,offset_list):
    angles = []
    for i in range(len(event)-1):
        angles.append(np.arctan(0.09*(event[i+1][2]-event[i][2]+offset_list[i+1+6*int(event[i+1][5])]-offset_list[i+6*int(event[i][5])])/(list_with_distances[int(event[i+1][4])] - list_with_distances[int(event[i][4])])))
    return angles


print('CLEAR --------------------->>>>>>>>>>>>>>>>>>>>>>>>')
offset_list = alignment(six_event_list)

print(six_event_list[0])

def angle(event_list,offset_list,to_degree,enable_filter,cut_value):
    import math
    angle_for_event = []
    for event in event_list:
        angles = angle_finder(event,offset_list)
        test_value =np.std(angles)/(abs(np.mean(angles)))
        if enable_filter and test_value >cut_value:
            continue
        angle_for_event.append(360/math.pi*np.mean(angles))
    return angle_for_event
two_angle=angle(two_event_list,offset_list,True,True,1.)
three_angle=angle(three_event_list,offset_list,True,True,1.)
four_angle=angle(four_event_list,offset_list,True,True,1.)
five_angle=angle(five_event_list,offset_list,True,True,1.)
six_angle=angle(six_event_list,offset_list,True,True,1.)
all_angles = two_angle+three_angle+four_angle+five_angle+six_angle

fig,axs = plt.subplots(nrows=3,ncols=2)
axs = axs.flatten()

fig.suptitle('Angle Distribution of muons')
axs[0].hist(two_angle,bins=1000)
axs[0].set_title(f'Angle Distribution of all two Events. N={len(two_angle)}' )
axs[1].hist(three_angle,bins=1000)
axs[1].set_title(f'Angle Distribution of all three Events. N={len(three_angle)}' )
axs[2].hist(four_angle,bins=1000)
axs[2].set_title(f'Angle Distribution of all four Events. N={len(four_angle)}' )
axs[3].hist(five_angle,bins=1000)
axs[3].set_title(f'Angle Distribution of all five Events. N={len(five_angle)}' )
axs[4].hist(six_angle,bins=1000)
axs[4].set_title(f'Angle Distribution of all six Events. N={len(six_angle)}' )
axs[5].hist(all_angles,bins=1000)
axs[5].set_title(f'Angle Distribution of all events. N={len(all_angles)}')
for i in range(6):
    axs[i].set_xlabel('Angles in degree')
plt.show()
#alignment(six_event_list)
#alignment(resort(six_event_list))