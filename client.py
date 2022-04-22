
import zmq
import base64 , io 
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2
# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits


def classify_digit(image):
    # this function loads sklearn digits dataset, and then trains a support vector machine classifier
    # once trained, it will classify the input 'image' and returns the predicted digit in string format
    # the trianed classifier can be saved on disk to be reused but as it is fast to train, and not the focus here, it is not saved
    digits = load_digits()
    sample_image = digits.images[0]

    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))

    # Create a classifier: a support vector machine 
    clf = svm.SVC(gamma=0.001)

    # Split data into 50% train and 50% test subsets
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.2, shuffle=False
    )   

    # Learn the digits on the train subset
    clf.fit(X_train, y_train)
    # this model can  be saved on the disk and loaded next time to save time, however it is not necessary as it runs fast

    # Predict the value of the digit on the test input image
    predicted = clf.predict(image)

    return str(predicted)

context = zmq.Context()

#  Socket to talk to server
print("Client side- Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  send a request and wait for a response to make sure connection is ok
request = 1
print("Client-message-Sending request %s …" % request)
socket.send(b"Client Ready to start receiving images to process")

index = 1
while True:
    message = socket.recv()
    ba = bytearray(base64.b64decode(message))
    
    img = Image.open(io.BytesIO(ba))
    #plt.imshow(img)
    # send the image to the classifier and get the category name and send it back to the server
    img = np.array(img)
    img = img.reshape(1,img.size)
    category_name = classify_digit(img)
    
    #category_name = '1'
    bytes = bytearray(category_name,"utf-8")
    strng = base64.b64encode(bytes)
    socket.send(strng)
    
    print("Client-message Sent processed image label %s " % index)
    index += 1
