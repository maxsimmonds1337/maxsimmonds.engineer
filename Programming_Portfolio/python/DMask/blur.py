#Import required Image library
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import numpy as np

#Open existing image
OriImage = Image.open('./images/1nb.jpeg')

blurImage = OriImage.filter(ImageFilter.GaussianBlur(15))
# blurImage.show()
#Save blurImage

# crop image 
width, height = blurImage.size
x = (width - height)//5
img_cropped = blurImage.crop((x, 0, x+height, height))

# create grayscale image with white circle (255) on black background (0)
mask = Image.new('L', img_cropped.size)
mask_draw = ImageDraw.Draw(mask)
width, height = img_cropped.size
mask_draw.ellipse((0, 0, width, height), fill=255)
#mask.show()


# add mask as alpha channel
img_cropped.putalpha(mask)

# save as png which keeps alpha channel 
img_cropped.save('./images/1_py.png')