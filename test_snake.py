"""Verifica regole, comandi e rendering senza aprire finestre."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from snake import COLONNE, RIGHE, SnakeGarden


class RegoleSnake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gioco = SnakeGarden()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.gioco.nuova_partita()
        self.gioco.stato = "gioco"
        self.gioco.cibo = (0, 0)

    def test_mela_allunga_e_aggiorna_record(self):
        g = self.gioco
        g.cibo = (11, 11)
        g.passo()
        self.assertEqual((g.punti, len(g.serpente)), (1, 6))
        self.assertGreaterEqual(g.record, 1)
        self.assertNotIn(g.cibo, g.serpente)

    def test_collisione_bordo(self):
        g = self.gioco
        g.serpente = [(COLONNE-1, 4), (COLONNE-2, 4)]
        g.passo()
        self.assertEqual(g.stato, "perso")
        self.assertEqual(g.serpente[0], (COLONNE-1, 4))

    def test_collisione_corpo(self):
        g = self.gioco
        g.serpente = [(2, 2), (2, 3), (3, 3), (3, 2), (4, 2)]
        g.passo()
        self.assertEqual(g.stato, "perso")

    def test_cella_coda_libera(self):
        g = self.gioco
        g.serpente = [(2, 2), (2, 3), (3, 3), (3, 2)]
        g.passo()
        self.assertEqual(g.stato, "gioco")
        self.assertEqual(g.serpente[0], (3, 2))

    def test_comandi_rapidi_non_invertono_la_marcia(self):
        g = self.gioco
        g.cambia_direzione((-1, 0))
        self.assertFalse(g.comandi)
        g.cambia_direzione((0, -1))
        g.cambia_direzione((-1, 0))
        g.passo()
        self.assertEqual(g.serpente[0], (10, 10))
        g.passo()
        self.assertEqual(g.serpente[0], (9, 10))

    def test_pausa_e_perdita_focus(self):
        g = self.gioco
        g.gestisci_evento(pygame.event.Event(pygame.WINDOWFOCUSLOST))
        self.assertEqual(g.stato, "pausa")
        prima = g.serpente.copy()
        g.aggiorna(1)
        self.assertEqual(g.serpente, prima)
        g.gestisci_evento(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        self.assertEqual(g.stato, "gioco")

    def test_riavvio_mantiene_record(self):
        g = self.gioco
        g.record = 12
        g.stato = "perso"
        g.gestisci_evento(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        self.assertEqual((g.stato, g.punti, g.record), ("gioco", 0, 12))

    def test_ultima_mela_vince(self):
        g = self.gioco
        g.serpente = [(COLONNE-2, RIGHE-1)] + [
            (x, y) for y in range(RIGHE) for x in range(COLONNE)
            if (x, y) not in [(COLONNE-2, RIGHE-1), (COLONNE-1, RIGHE-1)]]
        g.cibo = (COLONNE-1, RIGHE-1)
        g.passo()
        self.assertEqual(g.stato, "vinto")
        self.assertIsNone(g.cibo)

    def test_rendering_stati_e_animazioni(self):
        g = self.gioco
        for stato in ("pronto", "gioco", "pausa", "perso", "vinto"):
            g.stato = stato
            g.disegna()
        g.stato = "gioco"
        for _ in range(30):
            g.aggiorna(1/60)
            g.disegna()
        self.assertEqual(g.stato, "gioco")
        self.assertFalse(g.gestisci_evento(pygame.event.Event(pygame.QUIT)))


if __name__ == "__main__":
    unittest.main()
