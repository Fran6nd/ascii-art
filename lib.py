#!/usr/local/bin/python3
from PIL import Image, ImageFont, ImageDraw
import numpy
import time
import cv2
import sys
import threading

SCALE_FACTOR = 0.05

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
        self.chars = list(" ,:;|1[{CO0@")
        #self.chars = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
        #self.chars.reverse()
        for i in range(len(self.chars)):
            self.chars[i] = self.chars[i] + self.chars[i]

        self.fnt_size = self.fnt.getsize("A")
        self.line_spacing = self.fnt.getsize_multiline("A\nB")[1] - 2 * self.fnt_size[1]
        #print(self.line_spacing)
        self.input_size = None
        self.output_size = None

    def process_cv_image(self, im : numpy.ndarray,  max_size = None):
        start = time.process_time()
        output = ""
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        if not max_size:
            im = cv2.resize(im, None, fx = 1 * SCALE_FACTOR, fy = 1 * SCALE_FACTOR, interpolation = cv2.INTER_CUBIC)
        else:
            SCALE_FACTOR = 1/max(im.shape[0]/max_size[0],im.shape[1]/max_size[1])
            max_size = (int(max_size[0]/2), max_size[1])
            im = cv2.resize(im, max_size, interpolation = cv2.INTER_CUBIC)
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
        return output
    def process_pil_img(self, im, max_size = None):
        start = time.process_time()
        im.thumbnail((int(im.size[0]*SCALE_FACTOR), int(im.size[1]*SCALE_FACTOR)), Image.ANTIALIAS)
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

            self.chars_img = list()
            for c in self.chars:
                size = self.fnt_size
                tmp = Image.new('RGB',self.fnt.getsize(c) , color = (0, 0,0))
                d = ImageDraw.Draw(tmp)
                d.text((0,0), c, font=self.fnt, fill=color)
                self.chars_img.append(tmp)

        #global fnt

        start = time.process_time()
        def do_lines(start, stop):
            #print(start, stop)
            
            subtext = text[start * (line_length + 1): stop * (line_length + 1)]

            self.d.text((0,start * (self.line_spacing + self.fnt_size[1])), subtext, font=self.fnt, fill=color)
        #self.img.paste( (0,0,0), [0,0,self.img.size[0],self.img.size[1]])


        #self.run_in_thread(lambda : do_lines(0, int(lines/2)))

        #do_lines(int(lines/2), lines)
        text = text.split("\n")
        for y in range(len(text)):
            for x in range(int(len(text[y])/2)):
                index = 0
                for i in range(len(self.chars)):
                    if self.chars[i] == text[y][x*2] + text[y][x*2+1]:
                        index = i
                        break
                offset =  (x * self.fnt_size[0] *2,y* (self.fnt_size[1]+self.line_spacing))
                self.img.paste(self.chars_img[index], (offset[0],offset[1], self.chars_img[index].size[0]+offset[0],offset[1]+self.chars_img[index].size[1]))

        #do_lines(0,lines)
        while self.threads != 0:
            pass
        #print("text->img", time.process_time() - start)
        return self.img
    def full_process_img(self, img):
        return self.text_to_img(self.process_pil_img(img), (0,255, 0))