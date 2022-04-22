# ZMQ_Hand_Written_digits
This is a repo for a client server message sending with ZMQ. 

First run the server.py file, followed by running client.py

The server file, reads a random image from digits dataset from sklearn and writes it to the disk. 
This image is then sent through zmq to client file. 
Client trains the digits dataset from sklearn using a simple support vector classification, and predicts the classification of the test image sent via server and return its classification label to the server. 
