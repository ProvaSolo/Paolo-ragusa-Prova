import pygame
import time
import random

# Inizializzazione di Pygame
pygame.init()

# Definizione dei colori
BIANCO = (255, 255, 255)
GIALLO = (255, 255, 102)
NERO = (0, 0, 0)
ROSSO = (213, 50, 80)
VERDE = (0, 255, 0)
BLU = (50, 153, 213)

# Dimensioni della finestra di gioco
LARGHEZZA = 600
ALTEZZA = 400

# Creazione della finestra
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption('Snake in Python')

clock = pygame.time.Clock()

# Impostazioni del serpente
blocco_serpente = 10
velocita_serpente = 15

# Stili del testo
font_stile = pygame.font.SysFont("bahnschrift", 20)
font_punteggio = pygame.font.SysFont("comicsansms", 30)

def mostra_punteggio(score):
    valore = font_punteggio.render("Punteggio: " + str(score), True, GIALLO)
    schermo.blit(valore, [10, 10])

def disegna_serpente(blocco_serpente, lista_serpente):
    for x in lista_serpente:
        pygame.draw.rect(schermo, VERDE, [x[0], x[1], blocco_serpente, blocco_serpente])

def messaggio(msg, colore):
    mesg = font_stile.render(msg, True, colore)
    schermo.blit(mesg, [LARGHEZZA / 6, ALTEZZA / 3])

def gioco():
    game_over = False
    game_close = False

    # Posizione di partenza (centro dello schermo)
    x1 = LARGHEZZA / 2
    y1 = ALTEZZA / 2

    # Variabili di movimento
    x1_cambio = 0
    y1_cambio = 0

    lista_serpente = []
    lunghezza_serpente = 1

    # Generazione casuale del primo cibo
    cibo_x = round(random.randrange(0, LARGHEZZA - blocco_serpente) / 10.0) * 10.0
    cibo_y = round(random.randrange(0, ALTEZZA - blocco_serpente) / 10.0) * 10.0

    while not game_over:

        # Schermata di fine partita
        while game_close == True:
            schermo.fill(NERO)
            messaggio("Hai perso! Premi Q per Uscire o C per Rigiocare", ROSSO)
            mostra_punteggio(lunghezza_serpente - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gioco()

        # Lettura dei comandi da tastiera
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_cambio == 0:
                    x1_cambio = -blocco_serpente
                    y1_cambio = 0
                elif event.key == pygame.K_RIGHT and x1_cambio == 0:
                    x1_cambio = blocco_serpente
                    y1_cambio = 0
                elif event.key == pygame.K_UP and y1_cambio == 0:
                    y1_cambio = -blocco_serpente
                    x1_cambio = 0
                elif event.key == pygame.K_DOWN and y1_cambio == 0:
                    y1_cambio = blocco_serpente
                    x1_cambio = 0

        # Controllo collisioni con i bordi
        if x1 >= LARGHEZZA or x1 < 0 or y1 >= ALTEZZA or y1 < 0:
            game_close = True
            
        x1 += x1_cambio
        y1 += y1_cambio
        schermo.fill(BLU)
        
        # Disegno il cibo
        pygame.draw.rect(schermo, ROSSO, [cibo_x, cibo_y, blocco_serpente, blocco_serpente])
        
        # Aggiornamento posizione del serpente
        testa_serpente = []
        testa_serpente.append(x1)
        testa_serpente.append(y1)
        lista_serpente.append(testa_serpente)
        
        # Mantiene la lunghezza corretta del serpente
        if len(lista_serpente) > lunghezza_serpente:
            del lista_serpente[0]

        # Controllo collisioni con se stesso
        for blocco in lista_serpente[:-1]:
            if blocco == testa_serpente:
                game_close = True

        disegna_serpente(blocco_serpente, lista_serpente)
        mostra_punteggio(lunghezza_serpente - 1)

        pygame.display.update()

        # Mangiare il cibo
        if x1 == cibo_x and y1 == cibo_y:
            cibo_x = round(random.randrange(0, LARGHEZZA - blocco_serpente) / 10.0) * 10.0
            cibo_y = round(random.randrange(0, ALTEZZA - blocco_serpente) / 10.0) * 10.0
            lunghezza_serpente += 1

        clock.tick(velocita_serpente)

    pygame.quit()
    quit()

# Avvia il gioco
gioco()
