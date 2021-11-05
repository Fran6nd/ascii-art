#!/usr/local/bin/python3
from PIL import Image, ImageFont, ImageDraw
import sys

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
        self.fnt = ImageFont.truetype('./terminus.ttf', 16)
        #self.chars = [" ", ".", ":", "|", "V", "O", "0", "#", "@"]
        #self.chars = list(" .:-=+*#%@")
        self.chars = list(" ,:|1O0@")
        for i in range(len(self.chars)):
            self.chars[i] = self.chars[i] + self.chars[i]

        self.fnt_size = self.fnt.getsize("A")
        self.input_size = None
        self.text_size = [0,0]
        self.output_size = None
    def process_pil_img(self, im):
        im.thumbnail((int(im.size[0]/10), int(im.size[1]/10/2)), Image.ANTIALIAS)
        if not self.input_size:
            self.input_size = im.size
        pixels = im.load()
        width, height = im.size

        output = ""

        self.text_size = [0,0]
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
        return output
    def text_to_img(self, text, color = (0,0,0)):
        if not self.output_size:
            self.output_size = self.fnt.getsize_multiline(text)
        img = Image.new('RGB',self.output_size , color = (0, 0,0))
        #global fnt
        d = ImageDraw.Draw(img)
        d.text((0,0), text, font=self.fnt, fill=color)
        return img
    def full_process_img(self, img):
        return self.text_to_img(self.process_pil_img(img), (0,255, 0))