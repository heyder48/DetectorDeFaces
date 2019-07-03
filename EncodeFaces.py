# -*- coding: utf-8 -*-

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

#Construindo argparse e passando os argumentos

ap=argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required= True, help = "path to input directory of faces + image")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hogs",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))
 
# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):
    print("[INFO] processing image {} of {}".format(i + 1, len(imagePaths)))

    name=imagePath.split(os.path.sep)[-2]

    #Carrega a imagem e muda o esquema de cores para RGB pois dlib espera um arquivo em RGB
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #gera a região de interresse

    roi = face_recognition.face_locations(rgb , model=args["detection_method"])

    encodings = face_recognition.face_encodings(rgb, roi)

    for encoding in encodings:

        knownEncodings.append(encoding)
        knownNames.append(name)

print("[INFO] Serializing encodings ...")
data = {"encodings" : knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close() 


