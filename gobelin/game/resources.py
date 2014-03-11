from random import choice

import pyglet

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()

# image tools
def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2
    return image

def uncenter_image(image):
    image.anchor_x = 0
    image.anchor_y = 0
    return image
	
# IMAGES
# backgrounds
title = pyglet.resource.image("title.png")

# art
unitp00 = pyglet.resource.image("unitp00.png") # a caryatid's face
unitp01 = pyglet.resource.image("unitp01.png") # a cycladic figurine's portrait
unitp10 = pyglet.resource.image("unitp10.png") # a mouth and jaw from bosch
unitp11 = pyglet.resource.image("unitp11.png") # and one of his craven birds

## STATIC TILES | image grids
bottomless_pit = pyglet.image.load("../resources/-bottomless-pit.png")
bmpt_tiles = pyglet.image.ImageGrid(bottomless_pit, 4, 4)
# ground & fog
dirt = pyglet.resource.image("dirt.png")
mist = pyglet.resource.image("mist.png")
dark = pyglet.resource.image("dark.png")
# wall
brick = pyglet.resource.image("brick.png")
brk_t = pyglet.resource.image("brk-tp.png")
brk_c = pyglet.resource.image("brk-cp.png")
pillar = pyglet.resource.image("pillar.png")
# impassable
water = pyglet.resource.image("water.png")
bmpt_RIG = bmpt_tiles[0]
bmpt_SWC = bmpt_tiles[1]
bmpt_SEC = bmpt_tiles[2]
bmpt_BOT = bmpt_tiles[3]
bmpt_LEF = bmpt_tiles[4]
bmpt_NWC = bmpt_tiles[5]
bmpt_NEC = bmpt_tiles[6]
bmpt_TOP = bmpt_tiles[7]
bmpt_SEE = bmpt_tiles[8]
bmpt_EAR = bmpt_tiles[9]
bmpt_YOU = bmpt_tiles[10]
bmpt_RCH = bmpt_tiles[11]
bmpt_4SD = bmpt_tiles[12]
bmpt_ZSD = bmpt_tiles[13]
bmpt_PIT = bmpt_tiles[14]
bmpt_TUN = bmpt_tiles[15]
bmpt_lookup = {0b0000: bmpt_4SD,
               0b0001: bmpt_EAR,
               0b0010: bmpt_RCH,
               0b0011: bmpt_NEC,
               0b0100: bmpt_SEE,
               0b0101: bmpt_TUN,
               0b0110: bmpt_NWC,
               0b0111: bmpt_TOP,
               0b1000: bmpt_YOU,
               0b1001: bmpt_SEC,
               0b1010: bmpt_PIT,
               0b1011: bmpt_RIG,
               0b1100: bmpt_SWC,
               0b1101: bmpt_BOT,
               0b1110: bmpt_LEF,
               0b1111: bmpt_ZSD}
# usable
block = pyglet.resource.image("block.png")

# unit tiles
cursor = pyglet.resource.image("cursor.png")
magic_w = pyglet.resource.image("magic-w.png")
hemry = pyglet.resource.image("hemry.png")
goblin = pyglet.resource.image("goblin.png")
shadow = pyglet.resource.image("shadow.png")
sshadw = pyglet.resource.image("small_shdw.png")
flame = pyglet.resource.image("flame.png")

## MOVER TILES | image grids
gombroon_pottery = pyglet.image.load("../resources/gombroon.png")
box_tiles = pyglet.image.ImageGrid(gombroon_pottery, 2, 2)
# box
box_1 = box_tiles[0]
box_2 = box_tiles[1]
box_3 = box_tiles[2]
box_4 = box_tiles[3]
box_lookup = {'dinos':    box_1,
              'ewer':     box_2,
              'psykter':  box_3,
              'lekythos': box_4}
def random_box():
    return choice(box_lookup.values())
# torch | static
torch = pyglet.resource.image("torch.png")
    
# other
default = pyglet.resource.image("default.png")
empty = pyglet.resource.image("empty.png")

# cursor tiles
target = pyglet.resource.image("target.png")
select = pyglet.resource.image("select.png")
rslect = pyglet.resource.image("rslect.png")
bslect = pyglet.resource.image("bslect.png")

### DOODADS
## SUPERMARKET | image grids
supermarket = pyglet.image.load("../resources/-supermarket.png")
spmkt_tiles = pyglet.image.ImageGrid(supermarket, 8, 8)
supermarket_fog = pyglet.image.load("../resources/-supermarket-fog.png")
smfog_tiles = pyglet.image.ImageGrid(supermarket_fog, 8, 8)
supermarket_sign = pyglet.image.load("../resources/-supermarket-sign.png")
smsign_tiles = pyglet.image.ImageGrid(supermarket_sign, 8, 8)
# fog

# FONTS