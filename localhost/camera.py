import time
import pygame
import pygame.camera
import uuid

def take_picture():
    pygame.camera.init()

    cam_name = pygame.camera.list_cameras()

    cam = pygame.camera.Camera(cam_name,(640,480))

    cam.start()

    time.sleep(1)

    img = cam.get_image()

    pic_path = "./pics/" + str(uuid.uuid4()) + ".jpg"

    pygame.image.save(img, pic_path)

    return pic_path