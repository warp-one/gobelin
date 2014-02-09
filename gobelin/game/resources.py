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

# static tiles
dirt = pyglet.resource.image("dirt.png")
block = pyglet.resource.image("block.png")
water = pyglet.resource.image("water.png")

# unit tiles
cursor = pyglet.resource.image("cursor.png")
magic_w = pyglet.resource.image("magic-w.png")
goblin = pyglet.resource.image("goblin.png")

# mover tiles
default = pyglet.resource.image("default.png")
box = pyglet.resource.image("box.png")

# FONTS