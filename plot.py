import serial
import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import datetime

import tkinter as tk   
def moving_average(x, w):
    return np.convolve(x, np.ones(w)/w, mode='valid')

def main(flag):

    flag=flag
        
    serial_port='COM6'#9
    baud_rate=4800
    ser=serial.Serial(serial_port, baud_rate)

    time_formatted=datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    filename = time_formatted # + extra argument
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    
    data_array = []
    time_array = []
    angle_array=[]
    toe_heel_array=[]

    t0 = time.time()

    toe_color = '#ffcccb'
    heel_color = '#90ee90'
    toe_heel_color = '#add8e6'
    
    sample_data=[]
    sample_time=[]
    

    with open("saved_data"+'.csv', 'r', encoding='UTF8', newline='') as f:
                    reader = csv.reader(f, delimiter=',')
                    count=0
                    next(f)
                    next(f)
                    for i in reader:
                        sample_time.append(float(i[0]))
                        sample_data.append(float(i[1]))
                    #print(len(sample_data))
                    #print(len(sample_time))
                        

    while True:
        
        try:
            data = ser.readline()
            data = data.decode("utf-8")
            data = data.strip()
            #data = float(data)
            
            toe_heel = (int(data[2]), int(data[5]))
            angle = data.replace(data[0:data.index("A:")+2],"")
            
            angle_array.append(float(angle))
            toe_heel_array.append(toe_heel)

            relative_time = time.time() - t0
            time_array.append(relative_time)

            
            data_array.append(data)
            print(data)

        except KeyboardInterrupt:
            print("\nYou have finished recording!")
            
            # print(time_array)
            # print("time_array length:  "+str(len(time_array)))
            # print(toe_heel_array)
            # print("toe_heel_array length:  "+str(len(toe_heel_array)))
            # print(angle_array)
            # print("angle_array length:  "+str(len(angle_array)))
            
            ser.close()

            data_array = np.array(data_array)
            sample_data=np.array(sample_data)
            time_array = np.array(time_array)
            angle_array = np.array(angle_array)
            toe_heel_array = np.array(toe_heel_array)

          

            window_width = 17
            
            data_array_filtered = moving_average(angle_array, window_width)

            fig, ax1 = plt.subplots()
            #print(len(sample_data))
            #print(len(sample_time))
            plt.plot(time_array[8:-8], data_array_filtered, label="Actual Measurement")
            plt.plot(sample_time, sample_data, "--", label="Sample Measurement")
            plt.title("Foot Angle")
            plt.xlabel("Time(s)")
            plt.ylabel("Angle (degrees)")
            #ax1.set_ylim(0,180)

            for index, tuple in enumerate(toe_heel_array[:-1]):
                if tuple[0]==1 and tuple[1]==0: #toe touches, heel doesn't
                    ax1.axvspan(time_array[index], time_array[index+1], color=toe_color, label="Toe")
                elif tuple[0]==0 and tuple[1]==1: #heel touches, toe doesn't
                    ax1.axvspan(time_array[index], time_array[index+1], color=heel_color, label="Heel")
                elif tuple[0]==1 and tuple[1]==1: #they both touch
                    ax1.axvspan(time_array[index], time_array[index+1], color=toe_heel_color, label="Both")
            #ax1.axhline(y=60, color='r', label="ROM Bounds")
            #ax1.axhline(y=140, color='r')
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys(), fontsize="5", loc='upper right')
            plt.show()

            fig.savefig(filename+'.png')

            mean = np.mean(data_array_filtered)

            summary = ['Average angle', mean]
            header = ['Time', 'Variable1', 'Variable2', 'Variable3']

            time_array = list(time_array)
            data_array_filtered = list(data_array_filtered)

            #print(data_array_filtered)
            #print(time_array)

            if flag==1:
                with open("saved_data"+'.csv', 'w', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)

                    writer.writerow(summary)

                    writer.writerow(header)

                    for i in range(len(data_array_filtered)):
                        f.write("%s,%s\n"%(time_array[i+8],data_array_filtered[i]))

            ser.close()
            break

def measure_data():
    main(0)
def save_data():
    main(1)
parent = tk.Tk()
frame = tk.Frame(parent)
frame.pack()
parent.geometry("300x300")
parent.title("A Gait Solution")
md= tk.Button(frame, 
                   text="Measure Data", 
                   command=measure_data,height=5,width=10
                   )

md.pack(side=tk.TOP, padx=10,pady=50)

sd = tk.Button(frame,
                   text="Save data",
                   fg="green",
                   command=save_data,height=5,width=10)
sd.pack(side=tk.BOTTOM)

parent.mainloop()




#main()
