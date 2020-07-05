import os
import cv2
import uuid



def dirChange():
    os.chdir(r"E:\Projectcollection\DjangoProjects\WasteMainframe\darknet")


# basic0 = "./darknet.exe detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights "  # dependent weights
# basic1 = " -out "  # internal fucntion to save to custom directory


def raw_img_to_covert_processed_img(key, rawImagePath, processedImagePath):

    dirChange()
    curDir = os.getcwd()
    print("#####################################")
    print("current dir = ", curDir)
    print("#####################################")
    
    
    basic0 = "./darknet.exe detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights "  # dependent weights
    basic1 = " -out "  # internal fucntion to save to custom directory
    print("####################key######################")
    print(key)
    print("####################rawImagePath#" + rawImagePath + "#####################")
    print("####################processedImagePath#" + processedImagePath + "#####################")
    print("*******yup********")
    uuidNo = uuid.uuid1()
    # print(uuidNo)
    # source = rawImagePath
    # print(source)
    destination = processedImagePath + "/" + str(uuidNo)
    # print(destination)
    run = basic0 + rawImagePath + basic1 + destination
    print("######################")
    print(run)
    print("######################")
    file0 = open('mainExecFile.txt', 'w+')
    file0.write(run)
    file0.close()
    curDir = os.getcwd();
    print("#####################################")
    print("current dir[This one] = ", curDir)
    print("#####################################")
    os.system("bash mainExecFile.txt")
    curDir = os.getcwd();
    print("#####################################")
    print("current dir = ", curDir)
    print("#####################################")

    print("Destinatiom#####################################")
    print(destination)
    print("#####################################")
    mainImageToExport = cv2.imread("predictions.jpg")
    # cv2.imshow("ProcessedImage", mainImageToExport)
    cv2.imwrite((destination + ".jpg"), mainImageToExport)
    return key, str(uuidNo)+".jpg"


# The below lines are used to test the above defined function

# uniqueID, key = raw_img_to_covert_processed_img(5,"E:/Projectcollection/DjangoProjects/WasteMainframe/WasteRawImage/a.jpg","E:/Projectcollection/DjangoProjects/WasteMainframe/WasteProcessedImage")
#
# print(uniqueID)
# print(key)
