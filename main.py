#!/usr/local/bin/python3
from PIL import Image, ImageFont, ImageDraw
import sys
fnt = ImageFont.truetype('./terminus.ttf', 15)
chars = [" ", ":", "-", "|", "V", "O", "0", "&", "#"]
chars = list(" .:-=+*#%@")
#chars = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
#chars.reverse()
for i in range(len(chars)):
    chars[i] = chars[i] + chars[i]
def process_pil_img(im):
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
        img = Image.new('RGB', (size[0] * 15, size[1]*15), color = (0, 0,0))
        #global fnt
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
