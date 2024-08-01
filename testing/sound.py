import pygame

# Inisialisasi mixer pygame
pygame.mixer.init()

# Memuat file MP3
pygame.mixer.music.load('10_person.mp3')

# Memutar file MP3
pygame.mixer.music.play()

# Menunggu sampai musik selesai
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
