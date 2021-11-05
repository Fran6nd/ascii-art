#!/usr/local/bin/python3
from PIL import Image, ImageFont, ImageDraw
import sys
fnt = ImageFont.truetype('./terminus.ttf', 16)
chars = [" ", ".", ":", "|", "V", "O", "0", "#", "@"]
#chars = list(" .:-=+*#%@")
fnt_size = fnt.getsize("A")
print(fnt_size)
#chars = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
#chars.reverse()
for i in range(len(chars)):
    chars[i] = chars[i] + chars[i]
def process_pil_img(im):
    im.thumbnail((int(im.size[0]/fnt_size[0]), int(im.size[1]/fnt_size[1])), Image.ANTIALIAS)
    pixels = im.load()
    width, height = im.size

    output = ""


    for y in range(0, height):
        for x in range(0, width):
            r = pixels[x,y][0]
            g = pixels[x,y][1]
            b = pixels[x,y][2]
            avg = int( (r +g + b) / 3)
            avg = (int) (avg / 256 * len(chars))
            output = output + chars[avg]
        output = output + "\n"
    return output
def text_to_img(text, size, color = (0,0,0)):
        img = Image.new('RGB', (size[0] * fnt_size[0] * 2, int(size[1]*fnt_size[1]*2*2/3)) , color = (0, 0,0))
        #global fnt
        print(len(text.split("\n")))
        print(size, size[1]*fnt_size[1], size[1]*fnt_size[1] + 170)
        d = ImageDraw.Draw(img)
        d.text((0,0), text, font=fnt, fill=color)
        return img
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
        self.chars = [" ", ".", ":", "|", "V", "O", "0", "#", "@"]
        self.fnt_size = self.fnt.getsize("A")
        self.input_size = None
        self.text_size = [0,0]
        self.output_size = None
        for i in range(len(chars)):
            self.chars[i] = self.chars[i] + self.chars[i]
    def process_pil_img(self, im):
        if not self.input_size:
            self.input_size = im.size
        pixels = im.load()
        width, height = im.size

        output = ""

        self.text_size = [0,0]
        for y in range(0, height):
            for x in range(0, width):
                r = pixels[x,y][0]
                g = pixels[x,y][1]
                b = pixels[x,y][2]
                avg = int( (r +g + b) / 3)
                avg = (int) (avg / 256 * len(chars))
                output = output + chars[avg]
            output = output + "\n"
        return output
    def text_to_img(self, text, color = (0,0,0)):
        if not self.output_size:

            img = Image.new('RGB',self.output_size , color = (0, 0,0))
            #global fnt
            d = ImageDraw.Draw(img)
            d.text((0,0), text, font=fnt, fill=color)
            return img
    def full_process_img(self, img):
        return self.text_to_img(self.process_pil_img(img), (0,255, 0))