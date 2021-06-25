import cv2
import mediapipe as mp
import time

class handDetector:
  def __init__(self, mode=False, max_hands=2, detectConf=0.5, trackConf=0.5):
    self.mode = mode
    self.max_hands = max_hands
    self.detectConf = detectConf
    self.trackConf = trackConf

    self.mpHands = mp.solutions.hands
    self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.detectConf, self.trackConf)
    self.mpDraw = mp.solutions.drawing_utils
    
  def findHands(self, img, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.results = self.hands.process(imgRGB)
    if self.results.multi_hand_landmarks:
      for handLms in self.results.multi_hand_landmarks:
        if draw:
          self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
    
    return img

  def findPosition(self, img, handNum=0, draw=True):
    lmList = []
    if self.results.multi_hand_landmarks:
      myHand = self.results.multi_hand_landmarks[handNum]
      for id, lm in enumerate(myHand.landmark):
        h, w, c = img.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        lmList.append([id, cx, cy])
        if draw:
          cv2.circle(img, (cx, cy), 10, (255, 134, 132), cv2.FILLED)
    
    return lmList

def main():
  cap = cv2.VideoCapture(0)
  previous_time = 0
  current_time = 0
  detector = handDetector()
  
  while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
      print(lmList[0])
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.imshow("Image", img)
    cv2.waitKey(1)

if __name__=='__main__':
  main()