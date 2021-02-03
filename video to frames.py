import cv2 
  
def FrameCapture(path): 
    
    vidObj = cv2.VideoCapture(path) 
    
    count = 0
    
    success = 1
  
    while success: 

        success, image = vidObj.read() 

        try:
            cv2.imwrite("frames/frame%d.jpg" % count, image)
        except:
            pass
  
        count += 1
  
if __name__ == '__main__': 

    FrameCapture("bad_apple.mp4")
