# This server is used to send an image to the client.
# The processing if done from the client using HWDigitRecog.py and once the image is processed, the result is sent back to the server. 


# in this code, the server sends an image through the ZMQ socket to the client and receives the processed image from the client
import zmq
import base64
import time
import cv2
import random
from sklearn.datasets import load_digits


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

message = socket.recv()
print("Server connected to Client successfully and Received ready status: %s" % message)
#  Wait for next request from client

# loading skleanr dataset digits
# here we load the dataset 
digits = load_digits()
#print(digits.data.shape)
#sample_image = digits.images[random.randint(0,digits.data.shape[0])]

#f = open("test.jpg", 'wb')
#f = "test.bmp"

#cv2.imwrite(f, sample_image)

while True:
    
    # send the image to client for processing
    # first sample one random image and save it to disk.
    index = random.randint(0,digits.data.shape[0]-1);
    sample_image = digits.images[index]
    f = "test" + str(index)  + ".bmp"
    cv2.imwrite(f, sample_image)
    # load the image from disk
    f_in = open(f,'rb')
    bytes = bytearray(f_in.read())
    strng = base64.b64encode(bytes)
    socket.send(strng)
    # do whatever else here while the response from client is being prepared
    # receive the processed image from the client
    message = socket.recv()
    
    ba = bytearray(base64.b64decode(message))
    print("Server-side Received request: %s" % ba.decode('utf-8'))

    time.sleep(1)

    

