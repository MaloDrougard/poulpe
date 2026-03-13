dernière ajout:
- picam.py pour l'utilisation des cam ISC rasberry

prochaines étapes:
- création des filtres
- connection du clavier midi



## systemd poulpe services

Le fichier `poulpe-*.service` permet de lancer les applications `picam.py`, `arduino-api.py`, `midi.py` au démarrage.

Installation:

```bash
sudo cp ./poulpe-*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl status poulpe-*.service
```

Vérification:

```bash
systemctl status poulpe-*.service
journalctl -u poulpe-*.service -f