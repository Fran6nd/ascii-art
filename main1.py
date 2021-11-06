"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""
import cv2
import time
import numpy as np
from PIL import Image
import main

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    filter = main.videofilter()
    prev_frame_time = 0
  
    new_frame_time = 0
    while True:
    
        
        font = cv2.FONT_HERSHEY_SIMPLEX 
        
        new_frame_time = time.time() 
    
        
    
        
        
        
        fps = 1/(new_frame_time-prev_frame_time) 
        prev_frame_time = new_frame_time 
    
        
        fps = int(fps) 
    
        
        
        fps = str(fps) 
        ret_val, img = cam.read()

        
        if mirror: 
            img = cv2.flip(img, 1)
        #cv2.imshow('my webcam', img)  


        color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_image=Image.fromarray(color_coverted)
        pil_image = filter.full_process_img(pil_image)
        #pil_image = filter.text_to_img(filter.process_cv_image(img), (0,255,0) )
        #filter.process_cv_image(img)
        numpy_image=np.array(pil_image)  

        # convert to a openCV2 image, notice the COLOR_RGB2BGR which means that 
        # the color is converted from RGB to BGR format
        img=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR) 
        cv2.putText(img, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()
def if_main():
    show_webcam(mirror=True)
if __name__ == '__main__':
    if_main()