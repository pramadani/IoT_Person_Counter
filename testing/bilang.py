import pygame
import time
pygame.mixer.init()

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
            sound_path = sound_files[word]
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    kata_list = terbilang(angka).split(" ")
    for word in kata_list:
        play_terbilang_angka(kata)

def play_suhu_mencapai(suhu):
    pygame.mixer.music.load("resources/sound/suhu_mencapai.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    play_terbilang()
    pygame.mixer.music.load("resources/sound/derajat.mp3")
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def play_orang_mencapai(jumlah):
    pygame.mixer.music.load("resources/sound/orang_mencapai.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    play_terbilang()

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
        if namespace.person_count is None or namespace.temperature is None:
            time.sleep(0.1)
            continue

        if namespace.temperature > 30:
            play_suhu_mencapai(namespace.temperature)
            play_orang_mencapai(namespace.person_count)
            play_menurunkan_suhu()
            
        time.sleep(delay)