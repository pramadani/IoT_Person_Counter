from playsound import playsound
import multiprocessing
import time

def play_sound(path):
    playsound(path)

def start_playsound(path):
    process = multiprocessing.Process(target=play_sound, args=(path,))  # type: ignore
    process.daemon = True
    process.start()

def check_playsound(delay, namespace):
    while True:
        if namespace.person_count is not None:
            if namespace.person_count >= 0:
                start_playsound("10_person.mp3")
        
        time.sleep(delay)
        
def start_sound_process(delay, namespace):
    process = multiprocessing.Process(target=check_playsound, args=(delay, namespace))  # type: ignore
    process.start()