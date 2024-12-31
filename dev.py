from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__, static_folder="./api/static", template_folder="./api/templates")

# Load component images from folders
SKIN_IMAGES = []
for f in os.listdir('./api/static/skin'):
    if f.endswith('.png'):
        SKIN_IMAGES.append(f)

CLOTH_IMAGES = []  
for f in os.listdir('./api/static/cloth'):
    if f.endswith('.png'):
        CLOTH_IMAGES.append(f)
        
HAIR_IMAGES = []
for f in os.listdir('./api/static/hair'):
    if f.endswith('.png'):
        HAIR_IMAGES.append(f)

BG_IMAGES = []
for f in os.listdir('./api/static/bg'):
    if f.endswith('.png'):
        BG_IMAGES.append(f)
 
EYES_IMAGES = []
for f in os.listdir('./api/static/eyes'):
    if f.endswith('.png'):
        EYES_IMAGES.append(f)

MOUTH_IMAGES = []
for f in os.listdir('./api/static/mouth'):
    if f.endswith('.png'):
        MOUTH_IMAGES.append(f)

PLUS = []
for f in os.listdir('./api/static/plus'):
    if f.endswith('.png'):
        PLUS.append(f)
        
@app.route('/')
def home():
    return render_template('home.html')

# Editor route            
@app.route('/editor')
def editor():
    return render_template('v2editor.html', 
        skin_images=SKIN_IMAGES,
        cloth_images=CLOTH_IMAGES,
        hair_images=HAIR_IMAGES,
        bg_images = BG_IMAGES,
        eyes_images = EYES_IMAGES,
        #eyes_plus = EYES_PLUS,
        plus = PLUS,
        mouth_images = MOUTH_IMAGES
    )


# Render preview route
@app.route('/render_preview')
def render_preview():
  canvas = Image.new('RGB', (630, 630), color=(255,255,255))
  
  try:
      bg = request.args['bg']
      im_bg = Image.open(f'api/static/bg/{bg}')
      im_bg = im_bg.convert('RGBA')
      canvas.paste(im_bg, (0,0))
  except:
      pass
  try:
      skin = request.args['skin']
      im_skin = Image.open(f'api/static/skin/{skin}')
      im_skin =im_skin.convert('RGBA')
      canvas.paste(im_skin, (0,0), im_skin)
  except:
      pass
  try:
      cloth = request.args['cloth']
      im_cloth = Image.open(f'api/static/cloth/{cloth}')
      im_cloth = im_cloth.convert('RGBA')
      canvas.paste(im_cloth, (0,0), im_cloth)
  except:
      pass
  try:
      hair = request.args['hair']
      im_hair = Image.open(f'api/static/hair/{hair}')
      im_hair = im_hair.convert('RGBA')
      canvas.paste(im_hair, (0,0), im_hair)
  except:
      pass
  try:
      eyes = request.args['eyes']
      im_eyes = Image.open(f'api/static/eyes/{eyes}')
      im_eyes = im_eyes.convert('RGBA')
      canvas.paste(im_eyes, (0,0), im_eyes)
  except:
      pass
  try:
      eyesplus = request.args['eyesplus']
      im_eyesplus = Image.open(f'api/static/eyesplus/{eyesplus}')
      im_eyesplus = im_eyesplus.convert('RGBA')
      canvas.paste(im_eyesplus, (0,0), im_eyesplus)
  except:
      pass
  try:
      mouth = request.args['mouth']
      im_mouth = Image.open(f'api/static/mouth/{mouth}')
      im_mouth = im_mouth.convert('RGBA')
      canvas.paste(im_mouth, (0,0), im_mouth)
  except:
      pass
  try:
      plus = request.args['plus']
      im_plus = Image.open(f'api/static/plus/{plus}')
      im_plus = im_plus.convert('RGBA')
      canvas.paste(im_plus, (0,0), im_plus)
  except:
      pass
  
  buffered = BytesIO()
  canvas.save(buffered, format="PNG")
  buffered.seek(0)
  return send_file(buffered, mimetype='image/png')
    
if __name__ == '__main__':
    app.run(debug=True)