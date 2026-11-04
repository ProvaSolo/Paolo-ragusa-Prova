"""Snake Garden: grafica procedurale, senza immagini o suoni esterni."""

import math
import random
from collections import deque

import pygame


LARGHEZZA, ALTEZZA = 960, 740
CELLA = 24
COLONNE, RIGHE = 34, 22
CAMPO = pygame.Rect(72, 136, COLONNE * CELLA, RIGHE * CELLA)
PANNA = (236, 241, 218)
SALVIA = (157, 183, 145)
DIREZIONI = {
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
}


def centro(cella):
    return pygame.Vector2(CAMPO.x + (cella[0] + .5) * CELLA,
                          CAMPO.y + (cella[1] + .5) * CELLA)


class SnakeGarden:
    def __init__(self):
        pygame.init()
        self.schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
        pygame.display.set_caption("Snake Garden")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("segoeui", 19)
        self.piccolo = pygame.font.SysFont("segoeui", 15)
        self.grande = pygame.font.SysFont("segoeui", 43, bold=True)
        self.numero = pygame.font.SysFont("segoeui", 30, bold=True)
        self.record = 0
        self.tempo = 0
        self.sfondo = self.crea_giardino()
        self.nuova_partita()

    def nuova_partita(self):
        self.serpente = [(10, 11), (9, 11), (8, 11), (7, 11), (6, 11)]
        self.precedente = self.serpente.copy()
        self.direzione = (1, 0)
        self.comandi = deque()
        self.punti = 0
        self.accumulatore = 0
        self.stato = "pronto"
        self.particelle = []
        self.cibo = self.genera_cibo()

    @property
    def intervallo(self):
        return max(.075, .145 - self.punti * .0025)

    def genera_cibo(self):
        occupate = set(self.serpente)
        libere = [(x, y) for y in range(RIGHE) for x in range(COLONNE)
                  if (x, y) not in occupate]
        return random.choice(libere) if libere else None

    def testo(self, testo, posizione, font=None, colore=PANNA, centro_x=False):
        superficie = (font or self.font).render(testo, True, colore)
        rettangolo = superficie.get_rect()
        if centro_x:
            rettangolo.midtop = posizione
        else:
            rettangolo.topleft = posizione
        self.schermo.blit(superficie, rettangolo)

    def crea_giardino(self):
        superficie = pygame.Surface((LARGHEZZA, ALTEZZA))
        for y in range(ALTEZZA):
            t = y / ALTEZZA
            pygame.draw.line(superficie, (int(19 - 7*t), int(37 - 12*t),
                                         int(30 - 8*t)), (0, y), (LARGHEZZA, y))
        pygame.draw.rect(superficie, (8, 18, 13), CAMPO.inflate(22, 22).move(0, 6),
                         border_radius=20)
        pygame.draw.rect(superficie, (65, 88, 55), CAMPO.inflate(16, 16),
                         border_radius=16)
        pygame.draw.rect(superficie, (105, 126, 76), CAMPO.inflate(6, 6),
                         width=2, border_radius=7)
        rng = random.Random(18)
        for y in range(RIGHE):
            for x in range(COLONNE):
                tono = rng.randint(-3, 3) + (x + y) % 2 * 3
                r = pygame.Rect(CAMPO.x + x*CELLA, CAMPO.y + y*CELLA, CELLA, CELLA)
                pygame.draw.rect(superficie, (43 + tono, 66 + tono, 37 + tono), r)
        for _ in range(1900):
            x = rng.randrange(CAMPO.left + 3, CAMPO.right - 3)
            y = rng.randrange(CAMPO.top + 4, CAMPO.bottom - 2)
            colore = rng.choice([(55, 79, 43), (61, 83, 46), (36, 58, 32)])
            pygame.draw.line(superficie, colore, (x, y), (x + rng.choice([-2, 1, 2]), y - 3))
        for _ in range(32):
            x = rng.randrange(CAMPO.left + 5, CAMPO.right - 5)
            y = rng.randrange(CAMPO.top + 5, CAMPO.bottom - 5)
            pygame.draw.circle(superficie, (113, 119, 66), (x, y), 1)
        return superficie

    def cambia_direzione(self, direzione):
        ultima = self.comandi[-1] if self.comandi else self.direzione
        if direzione != ultima and direzione != (-ultima[0], -ultima[1]):
            if len(self.comandi) < 2:
                self.comandi.append(direzione)

    def passo(self):
        if self.comandi:
            self.direzione = self.comandi.popleft()
        x, y = self.serpente[0]
        dx, dy = self.direzione
        testa = (x + dx, y + dy)
        mangia = testa == self.cibo
        # La coda libera la propria cella durante lo stesso passo.
        corpo = self.serpente if mangia else self.serpente[:-1]
        if not (0 <= testa[0] < COLONNE and 0 <= testa[1] < RIGHE) or testa in corpo:
            self.stato = "perso"
            return
        self.precedente = self.serpente.copy()
        self.serpente.insert(0, testa)
        if mangia:
            self.punti += 1
            self.record = max(self.record, self.punti)
            self.esplosione(centro(testa))
            self.cibo = self.genera_cibo()
            if self.cibo is None:
                self.stato = "vinto"
        else:
            self.serpente.pop()

    def esplosione(self, posizione):
        for _ in range(20):
            angolo = random.uniform(0, math.tau)
            velocita = pygame.Vector2(math.cos(angolo), math.sin(angolo)) * random.uniform(25, 100)
            self.particelle.append([posizione.copy(), velocita, random.uniform(.3, .65)])

    def aggiorna(self, dt):
        self.tempo += dt
        if self.stato != "gioco":
            return
        self.accumulatore += dt
        while self.accumulatore >= self.intervallo and self.stato == "gioco":
            intervallo = self.intervallo
            self.accumulatore -= intervallo
            self.passo()
        for particella in self.particelle:
            particella[0] += particella[1] * dt
            particella[1] *= max(0, 1 - dt * 3)
            particella[2] -= dt
        self.particelle = [p for p in self.particelle if p[2] > 0]

    def disegna_mela(self):
        if self.cibo is None:
            return
        p = centro(self.cibo)
        y = p.y + math.sin(self.tempo * 3) * 1.5
        alone = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.circle(alone, (241, 131, 67, 14), (32, 32),
                           int(24 + math.sin(self.tempo * 3)*2))
        self.schermo.blit(alone, (p.x - 32, p.y - 32))
        pygame.draw.ellipse(self.schermo, (25, 43, 26), (p.x - 10, p.y + 6, 21, 8))
        pygame.draw.line(self.schermo, (111, 75, 40), (p.x, y-4), (p.x+2, y-14), 3)
        pygame.draw.ellipse(self.schermo, (143, 188, 78), (p.x+2, y-14, 10, 5))
        pygame.draw.circle(self.schermo, (161, 48, 35), (p.x, y+1), 10)
        pygame.draw.circle(self.schermo, (225, 76, 45), (p.x-3, y-1), 8)
        pygame.draw.circle(self.schermo, (238, 100, 57), (p.x+3, y-2), 7)
        pygame.draw.ellipse(self.schermo, (255, 186, 125), (p.x-6, y-6, 4, 6))

    def disegna_serpente(self):
        fattore = min(1, self.accumulatore / self.intervallo)
        if self.stato in ("pronto", "perso", "vinto"):
            fattore = 1
        punti = []
        for i, cella in enumerate(self.serpente):
            prima = self.precedente[min(i, len(self.precedente)-1)]
            punti.append(centro(prima).lerp(centro(cella), fattore))

        # Risoluzione doppia per contorni morbidi e squame leggibili.
        pelle = pygame.Surface((CAMPO.width*2, CAMPO.height*2), pygame.SRCALPHA)
        locali = [(p - pygame.Vector2(CAMPO.topleft))*2 for p in punti]
        for i in range(len(locali)-1, -1, -1):
            p = locali[i]
            raggio = 19 if i == 0 else int(17 - 8*(i/max(1, len(locali)-1))**3)
            ombra = p + pygame.Vector2(3, 7)
            if i < len(locali)-1:
                pygame.draw.line(pelle, (9, 24, 12, 110), ombra,
                                 locali[i+1] + pygame.Vector2(3, 7), raggio*2+3)
            pygame.draw.circle(pelle, (9, 24, 12, 110), ombra, raggio+2)
        for i in range(len(locali)-1, -1, -1):
            p = locali[i]
            raggio = 19 if i == 0 else int(17 - 8*(i/max(1, len(locali)-1))**3)
            colore = (121, 166, 64) if i == 0 else (91, 143 + i % 3*4, 53)
            if i < len(locali)-1:
                pygame.draw.line(pelle, colore, p, locali[i+1], raggio*2)
            pygame.draw.circle(pelle, colore, p, raggio)
            pygame.draw.circle(pelle, (151, 185, 82), p + pygame.Vector2(-3, -5),
                               max(3, raggio-7))
            if i > 0:
                asse = locali[max(0, i-1)] - p
                if asse.length_squared() > 0:
                    asse = asse.normalize()
                    lato = pygame.Vector2(-asse.y, asse.x)
                    for scarto in (-7, 4):
                        c = p + asse*scarto
                        pygame.draw.lines(pelle, (66, 113, 43), False,
                                          [c-lato*6-asse*2, c+asse*2, c+lato*6-asse*2], 2)

        direzione = locali[0] - locali[1]
        if direzione.length_squared() == 0:
            direzione = pygame.Vector2(self.direzione)
        direzione = direzione.normalize()
        lato = pygame.Vector2(-direzione.y, direzione.x)
        testa = locali[0]
        if self.stato == "gioco" and math.sin(self.tempo*4) > .88:
            base = testa + direzione*18
            punta = base + direzione*14
            pygame.draw.line(pelle, (216, 103, 99), base, punta, 3)
            for segno in (-1, 1):
                pygame.draw.line(pelle, (216, 103, 99), punta,
                                 punta+direzione*5+lato*segno*4, 2)
        for segno in (-1, 1):
            occhio = testa + direzione*7 + lato*segno*11
            pygame.draw.circle(pelle, (224, 218, 134), occhio, 6)
            pygame.draw.circle(pelle, (16, 30, 19), occhio+direzione*2, 4)
            pygame.draw.circle(pelle, (255, 255, 230), occhio+pygame.Vector2(-1, -2), 1)
        self.schermo.blit(pygame.transform.smoothscale(pelle, CAMPO.size), CAMPO)

    def disegna_pannello(self):
        velo = pygame.Surface((LARGHEZZA, ALTEZZA), pygame.SRCALPHA)
        velo.fill((6, 16, 12, 150))
        self.schermo.blit(velo, (0, 0))
        card = pygame.Rect(210, 251, 540, 292)
        pygame.draw.rect(self.schermo, (10, 25, 19), card.move(0, 7), border_radius=24)
        pygame.draw.rect(self.schermo, (28, 49, 35), card, border_radius=24)
        pygame.draw.rect(self.schermo, (84, 112, 63), card, 1, border_radius=24)
        titoli = {"pronto": "Un piccolo giardino.", "pausa": "Prenditi una pausa.",
                  "perso": "Si ricomincia?", "vinto": "Il giardino è tuo!"}
        self.testo("S N A K E  G A R D E N", (480, 277), self.piccolo, SALVIA, True)
        self.testo(titoli[self.stato], (480, 310), self.grande, centro_x=True)
        dettaglio = {
            "pronto": "Raccogli le mele e lascia spazio alla tua coda.",
            "pausa": "Il tuo giardino ti aspetta.",
            "perso": f"{self.punti} mele raccolte  ·  Record sessione: {self.record}",
            "vinto": f"Hai riempito tutto il prato: {self.punti} mele!",
        }
        self.testo(dettaglio[self.stato], (480, 375), colore=SALVIA, centro_x=True)
        bottone = pygame.Rect(310, 429, 340, 48)
        pygame.draw.rect(self.schermo, (176, 207, 111), bottone, border_radius=12)
        etichetta = "SPAZIO  /  Inizia" if self.stato == "pronto" else (
            "SPAZIO  /  Riprendi" if self.stato == "pausa" else "INVIO  /  Gioca ancora")
        self.testo(etichetta, (480, 440), colore=(25, 48, 29), centro_x=True)
        self.testo("Frecce o WASD per muoverti", (480, 494), self.piccolo, SALVIA, True)

    def disegna(self):
        self.schermo.blit(self.sfondo, (0, 0))
        self.testo("SNAKE", (72, 28), self.grande)
        self.testo("G A R D E N", (74, 83), self.piccolo, SALVIA)
        self.testo("MELE", (617, 32), self.piccolo, SALVIA)
        self.testo(f"{self.punti:02}", (615, 53), self.numero)
        self.testo("RECORD SESSIONE", (726, 32), self.piccolo, SALVIA)
        self.testo(f"{self.record:02}", (726, 53), self.numero)
        self.disegna_mela()
        self.disegna_serpente()
        for posizione, _, vita in self.particelle:
            pygame.draw.circle(self.schermo, (235, 194, 103), posizione, max(1, int(vita*6)))
        self.testo("FRECCE / WASD   Muovi", (72, 696), self.piccolo, SALVIA)
        self.testo("SPAZIO / P   Pausa", (383, 696), self.piccolo, SALVIA)
        self.testo("ESC   Esci", (809, 696), self.piccolo, SALVIA)
        if self.stato != "gioco":
            self.disegna_pannello()
        pygame.display.flip()

    def gestisci_evento(self, evento):
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.WINDOWFOCUSLOST and self.stato == "gioco":
            self.stato = "pausa"
        if evento.type != pygame.KEYDOWN:
            return True
        tasto = evento.key
        if tasto in (pygame.K_ESCAPE, pygame.K_q):
            return False
        if self.stato in ("perso", "vinto"):
            if tasto in (pygame.K_RETURN, pygame.K_c, pygame.K_SPACE):
                self.nuova_partita()
                self.stato = "gioco"
        elif tasto in (pygame.K_SPACE, pygame.K_p, pygame.K_RETURN):
            self.stato = "pausa" if self.stato == "gioco" else "gioco"
        elif tasto in DIREZIONI and self.stato in ("pronto", "gioco"):
            self.cambia_direzione(DIREZIONI[tasto])
            self.stato = "gioco"
        return True

    def esegui(self):
        attivo = True
        while attivo:
            dt = min(self.clock.tick(60)/1000, .1)
            for evento in pygame.event.get():
                if not self.gestisci_evento(evento):
                    attivo = False
            if attivo:
                self.aggiorna(dt)
                self.disegna()
        pygame.quit()


def gioco():
    SnakeGarden().esegui()


if __name__ == "__main__":
    gioco()
