# Snake Garden

Snake in Python con un prato disegnato proceduralmente, serpente con squame,
occhi e lingua animata, mele, ombre e particelle. Il movimento viene interpolato
a 60 fotogrammi al secondo; la velocità aumenta con le mele raccolte.
Non servono immagini o altri file esterni.

## Avvio

Con Python 3.10 o successivo, dalla cartella del progetto:

```powershell
python -m pip install -r requirements.txt
python snake.py
```

## Comandi

- **Frecce / WASD**: muovi il serpente.
- **Spazio / Invio**: inizia la partita.
- **Spazio / P**: pausa e riprendi. La pausa si attiva anche cambiando finestra.
- **Invio / C / Spazio**: nuova partita dopo una sconfitta o una vittoria.
- **Esc / Q**: esci.

Raccogli le mele senza toccare i bordi o il corpo. Il record rimane disponibile
durante la sessione e si azzera alla chiusura del gioco.

## Verifica

I test eseguono anche il rendering senza aprire finestre:

```powershell
python -m unittest -v
```
