import cv2
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################################################
wCam, hCam = 640, 480
################################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
previous_time = 0

detector = htm.handDetector(detectConf=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
  success, img = cap.read()
  img = detector.findHands(img, draw=False)
  lmList = detector.findPosition(img, draw=False)
  if len(lmList) != 0:
    x1, y1 = lmList[4][1], lmList[4][2]
    x2, y2 = lmList[8][1], lmList[8][2]
    cx, cy = (x1+x2)//2, (y1+y2)//2
    cv2.circle(img, (x1, y1), 5, (255,0,2), cv2.FILLED)
    cv2.circle(img, (x2, y2), 5, (255,0,2), cv2.FILLED)
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 2), 3)
    cv2.circle(img, (cx, cy), 5, (255, 255, 0), cv2.FILLED)

    length = math.hypot(x2-x1, y2-y1)
    vol = np.interp(length, [15, 120], [minVol, maxVol])

    volume.SetMasterVolumeLevel(vol, None)
    if length<15:
      cv2.circle(img, (cx, cy), 5, (255,255,255), cv2.FILLED)

    volDisplay = np.interp(volume.GetMasterVolumeLevel(), [minVol, maxVol], [0, 100])

    cv2.rectangle(img, (50, 150-(int(vol)*4)), (85, 410), (142, 156, 20), cv2.FILLED)
    cv2.putText(img, f'Volume: {int(volDisplay)}', (20, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

  cv2.rectangle(img, (50, 150), (85, 410), (142, 156, 20), 3)
  cv2.putText(img, 'Volume Level', (40,70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

  cv2.imshow("Image",img)
  cv2.waitKey(1)

