from utils.scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-1, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4))
scene.set_directional_light((1, 1, -1), 0.2, (0.1, 0.1, 0.1))
# scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))

@ti.func
def create_block(pos, size, color, color_noise=vec3(0.0), lt=1):
    for I in ti.grouped(
        ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]), (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, lt, color + color_noise * ti.random())

@ti.func
def create_light(pos, size):
    create_block(pos, size, vec3(1, 1, 1), vec3(0.0), 2)

@ti.func
def music_note(pos, color):
    for i in range(5):
        scene.set_voxel(ivec3(pos[0], pos[1]+i, pos[2]), 2, color)
        scene.set_voxel(ivec3(pos[0], pos[1]+5, pos[2]+i), 2, color)
        scene.set_voxel(ivec3(pos[0], pos[1]+i, pos[2]+5), 2, color)
    scene.set_voxel(ivec3(pos[0], pos[1]+5, pos[2]+5), 2, color)
    scene.set_voxel(ivec3(pos[0], pos[1], pos[2]+1), 2, color)
    scene.set_voxel(ivec3(pos[0], pos[1], pos[2]+6), 2, color)

@ti.func
def make_round(pos, rad, thickness, color, color_noise):
    xrange = [pos[0] - rad, pos[0] + rad]
    yrange = [pos[1] - rad, pos[1] + rad]
    for I in ti.grouped(ti.ndrange((xrange[0], xrange[1]), (yrange[0], yrange[1]), (pos[2], pos[2] + thickness))):
        if (I[0] - pos[0])**2 + (I[1] - pos[1])**2 <= rad**2:
            scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.func
def make_round2(pos, rad, thickness, color, color_noise):
    xrange = [pos[0] - rad, pos[0] + rad]
    yrange = [pos[2] - rad, pos[2] + rad]
    for I in ti.grouped(ti.ndrange((xrange[0], xrange[1]), (pos[1], pos[1] + thickness), (yrange[0], yrange[1]))):
        if (I[0] - pos[0])**2 + (I[2] - pos[2])**2 <= rad**2:
            scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.kernel
