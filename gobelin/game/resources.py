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
	
# images
title = pyglet.resource.image("title.png")
dirt = pyglet.resource.image("dirt.png")
cursor = pyglet.resource.image("cursor.png")
block = pyglet.resource.image("block.png")
magic_w = pyglet.resource.image("magic-w.png")

# fonts