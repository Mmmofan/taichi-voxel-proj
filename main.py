from utils.scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-1, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4))
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))

@ti.func
def create_block(pos, size, color, color_noise=vec3(0.0)):
    for I in ti.grouped(
        ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]), (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.func
def music_note(pos, color):
    create_block(pos, ivec3(1, 5, 1), color)
    create_block(ivec3(pos[0], pos[1]+5, pos[2]), ivec3(1, 1, 5), color)
    create_block(ivec3(pos[0], pos[1], pos[2]+5), ivec3(1, 6, 1), color)
    scene.set_voxel(ivec3(pos[0], pos[1], pos[2]+1), 1, color)
    scene.set_voxel(ivec3(pos[0], pos[1], pos[2]+6), 1, color)

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
        make_round2(ivec3(-5 + i*40, 10, -3), 14, 10, vec3(0.2, 0.3, 0.2), vec3(0.1)) # tom drum
        make_round2(ivec3(-5 + i*40, 19, -3), 12, 1, vec3(1, 1, 1), vec3(0.1)) # tom drum2
    create_block(ivec3(-18, -12, 36), ivec3(6, 40, 4), vec3(0.5, 0.4, 0.4), vec3(0.01)) # guitar neck
    create_block(ivec3(-19, 28, 36), ivec3(8, 13, 4), vec3(0.5, 0.3, 0.3), vec3(0.01)) # guitar neck2
    create_block(ivec3(-21, -35, 35), ivec3(12, 2, 5), vec3(0.1, 0.1, 0.1), vec3(0.01)) # guitar pillow
    make_round(ivec3(-15, -22, 35), 5, 5, vec3(0.1, 0.1, 0.1), vec3(0.0)) # hole
    make_round(ivec3(13, -30, -25), 32, 20, vec3(0.2, 0.3, 0.2), vec3(0.2)) # kick drum1
    make_round(ivec3(13, -30, -4), 30, 1, vec3(0.8, 0.9, 0.9), vec3(0.2)) # kick drum2
    create_block(ivec3(12, 6, -3), ivec3(6, 10, 6), vec3(1, 1, 1), vec3(0.01)) # 鼓架
    make_round2(ivec3(45, -10, -30), 14, 10, vec3(0.2, 0.3, 0.2), vec3(0.1)) # snare
    make_round2(ivec3(45, -1, -30), 12, 1, vec3(1, 1, 1), vec3(0.1)) # snare2
    create_block(ivec3(45, -60, -30), ivec3(2, 50, 2), vec3(1., 1., 1.), vec3(0.0)) # snare3
    make_round2(ivec3(-35, -50, -27), 18, 35, vec3(0.2, 0.3, 0.2), vec3(0.1)) # floor tom
    make_round2(ivec3(-35, -16, -27), 16, 1, vec3(1, 1, 1), vec3(0.1)) # floor tom2
    for i in range(40):
        create_block(ivec3(30, -60+i, 40-i//2), ivec3(20, 1, 1), vec3(0.0, 0.0, 0.0), vec3(0.1)) # ad-plate
    for i in range(8):
        create_block(ivec3(-55+i*16, -62, 58), ivec3(2, 120, 1), vec3(0.3, 0.3, 0.3), vec3(0.2)) # fence
    create_block(ivec3(-62, -62, -60), ivec3(1, 120, 120), vec3(0.8, 0.6, 0.1), vec3(0.3))
    create_block(ivec3(-62, -62, -60), ivec3(120, 120, 1), vec3(0.8, 0.6, 0.1), vec3(0.3))
    music_note(ivec3(-40, 10, 30), vec3(0, 0, 0))
    music_note(ivec3(-15, -20, 55), vec3(0, 0, 0))

initialize_voxels()

scene.finish()
