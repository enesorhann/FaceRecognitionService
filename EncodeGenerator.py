import cv2
import face_recognition
import os
import pickle

folderPath = "Images"
pathList = os.listdir(folderPath)
imgList=[]
idList=[]

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    idList.append(os.path.splitext(path)[0])
    
print(imgList)
print(idList)

def findEncodings(imageList):
    encodeList=[]
    for img in imageList:
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        
    return encodeList
    
print("Encoding Started")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIDS = [encodeListKnown,idList]
print("Encoding Finally")

file = open("EncodeFile.p","wb")
pickle.dump(encodeListKnownWithIDS,file)
file.close()
print("File Saved")