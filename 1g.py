import pygame
import time
pygame.mixer.init()

person_count = 10
temperature = 23
angka = 23

def play_terbilang(angka):
    def terbilang(n):
        satuan = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan", "Sepuluh", "Sebelas"]
        if n < 0:
            return "Minus " + terbilang(-n)
        if n <= 11:
            return " " + satuan[n]
        elif n <= 19:
            return terbilang(n % 10) + " Belas"
        elif n <= 99:
            return terbilang(n // 10) + " Puluh" + terbilang(n % 10)
        elif n <= 199:
            return " Seratus" + terbilang(n - 100)
        elif n <= 999:
            return terbilang(n // 100) + " Ratus" + terbilang(n % 100)
        elif n <= 1999:
            return " Seribu" + terbilang(n - 1000)
        elif n <= 999999:
            return terbilang(n // 1000) + " Ribu" + terbilang(n % 1000)
        elif n <= 999999999:
            return terbilang(n // 1000000) + " Juta" + terbilang(n % 1000000)
        else:
            return terbilang(n // 1000000000) + " Milyar" + terbilang(n % 1000000000)

    def play_terbilang_angka(word):
        sound_files = {
            "satu": "resources/sound/satu.mp3",
            "dua": "resources/sound/dua.mp3",
            "tiga": "resources/sound/tiga.mp3",
            "empat": "resources/sound/empat.mp3",
            "lima": "resources/sound/lima.mp3",
            "enam": "resources/sound/enam.mp3",
            "tujuh": "resources/sound/tujuh.mp3",
            "delapan": "resources/sound/delapan.mp3",
            "sembilan": "resources/sound/sembilan.mp3",
            "sepuluh": "resources/sound/sepuluh.mp3",
            "sebelas": "resources/sound/sebelas.mp3",
            "puluh": "resources/sound/puluh.mp3",
        }

        if word in sound_files:
            print("bebas")
            sound_path = sound_files[word]
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    kata_list = terbilang(angka).strip().lower().split(" ")
    for word in kata_list:
        print(word)
        play_terbilang_angka(word)

def play_suhu_mencapai(suhu):
    pygame.mixer.music.load("resources/sound/suhu_mencapai.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    play_terbilang(suhu)
    pygame.mixer.music.load("resources/sound/derajat.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def play_orang_mencapai(jumlah):
    pygame.mixer.music.load("resources/sound/orang_mencapai.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    play_terbilang(jumlah)

def play_menurunkan_suhu():
    pygame.mixer.music.load("resources/sound/menurunkan.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def play_menaikkan_suhu():
    pygame.mixer.music.load("resources/sound/menaikkan.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def check_playsound(delay, namespace):
    while True:
        print(person_count)

        if person_count is None or temperature is None:
            time.sleep(0.1)
            continue

        if temperature >= 27:
            print("1g")
            play_suhu_mencapai(temperature)
            print("2g")
            play_orang_mencapai(person_count)
            print("3g")
            play_menurunkan_suhu()
            print("4g")
            
        elif temperature <= 20:
            play_suhu_mencapai(temperature)
            play_orang_mencapai(person_count)
            play_menaikkan_suhu()
        
        elif person_count >= 10:
            play_orang_mencapai(person_count)
        
        elif person_count >= 5:
            play_orang_mencapai(person_count)

            
        time.sleep(delay)

check_playsound(5, 1)