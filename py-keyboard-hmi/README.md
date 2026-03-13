dernière ajout:
- picam.py pour l'utilisation des cam ISC rasberry

prochaines étapes:
- création des filtres
- connection du clavier midi


## systemd service webcam

Le fichier `webcam.service` permet de lancer `webcam.py` au démarrage graphique.

Installation:

```bash
sudo cp /home/makem/Git/poulpe/py-keyboard-hmi/webcam.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start webcam.service
```

Vérification:

```bash
systemctl status webcam.service
journalctl -u webcam.service -f
```

