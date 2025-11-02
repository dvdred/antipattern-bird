import unittest, pathlib, os, builtins, sys
from pathlib import Path
#from app import *

# Verifica se stiamo eseguendo i test
is_testing = 'unittest' in sys.modules or 'pytest' in sys.modules

# Set dummy drivers before importing pygame
#os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Now import pygame - it will use dummy drivers
import pygame

# Your existing test imports and code
from unittest.mock import Mock

# Import your app after setting up the environment
try:
    from app import *
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class TestGameFilesExist(unittest.TestCase):
    def test_required_resource_files_exist(self):
        """Test che verifica l'esistenza dei file risorse necessari al gioco"""
        # Lista dei file necessari
        required_files = [
            'icon32.png',
            'jump.wav',
            'point.wav',
            'rainbow.wav',
            'lifeup.wav',
            'lifedown.wav',
            'golden.wav',
            'ice.wav',
            'legacy.wav',
            'debt.wav',
            'DejaVuSansMono.ttf'
        ]
        
        # Verifica che ogni file esista
        for file_name in required_files:
            with self.subTest(file=file_name):
                # Controlla diversi percorsi possibili
                possible_paths = [
                    file_name,  # Percorso corrente
                    os.path.join('assets', file_name),  # Percorso assets
                    os.path.join('resources', file_name),  # Percorso resources
                ]
                
                file_exists = False
                for path in possible_paths:
                    if os.path.exists(path):
                        file_exists = True
                        break
                
                self.assertTrue(file_exists, f"File mancante: {file_name}")

class TestPipeDraw(unittest.TestCase):
    def test_draw_method(self):
        # Creare un'istanza della classe Pipe
        pipe = Pipe(100, "Test Text", 180)
        # Creare una superficie di test
        surface = Mock()
        # Chiamare il metodo draw
        pipe.draw(surface)
        # Verificare che il metodo blit sia stato chiamato almeno una volta
        # (Potrebbe essere chiamato più volte per i vari componenti)
        surface.blit.assert_called()

class TestBirdDraw(unittest.TestCase):
    def test_draw_method(self):
        # Creare un'istanza della classe Bird
        # Controlla la firma del costruttore Bird nella classe
        bird = Bird()  # Prova con un solo parametro
        # Creare una superficie di test
        surface = Mock()
        # Chiamare il metodo draw
        bird.draw(surface)
        # Verificare che il metodo blit sia stato chiamato
        surface.blit.assert_called()

class TestBirdUpdate(unittest.TestCase):
    def test_bird_update(self):
        bird = Bird()
        bird.x = 100
        bird.y = 100
        bird.velocity = 5
        bird.update()
        self.assertAlmostEqual(bird.y, 100.25, places=2)

class TestPipeCollide(unittest.TestCase):
  
    def setUp(self):
        # Creiamo un mock per il passero (bird)
        self.bird = Mock()
        self.bird.x = 100
        self.bird.y = 100
        self.bird.size = 20
        
        # Creiamo un'istanza di Pipe con valori di esempio
        # Using the actual constructor signature from the context
        self.pipe = Pipe(100, "Test Text", 180)
        
        # Set the height and gap to known values for testing
        self.pipe.height = 150  # Set a specific height
        self.pipe.gap = 100    # Set a specific gap
  
    def test_collide_with_top_pipe(self):
        # Simuliamo una collisione con il tubo superiore
        # The bird's rectangle should be positioned to collide with top pipe
        self.bird.get_rect.return_value = pygame.Rect(100, 50, 20, 20)  # Position above the top pipe
        
        # Verifichiamo che collide restituisca True
        result = self.pipe.collide(self.bird)
        self.assertTrue(result, "Collisione con il tubo superiore non rilevata")
  
    def test_collide_with_bottom_pipe(self):
        # Simuliamo una collisione con il tubo inferiore
        # The bird's rectangle should be positioned to collide with bottom pipe
        self.bird.get_rect.return_value = pygame.Rect(100, 250, 20, 20)  # Position below the bottom pipe
        
        # Verifichiamo che collide restituisca True
        result = self.pipe.collide(self.bird)
        self.assertTrue(result, "Collisione con il tubo inferiore non rilevata")
  
    def test_no_collide(self):
        # Simuliamo nessuna collisione
        # The bird's rectangle should be positioned so it doesn't collide with either pipe
        self.bird.get_rect.return_value = pygame.Rect(150, 200, 20, 20)  # Position away from pipes
        
        # Verifichiamo che collide restituisca False
        result = self.pipe.collide(self.bird)
        self.assertFalse(result, "Collisione rilevata dove non ci doveva essere")

