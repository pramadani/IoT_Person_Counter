from playsound import playsound
import multiprocessing
import time

def play_sound(path):
    playsound(path)

def start_playsound(path):
    process = multiprocessing.Process(target=play_sound, args=(path,)) # type: ignore
    process.daemon = True
    process.start()

def check_playsound(delay, person_count):
    while True:
        if person_count.value > 1:
            start_playsound("10_person.mp3")
        
        time.sleep(delay)
        
def start_sound_process(delay, person_count):
    process = multiprocessing.Process(target=check_playsound, args=(delay, person_count)) # type: ignore
    process.start()