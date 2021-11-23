from flask import Flask, abort
from flask import jsonify
from google.cloud import storage
from google.oauth2 import service_account
import numpy as np
from PIL import Image
import os
import mimetypes

GOOGLE_STORAGE_BASE = os.environ['GOOGLE_STORAGE_BASE']
GOOGLE_STORAGE_PROJECT = os.environ['GOOGLE_STORAGE_PROJECT']
GOOGLE_STORAGE_BUCKET = os.environ['GOOGLE_STORAGE_BUCKET']
ASSETFOLDER = GOOGLE_STORAGE_BASE + GOOGLE_STORAGE_BUCKET + '/Assets/'

app = Flask(__name__)

########################################################################
# Data
########################################################################

# GetYourKicks - HiTops

def generateRandomNumber(lowIn, highIn):
    rng = np.random.randint(lowIn, highIn)
    return rng

# Side Panels - Required in all designs
sidePanelDict = {
    1: 'Blue Flowers',
    2: 'Blue Stripes',
    3: 'Giraffe',
    4: 'Green Stripes',
    5: 'Green Swirls',
    6: 'Leopard',
    7: 'Pink Arc',
    8: 'Red Flowers',
    9: 'Zebra'
}

# Soles - Required in all designs
soleDict = {
    1: 'Style 1 - Grey Fade',
    2: 'Style 1 - White',
    3: 'Style 2 - Purple',
    4: 'Style 2 - Yellow'
}

# SubSoles - Required in all designs, split based on matching Sole type
subSoleDict = {
    1: 'Style 1 - Blue',
    2: 'Style 1 - Green',
    3: 'Style 1 - Red',
    4: 'Style 2 - Blue',
    5: 'Style 2 - Green'
}

# Laces - Required in all designs
lacesDict = {
    1: '3D',
    2: 'Black',
    3: 'Neon Yellow',
    4: 'Rainbow',
    5: 'Red'
}

# Tongues - Required in all designs
tongueDict = {
    1: 'Style 1 - Blue',
    2: 'Style 1 - Giraffe',
    3: 'Style 1 - Green',
    4: 'Style 1 - Leopard',
    5: 'Style 1 - Shiny Red',
    6: 'Style 1 - Zebra',
    7: 'Style 2 - Blue',
    8: 'Style 2 - Denim',
    9: 'Style 2 - Purple',
    10: 'Style 2 - Rainbow',
    11: 'Style 2 - Yellow',
    12: 'Style 2 - Zebra'
}

# Toe Lowers - Optional element
toeLowerDict = {
    1: 'Blue Speckle',
    2: 'Denim',
    3: 'Giraffe',
    4: 'Leopard',
    5: 'Purple',
    6: 'Zebra'
}

# Toe Uppers - Optional element
toeUpperDict = {
    1: 'Giraffe',
    2: 'Grey Suede',
    3: 'Leopard',
    4: 'Zebra'
}

# Lace Surrounds - Optional element
lacesSurroundDict = {
    1: 'Blue',
    2: 'Giraffe',
    3: 'Green Crackle',
    4: 'Leopard',
    5: 'Pink',
    6: 'Zebra'
}

# Ankles - Optional element
ankleDict = {
    1: 'Black',
    2: 'Blue',
    3: 'Giraffe',
    4: 'Leopard',
    5: 'Purple Crackle',
    6: 'Zebra'
}

# Heels - Optional element
heelDict = {
    1: 'Style 1 - Blue',
    2: 'Style 1 - Giraffe',
    3: 'Style 1 - Leopard',
    4: 'Style 1 - Zebra',
    5: 'Style 2 - Green Crackle',
    6: 'Style 2 - Leopard',
    7: 'Style 2 - Shiny Red'
}

# Decorations - Optional element
decorationDict = {
    1: 'Black Heel Smiley',
    2: 'Gold Heel Fleur De Lis',
    3: 'Toe Vents',
    4: 'White Heel FLower',
    5: 'Sole Bubble'
}

# contractURI() support