class TestPipeUpdate(unittest.TestCase):
    def test_pipe_update(self):
        pipe = Pipe(100, "Test", 180)
        pipe.x = 100
        pipe.update()
        self.assertEqual(pipe.x, 97)  # Se si muove di 3

class TestDrawScore(unittest.TestCase):
    def test_draw_score_called(self):
        surface = Mock()
        score = 1000

        draw_score(surface, score)

        surface.blit.assert_called()

class TestDrawLives(unittest.TestCase):
    def test_draw_lives_called(self):
        surface = Mock()
        lives = 3

        draw_lives(surface, lives)

        surface.blit.assert_called()

class TestDrawLevel(unittest.TestCase):
    def test_draw_level_called(self):
        surface = Mock()
        level = 2

        draw_level(surface, level)

        surface.blit.assert_called()

class TestDrawPauseOverlay(unittest.TestCase):
    def test_draw_pause_overlay_called(self):
        surface = Mock()

        draw_pause_overlay(surface)

        surface.blit.assert_called()

class TestDrawZebraActive(unittest.TestCase):
    def test_draw_zebra_active_called(self):
        surface = Mock()
        remaining_time = 5000

        draw_zebra_active(surface, remaining_time)

        surface.blit.assert_called()

class TestDrawIceActive(unittest.TestCase):
    def test_draw_ice_active_called(self):
        surface = Mock()
        remaining_time = 8000

        draw_ice_active(surface, remaining_time)

        surface.blit.assert_called()

class TestDrawDebtIndicator(unittest.TestCase):
    def test_draw_debt_indicator_called(self):
        surface = Mock()
        bird_x, bird_y, bird_size = 100, 100, 20

        draw_debt_indicator(surface, bird_x, bird_y, bird_size)

        surface.blit.assert_called()

class TestDrawDebugInfo(unittest.TestCase):
    def test_draw_debug_info_called(self):
        surface = Mock()
        base_speed = 5
        speed_lvl = 2
        zebra_active = True
        ice_active = False
        debt_active = True
        master_speed = 10
        level_timer = 120
        current_gap = 180
        debt_mult = 2

        draw_debug_info(surface, base_speed, speed_lvl, zebra_active, ice_active, debt_active,
                        master_speed, level_timer, current_gap, debt_mult)

        surface.blit.assert_called()

class TestBirdGetRect(unittest.TestCase):
    def test_bird_get_rect(self):
        bird = Bird()
        bird.x = 100
        bird.y = 100
        bird.size = 20

        rect = bird.get_rect()
        self.assertIsInstance(rect, pygame.Rect)
        self.assertEqual(rect.x, 100)
        self.assertEqual(rect.y, 100)
        self.assertEqual(rect.width, 20)
        self.assertEqual(rect.height, 20)

class TestDrawShapeSelectionMenu(unittest.TestCase):
    def test_draw_shape_selection_menu_called(self):
        surface = pygame.Surface((800, 600))
        bg_color = (255, 255, 255)
        current_shape = "circle"
        current_color = (0, 0, 0)
        debug_mode = False

        result = draw_shape_selection_menu(surface, bg_color, current_shape, current_color, debug_mode)

        # Verifica che la funzione non sollevi eccezioni e restituisca qualcosa
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)  # 3 elementi come mostrato nel messaggio

class TestDrawStartScreen(unittest.TestCase):
    def test_draw_start_screen_called(self):
        surface = pygame.Surface((800, 600))
        demo_pipes = []
        demo_land = (100, 100, 100)  # Corretto: è una tupla invece di Mock
        start_bg_color = (255, 255, 255)

        draw_start_screen(surface, demo_pipes, demo_land, start_bg_color)

class TestDrawGameOver(unittest.TestCase):
    def test_draw_game_over_called(self):
        surface = Mock()
        score = 1000
        high_score = 2000
        bonus_score = 0
        draw_game_over(surface, score, high_score, bonus_score)
        surface.blit.assert_called()

class TestDrawWinScreen(unittest.TestCase):
    def test_draw_win_screen_called(self):
        surface = Mock()  # Usa Mock invece di pygame.Surface
        score = 1000
        high_score = 2000
        draw_win_screen(surface, score, high_score)
        surface.blit.assert_called()  # Ora funziona perché surface è un Mock



if __name__ == '__main__':
    unittest.main()