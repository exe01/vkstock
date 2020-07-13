from backend.stock_api.builders import ImageBuilder, TextBuilder
from PIL import Image, ImageOps


# textBuilder = TextBuilder()
#
# text = 'text1text1text1text1'
# ref_text = 'text2text2text2text2'
#
# ret = textBuilder.format_text(text, "")
# print(ret)
#
# ret = textBuilder.format_text("", ref_text)
# print(ret)
#
# ret = textBuilder.format_text("", "")
# print(ret)
#
# ret = textBuilder.format_text(text, ref_text)
# print(ret)

imageBuilder = ImageBuilder()


# im = Image.open('media/post_images/stockApiLoader_2ITUUWR.jpeg')

# text = """You can create instances of this class in several ways; either by loading images from files, processing other images, or creating images from scratch.
# To load an image from a file, use the open() function in the Image module:"""

im = Image.new('RGB', (1, 0), color="white")

x, y = im.size

# new_im = ImageOps.expand(im, border=30)
# new_im.show()

im.show()

# new_img = ImageOps.fit(
#     im,
#     (x+100, y+100),
#     Image.EXTENT,
# )
#
# new_img.show()

# im = im.transform(
#     (x, y + 500),
#     Image.EXTENT,
#     data=(0, 500, x, y),
#     fill=(0, 0, 0)
# )
#
# im.show()

# new_im = imageBuilder.build(im, text)

# width = 400
#
# orig_width, orig_height = im.size
#
# scale_factor = orig_width/width
#
# height = int(orig_height/scale_factor)
#
# new_im = im.resize((width, height))
# new_im.show()
# im.show()
#
# new_im.show()