# ToDo: correct image and external_link values below
CONTRACT_URI_METADATA = {
    'getyourkicks-hitops': {
        'name': 'GetYourKicks HiTops',
        'description': 'Hi-top kicks for the metaverse.',
        'image': 'https://example.com/image.png',
        'external_link': 'https://github.com/ProjectOpenSea/opensea-creatures/'
    }
}
CONTRACT_URI_METADATA_AVAILABLE = CONTRACT_URI_METADATA.keys()


########################################################################
# Routes
########################################################################

# getyourkicks-hitops

@app.route('/api/hitop/<token_id>')
def hitop(token_id):
    token_id = int(token_id)

    # Init counters for various stats
    statAnimalInstinct = 0
    statBreathability = 0
    statJumpBoost = 0
    statLaceSpeedBoost = 0

    # Side Panels - Required in all designs
    sidePanel = generateRandomNumber(1, 9)
    strSidePanel = sidePanelDict[sidePanel]
    strSidePanelFile = strSidePanel.replace(" ", "")
    if (sidePanel == 3 or sidePanel == 6 or sidePanel == 9) :
        statAnimalInstinct = statAnimalInstinct + 1

    # Soles - Required in all designs
    sole = generateRandomNumber(1, 4)
    strSole = soleDict[sole]
    strSoleFile = strSole.replace(" ", "")

    # SubSoles - Required in all designs, split based on matching Sole type
    if (sole < 3) :
        subSole = generateRandomNumber(1, 3)
    else :
        subSole = generateRandomNumber(4, 5)

    strSubSole = subSoleDict[subSole]
    strSubSoleFile = strSubSole.replace(" ", "")

    # Laces - Required in all designs
    laces = generateRandomNumber(1, 5)
    strLaces = lacesDict[laces]
    strLacesFile = strLaces.replace(" ", "")

    # Tongues - Required in all designs
    tongue = generateRandomNumber(1, 12)
    strTongue = tongueDict[tongue]
    strTongueFile = strTongue.replace(" ", "")
    if (tongue == 2 or tongue == 4 or tongue == 6 or tongue == 12) :
        statAnimalInstinct = statAnimalInstinct + 1

    # Toe Lowers - Optional element
    toeLower = generateRandomNumber(1, 12)
    strToeLower = ""
    if (toeLower < 7) :
        strToeLower = toeLowerDict[toeLower]
        strToeLowerFile = strToeLower.replace(" ", "")
        if (toeLower == 3 or toeLower == 4 or toeLower == 6) :
            statAnimalInstinct = statAnimalInstinct + 1

    # Toe Uppers - Optional element
    toeUpper = generateRandomNumber(1, 20)
    strToeUpper = ""
    if (toeUpper < 5) :
        strToeUpper = toeUpperDict[toeUpper]
        strToeUpperFile = strToeUpper.replace(" ", "")
        if (toeUpper == 1 or toeUpper == 3 or toeUpper == 4) :
            statAnimalInstinct = statAnimalInstinct + 1

    # Lace Surrounds - Optional element
    lacesSurround = generateRandomNumber(1, 8)
    strLacesSurround = ""
    if (lacesSurround < 7) :
        strLacesSurround = lacesSurroundDict[lacesSurround]
        strLacesSurroundFile = strLacesSurround.replace(" ", "")
        if (lacesSurround == 2 or lacesSurround == 4 or lacesSurround == 6) :
            statAnimalInstinct = statAnimalInstinct + 1

    # Ankles - Optional element
    ankle = generateRandomNumber(1, 9)
    strAnkle = ""
    if (ankle < 7) :
        strAnkle = ankleDict[ankle]
        strAnkleFile = strAnkle.replace(" ", "")
        if (ankle == 3 or ankle == 4 or ankle == 6) :
            statAnimalInstinct = statAnimalInstinct + 1

    # Heels - Optional element
    heel = generateRandomNumber(1, 12)
    strHeel = ""
    if (heel < 8) :
        strHeel = heelDict[heel]
        strHeelFile = strHeel.replace(" ", "")
        if (heel == 2 or heel == 3 or heel == 4 or heel == 6) :
            statAnimalInstinct = statAnimalInstinct + 1

    # Decorations - Optional element
    decoration = generateRandomNumber(1, 20)
    strDecoration = ""
    if (decoration < 7) :
        strDecoration = decorationDict[decoration]
        strDecorationFile = strDecoration.replace(" ", "")

    # Open Required pngs in respective folders
    imgSidePanel = Image.open(ASSETFOLDER + "Side Panels/" + strSidePanelFile + ".png")
    imgSole = Image.open(ASSETFOLDER + "Soles/" + strSoleFile + ".png")
    imgSubSole = Image.open(ASSETFOLDER + "Sub Soles/" + strSubSoleFile + ".png")
    imgLaces = Image.open(ASSETFOLDER + "Laces/" + strLacesFile + ".png")
    imgTongue = Image.open(ASSETFOLDER + "Tongues/" + strTongueFile + ".png")
    imgLaceHoles = Image.open(ASSETFOLDER + "Lace Holes/LaceHoles.png")
    imgSidePanel = imgSidePanel.convert("RGBA")
    imgSole = imgSole.convert("RGBA")
    imgSubSole = imgSubSole.convert("RGBA")
    imgLaces = imgLaces.convert("RGBA")
    imgTongue = imgTongue.convert("RGBA")
    imgLaceHoles = imgLaceHoles.convert("RGBA")

    # Paste/Merge Required PNGs, as layers on base, paying attention to ordering for desired overlap
    # Start building the design with the side panel as base layer
    currentHiTop = imgSidePanel.copy()

    # Attach the main sole layer
    currentHiTop.paste(imgSole, (0, 0), mask=imgSole)

    # If there is a toe upper layer, add it next
    if (toeUpper < 5) :
        imgToeUpper = Image.open(ASSETFOLDER + "Toe Uppers/" + strToeUpperFile + ".png")
        imgToeUpper = imgToeUpper.convert("RGBA")
        currentHiTop.paste(imgToeUpper, (0, 0), mask=imgToeUpper)

    # If there is a toe lower layer, add it layered above any toe upper
    if (toeLower < 7) :
        imgToeLower = Image.open(ASSETFOLDER + "Toe Lowers/" + strToeLowerFile + ".png")
        imgToeLower = imgToeLower.convert("RGBA")
        currentHiTop.paste(imgToeLower, (0, 0), mask=imgToeLower)

    # Add the tongue before laces, et al.
    currentHiTop.paste(imgTongue, (0, 0), mask=imgTongue)

    # If there is an ankle layer, add it so it will position beneath any laces surround layer
    if (ankle < 7) :
        imgAnkle = Image.open(ASSETFOLDER + "Ankles/" + strAnkleFile + ".png")
        imgAnkle = imgAnkle.convert("RGBA")
        currentHiTop.paste(imgAnkle, (0, 0), mask=imgAnkle)

    # If there is a laces surround, add it before lace holes
    if (lacesSurround < 7) :
        imgLacesSurround = Image.open(ASSETFOLDER + "Lace Surrounds/" + strLacesSurroundFile + ".png")
        imgLacesSurround = imgLacesSurround.convert("RGBA")
        currentHiTop.paste(imgLacesSurround, (0, 0), mask=imgLacesSurround)

    # Add the lace holes
    currentHiTop.paste(imgLaceHoles, (0, 0), mask=imgLaceHoles)

    # Add the laces on top of the lace holes
    currentHiTop.paste(imgLaces, (0, 0), mask=imgLaces)

    # If there is a heel layer, add it so tall variants cover any ankle element at top back
    if (heel < 8) :
        imgHeel = Image.open(ASSETFOLDER + "Heels/" + strHeelFile + ".png")
        imgHeel = imgHeel.convert("RGBA")
        currentHiTop.paste(imgHeel, (0, 0), mask=imgHeel)

    # Add the subsole so tall variants cover any heel element
    currentHiTop.paste(imgSubSole, (0, 0), mask=imgSubSole)

    # Add decorations last
    if (decoration < 6) :
        imgDecoration = Image.open(ASSETFOLDER + "Decorations/" + strDecorationFile + ".png")
        imgDecoration = imgDecoration.convert("RGBA")
        currentHiTop.paste(imgDecoration, (0, 0), mask=imgDecoration)

    # Resize image to OpenSea market recommended size - "Resample Nearest" to retain resolution
    #resized_img = img0.resize((300, 300), resample=Image.NEAREST)
    currentHiTop.save('G:/My Drive/Artwork/NFT/JustForKicks/HiTops/Generated/' + 'Test_0006' + '.png', "PNG")

    image_url = _compose_image(['images/bases/base-%s.png' % base,
                                'images/eyes/eyes-%s.png' % eyes,
                                'images/mouths/mouth-%s.png' % mouth],
                               token_id)

    attributes = []
    _add_attribute(attributes, 'Side Panel', strSidePanel, token_id)
    _add_attribute(attributes, 'Sole', strSole, token_id)
    _add_attribute(attributes, 'SubSole', strSubSole, token_id)
    _add_attribute(attributes, 'Laces', strLaces, token_id)
    _add_attribute(attributes, 'Tongue', strTongue, token_id)

    if (strLacesSurround != "") :
        _add_attribute(attributes, 'Lace Surround', strLacesSurround, token_id)

    if (strToeUpper != "") :
        _add_attribute(attributes, 'Toe Upper', strToeUpper, token_id)

    if (strToeLower != "") :
        _add_attribute(attributes, 'Toe Lower', strToeLower, token_id)

    if (strAnkle != "") :
        _add_attribute(attributes, 'Ankle', strAnkle, token_id)

    if (strHeel != "") :
        _add_attribute(attributes, 'Heel', strHeel, token_id)

    if (strDecoration != "") :
        _add_attribute(attributes, 'Decoration', strDecoration, token_id)

    # ToDo: Correct external_url and image_url
    return jsonify({
        'name': 'HiTop Style #%s' % token_id,
        'description': 'Funky and unique hi-top style kickin\' it in the metaverse.',
        'image': image_url,
        'external_url': 'https://getyourkicks.assemblystudio.com/%s' % token_id,
        'attributes': attributes
    })

