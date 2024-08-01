import pygame # type: ignore
import multiprocessing
import time

def play_sound(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def check_playsound(delay, namespace):
    while True:
        if namespace.person_count is not None:
            if namespace.person_count >= 1:
                play_sound("./resources/10_person.mp3")
        time.sleep(delay)

def start_sound_process(delay, namespace):
    process = multiprocessing.Process(target=check_playsound, args=(delay, namespace))
    process.start()