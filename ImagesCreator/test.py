# from PIL import Image, ImageDraw, ImageFont
#
# im = Image.open('images/download.jpeg')
#
# xsize, ysize = im.size
# offset = 100
#
# nim = Image.new('RGB', (xsize, ysize+offset), color="white")
# nim.paste(im, (0, offset))
#
# imdr = ImageDraw.Draw(nim)
#
# fnt = ImageFont.truetype("fonts/tahoma.ttf", 40)
# imdr.text((10, 10), "Helo wrld@", fill=(0, 0, 0), font=fnt)
#
# # imdr.
#
# nim.show()
#
# # rim = im.resize((xsize+100, ysize+100))
#
# # rim.show()