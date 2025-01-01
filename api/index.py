from flask import Flask, render_template, request, send_file, redirect, jsonify, url_for
from PIL import Image
import os
from io import BytesIO
import sqlite3


# Create table if not exists
conn = sqlite3.connect('blog.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY, 
                title TEXT,
                body TEXT, 
                slug TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                image TEXT
            )''')
conn.commit()
conn.close()


app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load component images from folders
SKIN_IMAGES = []
for f in os.listdir('./api/static/skin'):
    if f.endswith('.png'):
        SKIN_IMAGES.append(f)

CLOTH_IMAGES = []  
for f in os.listdir('./api/static/cloth'):
    if f.endswith('.png'):
        CLOTH_IMAGES.append(f)

CAPES_IMAGES = []  
for f in os.listdir('./api/static/capes'):
    if f.endswith('.png'):
        CAPES_IMAGES.append(f)
  
HAIR_IMAGES = []
for f in os.listdir('./api/static/hair'):
    if f.endswith('.png'):
        HAIR_IMAGES.append(f)

SHIRT_IMAGES = []
for f in os.listdir('./api/static/shirt'):
    if f.endswith('.png'):
        SHIRT_IMAGES.append(f)

HAIR_PLUS = []
for f in os.listdir('./api/static/hairplus'):
    if f.endswith('.png'):
        HAIR_PLUS.append(f)

HAT_IMAGES = []
for f in os.listdir('./api/static/hat'):
    if f.endswith('.png'):
        HAT_IMAGES.append(f)

BG_IMAGES = []
for f in os.listdir('./api/static/bg'):
    if f.endswith('.png'):
        BG_IMAGES.append(f)
 
EYES_IMAGES = []
for f in os.listdir('./api/static/eyes'):
    if f.endswith('.png'):
        EYES_IMAGES.append(f)

PANTS_IMAGES = []
for f in os.listdir('./api/static/pants'):
    if f.endswith('.png'):
        PANTS_IMAGES.append(f)        

SHOES_IMAGES = []
for f in os.listdir('./api/static/shoes'):
    if f.endswith('.png'):
        SHOES_IMAGES.append(f)        

MOUTH_IMAGES = []
for f in os.listdir('./api/static/mouth'):
    if f.endswith('.png'):
        MOUTH_IMAGES.append(f)      

PLUS = []
for f in os.listdir('./api/static/plus'):
    if f.endswith('.png'):
        PLUS.append(f)

def create_post(title, body, slug, image):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (title, body, slug, image) VALUES (?, ?, ?, ?)", 
              (title, body, slug, image))
    conn.commit()
        

# Homepage
@app.route('/')
def index():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT title, body, slug, image FROM posts ORDER BY date DESC LIMIT 3')
    posts = c.fetchall()
    print(posts)
    return render_template('v2.html', posts=posts)

# All Posts
@app.route('/blog')    
def blog():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT title, body, slug, date, image FROM posts ORDER BY date DESC')
    posts = c.fetchall()
    return render_template('blog.html', posts=posts)

# Single Post 
@app.route('/blog/<slug>')
def post(slug):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT title, body, date, image FROM posts WHERE slug="%s"' % slug)
    post = c.fetchone()
    return render_template('post.html', post=post)


# Editor route for v2         
@app.route('/editor')
def v2editor():
    return render_template('v2editor.html', 
        skin_images=SKIN_IMAGES,
        cloth_images=CLOTH_IMAGES,
        hair_images=HAIR_IMAGES,
        bg_images = BG_IMAGES,
        eyes_images = EYES_IMAGES,
        shoes_images = SHOES_IMAGES,
        pants_images = PANTS_IMAGES,
        mouth_images=MOUTH_IMAGES,
        hair_plus=HAIR_PLUS,
        hat_images=HAT_IMAGES,
        shirt_images=SHIRT_IMAGES,
        capes_images=CAPES_IMAGES,
        plus = PLUS
    )

@app.route('/v2/<string:v2_redirect>')
def v2redirect(v2_redirect):
    return redirect(f'/{v2_redirect}')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save the file to a directory of your choice
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    return f"{UPLOAD_FOLDER}/{file.filename}"

  
# Render preview route
@app.route('/render_preview', methods=['POST'])
def render_preview():
    
    canvas = Image.new('RGB', (512, 512), color=(255,255,255))
    data = request.get_json()
    # Here you can process the received data as needed
    print(data)

    
    try:
        bg = data['bg']
        if 'uploads' in bg:
            im_bg = Image.open(bg)
            im_bg = im_bg.convert('RGBA')
            im_bg.resize((512,512))
        else:
            im_bg = Image.open(f'./api/static/bg/{bg}')
            im_bg = im_bg.convert('RGBA')
            
        canvas.paste(im_bg, (0,0), im_bg)
    except:
        pass
    try:
        im_cape = Image.open(f"./api/static/capes/{data['capes']}").convert('RGBA')
        canvas.paste(im_cape, (0,0), im_cape)
    except:
        pass
    try:
        skin = data['skin']
        if 'uploads' in skin:
            im_skin = Image.open(skin)
            im_skin = im_skin.convert('RGBA')
            im_skin.resize((512,512))
        else:
            im_skin = Image.open(f'./api/static/skin/{skin}')
            im_skin =im_skin.convert('RGBA')
        
        canvas.paste(im_skin, (0,0), im_skin)
    except:
        pass
    
    try:
        hair = data['hair']
        im_hair = Image.open(f'./api/static/hair/{hair}')
        im_hair = im_hair.convert('RGBA')
        canvas.paste(im_hair, (0,0), im_hair)
    except:
        pass
    try:
        eyes = data['eyes']
        im_eyes = Image.open(f'./api/static/eyes/{eyes}')
        im_eyes = im_eyes.convert('RGBA')
        canvas.paste(im_eyes, (0,0), im_eyes)
    except:
        pass
    try:
        shirt = data['shirt']
        im_shirt = Image.open(f'./api/static/shirt/{shirt}')
        im_shirt = im_shirt.convert('RGBA')
        canvas.paste(im_shirt, (0,0), im_shirt)
    except:
        pass
    try:
        pants = data['pants']
        im_pants = Image.open(f'./api/static/pants/{pants}')
        im_pants = im_pants.convert('RGBA')
        canvas.paste(im_pants, (0,0), im_pants)
    except:
        pass
    try:
        shoes = data['shoes']
        im_shoes = Image.open(f'./api/static/shoes/{shoes}')
        im_shoes = im_shoes.convert('RGBA')
        canvas.paste(im_shoes, (0,0), im_shoes)
    except:
        pass
    try:
        cloth = data['cloth']
        im_cloth = Image.open(f'./api/static/cloth/{cloth}')
        im_cloth = im_cloth.convert('RGBA')
        canvas.paste(im_cloth, (0,0), im_cloth)
    except:
        pass
    try:
        mouth = data['mouth']
        im_mouth = Image.open(f'./api/static/mouth/{mouth}')
        im_mouth = im_mouth.convert('RGBA')
        canvas.paste(im_mouth, (0,0), im_mouth)
    except:
        pass
    try:
        hat = data['hat']
        im_hat = Image.open(f'./api/static/hat/{hat}')
        im_hat = im_hat.convert('RGBA')
        canvas.paste(im_hat, (0,0), im_hat)
    except:
        pass
    try:
        hairplus = data['hairplus']
        im_hairplus = Image.open(f'./api/static/hairplus/{hairplus}')
        im_hairplus = im_hairplus.convert('RGBA')
        canvas.paste(im_hairplus, (0,0), im_hairplus)
    except:
        pass
    try:
        plus = data['plus']
        im_plus = Image.open(f'./api/static/plus/{plus}')
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
