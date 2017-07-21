from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random


def rd_check_code(width=120,height=30,char_length=5,font_file='static/font/domi.ttf',font_size=28):
    code=[]
    img=Image.new(mode='RGB',size=(width,height),color=(255,255,255))
    draw=ImageDraw.Draw(img,mode='RGB')

    def rndChar():
        return chr(random.randint(65,90))
    def rndColor():
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    font=ImageFont.truetype(font_file,font_size)
    for i in range(char_length):
        char=rndChar()
        code.append(char)
        h=random.randint(0,4)
        draw.text([i*width/char_length,h],char,font=font,fill=rndColor())

    for i in range(10):
        draw.point([random.randint(0,width),random.randint(0,height)],fill=rndColor())
    for i in range(1):
        x=random.randint(0,width)
        y=random.randint(0,height)
        draw.arc((x,y,x+4,y+4),0,90,fill=rndColor())
    for i in range(0):
        x = random.randint(0, width)
        y = random.randint(0, height)
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        draw.line((x1,y1,x,y),fill=rndColor())

    img=img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img,''.join(code)