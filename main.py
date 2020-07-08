import os
import cv2
import uuid
from WasteMainframe.settings import BASE_DIR


def dirChange():
    # print("needed dir:", BASE_DIR)
    os.chdir(BASE_DIR + "\darknet")


# basic0 = "./darknet.exe detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights "  # dependent weights
# basic1 = " -out "  # internal fucntion to save to custom directory


def raw_img_to_covert_processed_img(key, rawImagePath, processedImagePath):

    dirChange()
    curDir = os.getcwd()
    print("Start Of Execution")

    basic0 = "./darknet.exe detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights "  # dependent weights
    basic1 = " -out "  # internal fucntion to save to custom directory

    # print("The Key in subject : " + key)
    # print("Raw Image's Path : " + rawImagePath)
    # print("Processed Image's Path : " + processedImagePath)
    uuidNo = uuid.uuid1()
    destination = processedImagePath + "/" + str(uuidNo)
    run = basic0 + rawImagePath + basic1 + destination
    print("Driver Code to Bash : " + run)

    file0 = open('mainExecFile.txt', 'w+')
    file0.write(run)
    file0.close()
    os.system("bash mainExecFile.txt")
    curDir = os.getcwd();

    mainImageToExport = cv2.imread("predictions.jpg")
    # cv2.imshow("ProcessedImage", mainImageToExport) ~enable this to view the processed image as soon as execution
    # is over
    cv2.imwrite((destination + ".jpg"), mainImageToExport)
    print("End Of Execution")
    return key, str(uuidNo)+".jpg"


# The below lines are used to test the above defined functions

# uniqueID, key = raw_img_to_covert_processed_img(5,
# "E:/Projectcollection/DjangoProjects/WasteMainframe/WasteRawImage/a.jpg",
# "E:/Projectcollection/DjangoProjects/WasteMainframe/WasteProcessedImage")
