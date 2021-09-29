from PIL import Image
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
        pixels[x,y] = (avg,avg,avg)

im.thumbnail((100,100),Image.ANTIALIAS)
im.save("test.jpg")


im = Image.open('test.jpg')
pixels = im.load()
width, height = im.size
print(width, height)
output = ""
chars = ["  ", "--", "::", "||", "[]", "OO", "00", "&&", "##"]


for x in range(0, width):
    for y in range(0, height):
        #print(pixels[x,y])
        avg = pixels[x,y][0]
        avg = (int) (avg / 256 * len(chars))
        output = output + chars[avg]
        

    output = output + "\n"
#with open("output.txt", "w") as f:
#    f.write(output)
print(output)
