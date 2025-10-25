import os
import sys

# Setup per Android
if 'ANDROID_PRIVATE' in os.environ:
    os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = '1'
    # Path per i file su Android
    sys.path.insert(0, os.environ['ANDROID_PRIVATE'])

# Import pygame
import pygame

# Funzione per trovare risorse su Android
def resource_path(relative_path):
    if 'ANDROID_PRIVATE' in os.environ:
        return os.path.join(os.environ['ANDROID_PRIVATE'], relative_path)
    return relative_path

# Modifica il tuo app.py per usare resource_path()
# Poi importa il tuo gioco
if __name__ == '__main__':
    # Inizializzazione pygame specifica per Android
    pygame.init()
    
    # Ottieni la risoluzione dello schermo
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    
    # Su Android usa FULLSCREEN
    if 'ANDROID_PRIVATE' in os.environ:
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 600))
    
    # Importa ed esegui il tuo gioco
    import app