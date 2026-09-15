from gpiozero import LightSensor, Buzzer
import pygame
import time
import os
import requests

from picamera import PiCamera
from time import sleep

class_names = ['class_c', 'class_d', 'class_e', 'class_g']

camera = PiCamera()
camera.resolution = (450, 450)

pygame.mixer.init()

# up chords
sound0 = pygame.mixer.Sound("sounds/c.wav")
sound1 = pygame.mixer.Sound("sounds/d.wav")
sound2 = pygame.mixer.Sound("sounds/e.wav")
sound3 = pygame.mixer.Sound("sounds/g.wav")

# down chords
sound4 = pygame.mixer.Sound("sounds/c.wav")
sound5 = pygame.mixer.Sound("sounds/d.wav")
sound6 = pygame.mixer.Sound("sounds/e.wav")
sound7 = pygame.mixer.Sound("sounds/g.wav")
# sound4 = pygame.mixer.Sound("d.wav")
# sound5 = pygame.mixer.Sound("d.wav")
# sound6 = pygame.mixer.Sound("d.wav")
# sound7 = pygame.mixer.Sound("d.wav")

ldr1 = LightSensor(14)
ldr2 = LightSensor(15)
sounds = (sound0, sound1, sound2, sound3, sound4, sound5, sound6, sound7)
current_sound = 0

print("---Program started---")

ldr1_timer = 0
ldr2_timer = 0

delay = 0
last1 = 0
last2 = 0

camera.start_preview()

try:
    while True:
        ldr1_strummed = ldr1.value < 0.5
        ldr2_strummed = ldr2.value < 0.5
      
        if (ldr1_strummed or ldr2_strummed):
            # take photo!
            os.makedirs('./media', exist_ok=True)
            # print("Taking picture...")
            # os.system('raspistill -o media/image.png -w 450 -h 450')
            print("Taking picture...")
            camera.capture('./media/image.png')
            print("Uploading picture...")
            upload_file = open("media/image.png", "rb")
            r = requests.post('http://oracle-2.host:9990/', files = {"file": upload_file})

            current_sound = int(r.text)
            print("Sound:", class_names[current_sound])

            if (ldr1_strummed and time.time() - last1 >= delay):
                print(f"playing noise from ldr1! currently on sound {current_sound}")
                pygame.mixer.Sound.play(sounds[current_sound])
                last1 = time.time()

            if (ldr2_strummed and time.time() - last2 >= delay):
                current_sound += 4
                print(f"playing noise from ldr2! currently on sound {current_sound}")
                pygame.mixer.Sound.play(sounds[current_sound])
                last2 = time.time()

except KeyboardInterrupt:
    print("Program exited with Ctrl-C")
    camera.stop_preview()
