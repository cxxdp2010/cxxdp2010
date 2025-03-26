# ms_master.py 
import threading 
import queue 
import subprocess 
  
  
def read_output(process, output_queue): 
    # this function will be run in a separate thread to read the output of the process 
    for line in iter(process.stdout.readline, b''): 
        output_queue.put(line.decode('utf-8').strip()) 
  
if __name__ == '__main__': 
    # start the subprocess 
    process = subprocess.Popen('python -u ms_slave.py'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE) 
    # create a queue to hold the output lines 
    # create a separate thread to read from its stdout 
    output_queue = queue.Queue() 
    thread = threading.Thread(target=read_output, args=(process, output_queue)) 
    thread.start() 
  
    # print the lines from the queue 
    while process.poll() is None: 
        input_str = input("Enter a string to hash(Enter \"Quit\" to exit): ") 
        input_str = input_str.strip().encode() + b'\n'
        process.stdin.write(input_str) 
        process.stdin.flush() 
        try: 
            while True: 
                print('Got:', output_queue.get(timeout=0.02)) 
        except queue.Empty: 
            pass
    # process.terminate() 
    thread.join() 
    print('Ended.')