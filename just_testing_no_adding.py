

from PIL import Image,ImageOps,ImageDraw,ImageFilter,ImageFont
import numpy as np

img1 = Image.open("Resources/welcome_banner.png")
#img.show()
prof = Image.open("Resources/sample_avatar.png")
prof = prof.resize((300,300))
#prof.show()

img=prof.convert("RGB")
npImage=np.array(img)
h,w=img.size

# Create same size alpha layer with circle
alpha = Image.new('L', img.size,0)
draw = ImageDraw.Draw(alpha)
draw.pieslice([0,0,h,w],0,360,fill=255)

# Convert alpha Image to numpy array
npAlpha=np.array(alpha)

# Add alpha layer to RGB
npImage=np.dstack((npImage,npAlpha))

# Save with alpha
final=Image.fromarray(npImage)
final.save('Output/welcome.png')

f = Image.open("Output/welcome.png")
img1.paste(f,((img1.size[0]-f.size[0])//2,240),f.convert('RGBA'))
user="Napoleon Bonaparte#9043"
m = ImageDraw.Draw(img1)
size=30
font = ImageFont.truetype("arial.ttf",size)
text = f"Welcome to the server, {user}"
no=390
count= f"Member number: #{no}"
while font.getsize(text)[0]<0.8*img1.size[0]:
    size+=1
    font = ImageFont.truetype("arial.ttf",size)
print(size)
m.text(((img1.size[0]-font.getsize(text)[0])//2,570),text,(255,255,255),font=font)
m.text(((img1.size[0]-font.getsize(count)[0])//2,570+size+10),count,(255,255,255),font=font)

img1.show()
img1.save('Output/welcomemessage.png')
