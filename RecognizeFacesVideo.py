from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
	help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
	help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="hogs",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

print("[INFO] loading encodings...")

data = pickle.loads(open(args["encodings"],"rb").read())

print("[INFO] starting video stream...")

vs = VideoStream(src=0).start()
writer=None
time.sleep(2.0)

while 1:

    frame = vs.read()

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frameRGB = imutils.resize(frame, width=750)
    r = frame.shape[1]/float(frameRGB.shape[1])

    roi = face_recognition.face_locations(frameRGB, model=args["detection_method"])
    encodings = face_recognition.face_encodings(frameRGB, roi)
    names = []

    for encoding in encodings:

        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknow"

        if True in matches:

            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:

                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key = counts.get)
        names.append(name)

    for ((top, right, bottom, left), name) in zip(roi, names):

		
	    top = int(top * r)
	    right = int(right * r)
	    bottom = int(bottom * r)
	    left = int(left * r)
 
		
	    cv2.rectangle(frame, (left, top), (right, bottom),
		    (0, 255, 0), 2)
	    y = top - 15 if top - 15 > 15 else top + 15
	    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
		    0.75, (0, 255, 0), 2)

    
    if writer is None and args["output"] is not None:
	    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
	    writer = cv2.VideoWriter(args["output"], fourcc, 20,
		    (frame.shape[1], frame.shape[0]), True)
 
	
    if writer is not None:
	    writer.write(frame)

    if args["display"] > 0:
	    cv2.imshow("Frame", frame)
	    key = cv2.waitKey(1) & 0xFF
 
		
	    if key == ord("q"):
		    break

cv2.destroyAllWindows()
vs.stop()

if writer is not None:
    writer.release()