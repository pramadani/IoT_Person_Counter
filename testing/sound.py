import pygame

# Inisialisasi pygame dan mixer
pygame.mixer.init()

# Memuat file MP3
try:
    pygame.mixer.music.load('10_person.mp3')
except pygame.error as e:
    print(f"Error loading file: {e}")
    exit()

# Memutar file MP3
pygame.mixer.music.play()

# Menunggu sampai musik selesai
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

print("Music finished playing.")
pygame.quit()