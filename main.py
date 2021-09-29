#!/usr/local/bin/python3
from PIL import Image, ImageFont, ImageDraw
import sys
im = Image.open(sys.argv[1])

pixels = im.load()
width, height = im.size

for x in range(0, width):
    for y in range(0, height):
        #print(pixels[x,y])
        r = pixels[x,y][0]
        g = pixels[x,y][1]
        b = pixels[x,y][2]
        avg = int( (r +g + b) / 3)
        pixels[x,y] = (avg,avg,avg, 255)

im.thumbnail((150,150),Image.ANTIALIAS)
#im.save("test.png")


#im = Image.open('test.png')
pixels = im.load()
width, height = im.size

output = ""
chars = ["  ", "::", "--", "||", "VA", "OO", "00", "&&", "##"]



for y in range(0, height):
    for x in range(0, width):
        #print(pixels[x,y])
        avg = pixels[x,y][0]
        avg = (int) (avg / 256 * len(chars))
        output = output + chars[avg]
        

    output = output + "\n"
if len(sys.argv) == 2: 
    #with open("output.txt", "w") as f:
       # f.write(output)
    print(output)

else:
    img = Image.new('RGB', (width * 15, height*15), color = (0, 0,0))
    
    fnt = ImageFont.truetype('./terminus.ttf', 15)
    d = ImageDraw.Draw(img)
    d.text((0,0), output, font=fnt, fill=(255, 255, 255))
    img.save(sys.argv[2])
