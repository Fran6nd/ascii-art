from PIL import Image
im = Image.open('index.jpg')

pixels = im.load()
width, height = im.size
print(width, height)
output = ""
chars = ["  ", "--", "::", "||", "[]", "00", "&&", "##"]
for x in range(0, width):
    for y in range(0, height):
        #print(pixels[x,y])
        r = pixels[x,y][0]
        g = pixels[x,y][1]
        b = pixels[x,y][2]
        avg = int( (r +g + b) / 3)
        pixels[x,y] = (avg,avg,avg)
        avg = (int) (avg / 256 * len(chars))
        output = output + chars[avg]
        

    output = output + "\n"
im.save("test.png")
with open("output.txt", "w") as f:
    f.write(output)
