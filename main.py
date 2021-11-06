#!/usr/local/bin/python3
from PIL import Image, ImageFont, ImageDraw
import numpy
import time
import cv2
import sys
import threading
from profilestats import profile

def main():
    im = Image.open(sys.argv[1])



            

    output = process_pil_img(im)
    if len(sys.argv) == 2: 
        #with open("output.txt", "w") as f:
        # f.write(output)
        print(output)

    else:
        im.save(text_to_img(output, im.size))

if __name__ == '__main__':
    main()

class videofilter():
    def __init__(self):
        self.threads = 0
        self.fnt = ImageFont.truetype('./terminus.ttf', 32)
        #self.chars = [" ", ".", ":", "|", "V", "O", "0", "#", "@"]
        #self.chars = list(" .:-=+*#%@")
        self.chars = list(" ,:|1O0@")
        for i in range(len(self.chars)):
            self.chars[i] = self.chars[i] + self.chars[i]

        self.fnt_size = self.fnt.getsize("A")
        self.line_spacing = self.fnt.getsize_multiline("A\nB")[1] - 2 * self.fnt_size[1]
        print(self.line_spacing)
        self.input_size = None
        self.output_size = None

    def process_cv_image(self, im : numpy.ndarray):
        start = time.process_time()
        output = ""
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.resize(im, None, fx = 1 * 0.1/1.5, fy = 1 * 0.1/1.5, interpolation = cv2.INTER_CUBIC)
        #im = numpy.rot90(im,0)
        if not self.input_size:
            self.input_size = im.shape
        #im = cv2.resize(im, (im.size[0], im.size[1]/2))

        prevx = 0
        for x,y in numpy.ndindex(im.shape):
            #print(x, y)
            if prevx != x:
                output = output + "\n"
                prevx = x
            avg = (int) (im[x][y] / 256 * len(self.chars))
            output = output + self.chars[avg]
        #exit()
        #print("cv->text", time.process_time() - start)
        return output[:-1]
    def process_pil_img(self, im):
        start = time.process_time()
        im.thumbnail((int(im.size[0]/10/1.5), int(im.size[1]/10/1.5)), Image.ANTIALIAS)
        if not self.input_size:
            self.input_size = im.size
        pixels = im.load()
        width, height = im.size

        output = ""
        self.line = 0
        for y in range(0, height):
            for x in range(0, width):
                r = pixels[x,y][0]
                g = pixels[x,y][1]
                b = pixels[x,y][2]
                avg = int( (r +g + b) / 3)
                avg = (int) (avg / 256 * len(self.chars))
                output = output + self.chars[avg]
            output = output + "\n"
            self.line += 1

        #print("pill->text", time.process_time() - start)
        return output[:-1]
    def run_in_thread(self, target):
        def thread():
            self.threads += 1
            target()
            self.threads -= 1
        threading.Thread(target=thread).start()
    def text_to_img(self, text, color = (0,0,0)):
        lines = len(text.split('\n'))
        line_length = len(text.split('\n')[0])

        if not self.output_size:
            self.output_size = self.fnt.getsize_multiline(text)
            self.img = Image.new('RGB',self.output_size , color = (0, 0,0))
            self.d = ImageDraw.Draw(self.img)
        #global fnt

        start = time.process_time()
        def do_lines(start, stop):
            #print(start, stop)
            
            subtext = text[start * (line_length + 1): stop * (line_length + 1)]
            self.d.text((0,start * (self.line_spacing + self.fnt_size[1])), subtext, font=self.fnt, fill=color)
        self.img.paste( (0,0,0), [0,0,self.img.size[0],self.img.size[1]])
        #for i in range (k-1):
        #    self.run_in_thread(lambda : do_lines(int(i/k) * lines, int((1 + i) / k * lines)))
        self.run_in_thread(lambda : do_lines(0, int(lines/2)))
        #self.run_in_thread(lambda : do_lines(int(lines/4), int(lines/2)))
        #self.run_in_thread(lambda : do_lines(int(lines/2), int(3*lines/4)))
        #do_lines(int(3*lines/4), lines)
        #print(self.th)
        do_lines(int(lines/2), lines)
        #do_lines(0,lines)
        while self.threads != 0:
            pass
        #print("text->img", time.process_time() - start)
        return self.img
    def full_process_img(self, img):
        return self.text_to_img(self.process_pil_img(img), (0,255, 0))