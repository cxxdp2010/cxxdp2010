# ms_slave.py 
import hashlib 
import sys 
  
if __name__ == "__main__": 
    for input_str in iter(sys.stdin.buffer.readline, b''): 
        input_str = input_str.strip().decode() 
        if input_str == 'Quit': 
            break
        # encode the string in UTF-8 format before hashing 
        hash_object = hashlib.sha256(input_str.encode('utf-8')) 
        # get the hexadecimal representation of the hash 
        hex_dig = hash_object.hexdigest() 
        print(hex_dig)