@app.route('/api/factory/hitop/<token_id>')
def hitop_factory(token_id):
    token_id = int(token_id)
    if token_id == 0:
        name = 'One GetYourKicks HiTop'
        description = 'When you purchase this, you will receive a single, freshly generated GetYourKicks HiTop of a random style. ' \
                      'Enjoy, and rock your Hi-Top in all its fabulous glory!'
        image_url = _compose_image(['images/factory/shoebox.png'], token_id, 'factory')
        num_inside = 1

    attributes = []
    _add_attribute(attributes, 'number_inside', [num_inside], token_id)

    return jsonify({
        'name': name,
        'description': description,
        'image': image_url,
        'external_url': 'https://getyourkicks.assemblystudio.com/%s' % token_id,
        'attributes': attributes
    })

# contractURI()

@app.route('/contract/<contract_name>')
def contract_uri(contract_name):
    if not contract_name in CONTRACT_URI_METADATA_AVAILABLE:
        abort(404, description='Resource not found')
    return jsonify(CONTRACT_URI_METADATA[contract_name])


# Error handling

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


########################################################################
# Utility code
########################################################################

def _add_attribute(existing, attribute_name, options, token_id, display_type=None):
    trait = {
        'trait_type': attribute_name,
        'value': options[token_id % len(options)]
    }
    if display_type:
        trait['display_type'] = display_type
    existing.append(trait)


def _compose_image(image_files, token_id, path='hitop'):
    composite = None
    for image_file in image_files:
        foreground = Image.open(image_file).convert('RGBA')

        if composite:
            composite = Image.alpha_composite(composite, foreground)
        else:
            composite = foreground

    output_path = 'images/output/%s.png' % token_id
    composite.save(output_path)

    blob = _get_bucket().blob(f'{path}/{token_id}.png')
    blob.upload_from_filename(filename=output_path)
    return blob.public_url


def _bucket_image(image_path, token_id, path='accessory'):
    blob = _get_bucket().blob(f'{path}/{token_id}.png')
    blob.upload_from_filename(filename=image_path)
    return blob.public_url


def _get_bucket():
    credentials = service_account.Credentials.from_service_account_file('credentials/google-storage-credentials.json')
    if credentials.requires_scopes:
        credentials = credentials.with_scopes(['https://www.googleapis.com/auth/devstorage.read_write'])
    client = storage.Client(project=GOOGLE_STORAGE_PROJECT, credentials=credentials)
    return client.get_bucket(GOOGLE_STORAGE_BUCKET)


########################################################################
# Main flow of execution
########################################################################

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
