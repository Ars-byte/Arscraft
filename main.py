from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(title='Arscraft :b')

window.title = "Arscraft :b"
window.borderless = False
window.fullscreen = False
window.color = color.azure
window.fps_counter.enabled = True

Entity.default_shader = 'unlit'

grass_tex = load_texture('assets/grass_block.png') or 'grass'
stone_tex = load_texture('assets/stone_block.png') or 'stone'
brick_tex = load_texture('assets/brick_block.png') or 'brick'
dirt_tex  = load_texture('assets/dirt_block.png') or 'dirt'
arm_tex   = load_texture('assets/arm_texture.png') or 'white_cube'
sky_box_tex = load_texture('assets/skybox.png')

textures = {1: grass_tex, 2: stone_tex, 3: brick_tex, 4: dirt_tex}
block_pick = 1

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=grass_tex):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=texture,
            color=color.white,
            origin_y=0.5,
            collider='box',
            shader='unlit',
            highlight_color=color.lime
        )

chunk_size = 16
render_distance = 5
chunks = {}

def create_chunk(cx, cz):
    chunk = Entity(
        model='plane',
        x=cx * chunk_size + chunk_size/2 - 0.5,
        z=cz * chunk_size + chunk_size/2 - 0.5,
        y=0,
        scale=chunk_size,
        texture=grass_tex,
        collider='box',
        shader='unlit'
    )
    chunk.texture_scale = (chunk_size, chunk_size)
    return chunk

def update_world():
    px = int(player.x // chunk_size)
    pz = int(player.z // chunk_size)

    for rz in range(pz - render_distance, pz + render_distance):
        for rx in range(px - render_distance, px + render_distance):
            if (rx, rz) not in chunks:
                chunks[(rx, rz)] = create_chunk(rx, rz)

hotbar = Entity(parent=camera.ui, model='quad', scale=(0.4, 0.08), position=(0, -0.45), color=color.black66)
selector = Entity(parent=hotbar, model='quad', color=color.rgba(255,255,255,100), scale=(0.22, 1.1), position=(-0.37, 0), z=-0.1)

for i in range(4):
    Entity(parent=hotbar, model='quad', texture=textures[i+1], scale=(0.18, 0.8), position=(-0.37 + (i * 0.25), 0), z=-0.2)

def update_hotbar():
    selector.x = -0.37 + ((block_pick - 1) * 0.25)

def input(key):
    global block_pick
    
    if key in ('1', '2', '3', '4'):
        block_pick = int(key)
        update_hotbar()

    if key == 'left mouse down':
        if mouse.hovered_entity:
            p = mouse.world_point + mouse.normal * 0.5
            Voxel(position=(round(p.x), round(p.y), round(p.z)), texture=textures[block_pick])

    if key == 'right mouse down':
        if mouse.hovered_entity and isinstance(mouse.hovered_entity, Voxel):
            destroy(mouse.hovered_entity)

def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.position = Vec2(0.5, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)
    
    if int(player.x) % 5 == 0:
        update_world()

player = FirstPersonController(y=2, origin_y=-0.5)
player.cursor.color = color.red
player.cursor.scale = 0.02

hand = Entity(
    parent=camera.ui, 
    model='cube', 
    texture=arm_tex, 
    color=color.orange, 
    scale=(0.2, 0.4, 0.2), 
    rotation=Vec3(150,-10,0), 
    position=Vec2(0.6,-0.6),
    shader='unlit'
)

sky = Sky(texture=sky_box_tex)

update_world()

window.title = "Arscraft :b"
app.run()