def initialize_voxels():
    for i in range(2):
        create_block(ivec3(-64, -64 + i, -64), ivec3(123, 2, 123), vec3(0.8, 0.6, 0.1), vec3(0.3)) # Base
        make_round(ivec3(-15, i*24 - 40, 30), 20 - 6*i, 10, vec3(0.5, 0.3, 0.3), vec3(0.05)) # guitar body
        create_block(ivec3(2 + 16*i, 10, -3), ivec3(10, 6, 6), vec3(1, 1, 1), vec3(0.01)) # 鼓架
        make_round2(ivec3(-5 + i*40, 10, -3), 14, 10, vec3(0.2, 0.3, 0.2), vec3(0.01)) # tom drum
        make_round2(ivec3(-5 + i*40, 19, -3), 12, 1, vec3(1, 1, 1), vec3(0.01)) # tom drum2
    create_block(ivec3(-18, -12, 36), ivec3(6, 40, 4), vec3(0.5, 0.4, 0.4), vec3(0.01)) # guitar neck
    create_block(ivec3(-19, 28, 36), ivec3(8, 13, 4), vec3(0.5, 0.3, 0.3), vec3(0.01)) # guitar neck2
    create_block(ivec3(-21, -35, 35), ivec3(12, 2, 5), vec3(0.1, 0.1, 0.1), vec3(0.01)) # guitar pillow
    make_round(ivec3(-15, -22, 35), 5, 5, vec3(0.1, 0.1, 0.1), vec3(0.0)) # hole
    make_round(ivec3(13, -30, -25), 32, 20, vec3(0.2, 0.3, 0.2), vec3(0.0)) # kick drum1
    make_round(ivec3(13, -30, -4), 30, 1, vec3(0.8, 0.9, 0.9), vec3(0.0)) # kick drum2
    create_block(ivec3(12, 6, -3), ivec3(6, 10, 6), vec3(1, 1, 1), vec3(0.01)) # 鼓架
    make_round2(ivec3(45, -10, -30), 14, 10, vec3(0.2, 0.3, 0.2), vec3(0.0)) # snare
    make_round2(ivec3(45, -1, -30), 12, 1, vec3(1, 1, 1), vec3(0.0)) # snare2
    create_block(ivec3(45, -60, -30), ivec3(2, 50, 2), vec3(1., 1., 1.), vec3(0.0)) # snare3
    make_round2(ivec3(-35, -50, -27), 18, 35, vec3(0.2, 0.3, 0.2), vec3(0.0)) # floor tom
    make_round2(ivec3(-35, -16, -27), 16, 1, vec3(1, 1, 1), vec3(0.0)) # floor tom2
    for i in range(40):
        if i == 0 or i == 39:
            create_light(ivec3(30, -60+i, 40-i//2), ivec3(20, 1, 1))
        else:
            create_block(ivec3(30, -60+i, 40-i//2), ivec3(20, 1, 1), vec3(0.0, 0.0, 0.0), vec3(0.01)) # ad-plate
    for i in range(8):
        create_block(ivec3(-55+i*16, -62, 58), ivec3(2, 120, 1), vec3(0.3, 0.3, 0.3), vec3(0.2)) # fence
    create_block(ivec3(-62, -62, -60), ivec3(1, 120, 120), vec3(0.8, 0.6, 0.1), vec3(0.3)) # wall1
    create_block(ivec3(-62, -62, -60), ivec3(120, 120, 1), vec3(0.8, 0.6, 0.1), vec3(0.3)) # wall2
    music_note(ivec3(35, 10, 30), vec3(1, 1, 1)); music_note(ivec3(-15, -20, 55), vec3(1, 1, 1))
    create_light(ivec3(-45, -61, 40), vec3(50, 1, 1)); create_light(ivec3(5, -61, 15), vec3(1, 1, 25)) # floor light
    create_light(ivec3(-45, -61, 15), vec3(1, 1, 25)); create_light(ivec3(-45, -61, 15), vec3(50, 1, 1)) # f light
    create_light(ivec3(-55, -61, 0), vec3(110, 1, 1)); create_light(ivec3(54, -61, -45), vec3(1, 1, 45)) # f light
    create_light(ivec3(-55, -61, -45), vec3(1, 1, 45)); create_light(ivec3(-55, -61, -45), vec3(110, 1, 1)) # f light
    create_light(ivec3(-61, 58, -60), ivec3(1, 1, 120)); create_light(ivec3(-61, 58, -59), ivec3(120, 1, 1)) # top
    create_light(ivec3(-61, 58, 60), ivec3(120, 1, 1)); create_light(ivec3(59, 58, -59), ivec3(1, 1, 120))
    create_light(ivec3(-27, 45, -58), ivec3(11, 1, 1)); create_light(ivec3(-27, 35, -58), ivec3(10, 1, 1)) # S
    # create_light(ivec3(-27, 25, -58), ivec3(10, 1, 1)); create_light(ivec3(-27, 35, -58), ivec3(1, 10, 1))
    # create_light(ivec3(-17, 25, -58), ivec3(1, 10, 1)); create_light(ivec3(-17, 43, -58), ivec3(1, 2, 1))
    create_light(ivec3(-27, 26, -58), ivec3(1, 2, 1)); create_light(ivec3(-3, 25, -58), ivec3(1, 21, 1)) # H
    # create_light(ivec3(7, 25, -58), ivec3(1, 21, 1)); create_light(ivec3(-3, 35, -58), ivec3(10, 1, 1)) # H
    create_block(ivec3(-35, 20, -59), ivec3(50, 30, 1), vec3(0.2, 0.6, 0.4), vec3(0.01))

initialize_voxels()

scene.finish()
