"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""
import cv2
import numpy as np
from PIL import Image
import main
def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        
        if mirror: 
            img = cv2.flip(img, 1)
        #cv2.imshow('my webcam', img)  
        color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_image=Image.fromarray(color_coverted)

        #pil_image.thumbnail((int(pil_image.size[0]/2), int(pil_image.size[1]/2)), Image.ANTIALIAS)
        pil_image = main.text_to_img(main.process_pil_img(pil_image), pil_image.size, (0,255,0))
        numpy_image=np.array(pil_image)  

        # convert to a openCV2 image, notice the COLOR_RGB2BGR which means that 
        # the color is converted from RGB to BGR format
        img=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR) 
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()
def if_main():
    show_webcam(mirror=False)
if __name__ == '__main__':
    if_main()