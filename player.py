import pygame as pg
from camera import Camera
from settings import *

class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)

        self.radius = 0.25
        self.height = 1.8

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def is_solid(self, x, y, z):
        vh = self.app.scene.world.voxel_handler
        return vh.is_solid((int(x), int(y), int(z)))

    def collide(self, new_pos):
        px, py, pz = new_pos

        r = self.radius
        h = self.height

        for dx in (-r, r):
            for dy in (0, h):
                for dz in (-r, r):
                    check_x = px + dx
                    check_y = py + dy
                    check_z = pz + dz

                    if self.is_solid(check_x, check_y, check_z):
                        return False

        return True

    def try_move(self, delta):
        x, y, z = self.position
        dx, dy, dz = delta

        new_pos = (x + dx, y, z)
        if self.collide(new_pos):
            x += dx

        new_pos = (x, y + dy, z)
        if self.collide(new_pos):
            y += dy

        new_pos = (x, y, z + dz)
        if self.collide(new_pos):
            z += dz

        self.position = (x, y, z)

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time

        move = pg.Vector3(0, 0, 0)

        if key_state[pg.K_w]:
            move += self.forward * vel
        if key_state[pg.K_s]:
            move -= self.forward * vel
        if key_state[pg.K_d]:
            move += self.right * vel
        if key_state[pg.K_a]:
            move -= self.right * vel
        if key_state[pg.K_q]:
            move.y += vel
        if key_state[pg.K_e]:
            move.y -= vel

        self.try_move(move)

    def handle_event(self, event):
        voxel_handler = self.app.scene.world.voxel_handler

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1: voxel_handler.select_block(0)
            if event.key == pg.K_2: voxel_handler.select_block(1)
            if event.key == pg.K_3: voxel_handler.select_block(2)
            if event.key == pg.K_4: voxel_handler.select_block(3)
            if event.key == pg.K_5: voxel_handler.select_block(4)
            if event.key == pg.K_6: voxel_handler.select_block(5)
            if event.key == pg.K_7: voxel_handler.select_block(6)