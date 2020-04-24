import os
import _thread
import fileinput
import time
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation

file= open("ping_output.log","w+")
file.truncate(0)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.grid(b=True, which='major', color='#666666', linestyle='-')

time_pattern=r"time=\d+\.\d*"
time_pattern_obj=re.compile(time_pattern)

sequence_pattern=r"icmp_seq[ =]{1}\d+"
sequence_pattern_obj=re.compile(sequence_pattern)

timeout_pattern=r"timeout"
timeout_pattern_obj=re.compile(timeout_pattern)

ping_count = 0
ping_time = []
ping_sequence = []
ping_base = []

def ping():
    os.system("ping 8.8.8.8 > ping_output.log")

def read_stdin(i):
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        analize_line(line)

def analize_line(line):
    global ping_sequence
    global ping_time
    global time_pattern
    global ping_count
    global ping_base

    time_result = time_pattern_obj.search(line)
    #sequence_result = sequence_pattern_obj.search(line)
    timeout_result = timeout_pattern_obj.search(line)

    if time_result:
        time = float(time_result.group()[5:])
        ping_time.append(time)
        ping_sequence.append(ping_count)
        ping_base.append(15)
        ping_count += 1
    elif timeout_result:
        ping_time.append(700)
        ping_sequence.append(ping_count)
        ping_base.append(15)
        ping_count += 1
    
    #if sequence_result:
    #    sequence = int(sequence_result.group()[9:])
    

    ping_time = ping_time[-50:]
    ping_sequence = ping_sequence[-50:]
    ping_base = ping_base[-50:]

    ax.clear()
    ax.plot(ping_sequence, ping_time, color="blue")
    ax.plot(ping_sequence, ping_base, color="red")

    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.title('Ping in Casa')
    plt.ylabel('Time (ms)')

try:
    _thread.start_new_thread( ping, () )
except:
   print("Error: unable to start thread")

ani = animation.FuncAnimation(fig, read_stdin, interval=500, repeat=False)
plt.show()