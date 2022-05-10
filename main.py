from utils.scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-1, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4))
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))


@ti.func
def create_block(pos, size, color, color_noise):
    for I in ti.grouped(
        ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]), (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())


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
        create_block(ivec3(-60, -64 + i, -60), ivec3(120, 1, 120), vec3(0.8, 0.6, 0.1), vec3(0.3)) # base
        make_round(ivec3(-15, i*24 - 40, 30), 20 - 6*i, 10, vec3(0.5, 0.3, 0.3), vec3(0.05))
        create_block(ivec3(2 + 16*i, 10, -18), ivec3(10, 6, 6), vec3(1, 1, 1), vec3(0.01)) # 鼓架
        make_round2(ivec3(-5 + i*40, 10, -18), 14, 10, vec3(0.2, 0.3, 0.2), vec3(0.1)) # tom drum
        make_round2(ivec3(-5 + i*40, 19, -18), 12, 1, vec3(1, 1, 1), vec3(0.1)) # tom drum2
    create_block(ivec3(-18, -12, 36), ivec3(6, 40, 4), vec3(0.5, 0.4, 0.4), vec3(0.01)) # guitar neck
    create_block(ivec3(-19, 28, 36), ivec3(8, 13, 4), vec3(0.5, 0.3, 0.3), vec3(0.01)) # guitar neck2
    create_block(ivec3(-21, -35, 35), ivec3(12, 2, 5), vec3(0.1, 0.1, 0.1), vec3(0.01)) # guitar pillow
    make_round(ivec3(-15, -22, 35), 5, 5, vec3(0.1, 0.1, 0.1), vec3(0.0)) # hole
    make_round(ivec3(15, -30, -40), 32, 20, vec3(0.2, 0.3, 0.2), vec3(0.2)) # kick drum1
    make_round(ivec3(15, -30, -19), 30, 1, vec3(0.8, 0.9, 0.9), vec3(0.2)) # kick drum2
    create_block(ivec3(12, 6, -18), ivec3(6, 10, 6), vec3(1, 1, 1), vec3(0.01)) # 鼓架
    make_round2(ivec3(45, -10, -45), 14, 10, vec3(0.2, 0.3, 0.2), vec3(0.1)) # snare
    make_round2(ivec3(-35, -50, -42), 18, 35, vec3(0.2, 0.3, 0.2), vec3(0.1)) # floor tom


initialize_voxels()

scene.finish()
