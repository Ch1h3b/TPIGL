# TP IGL: TOP IMMOBILIER

TOP IMMOBILIER est une application de vente immobilière, avec react et flask.

## Instalation

L'instalation avec docker compose est trés simple (sous linux):

```bash
docker compose up
```
Ensuite visiter http://127.0.0.1:3000

Pour excuter manuellement (linux/windows), sur le dossier api:

```bash
pip install -r requirements.txt
flask run
```

sur le dossier front:

```bash
npm install
npm start
```


## Note:

Le deuxieme utilisateur inscrit est par default l'administrateur.
Pour visualiser les fonctionalités d'un administrateur s'inscrire avec un second compte, ou alors modifier .env!

Une section de app.py (voir commentaire) doit étre modifiée selon les preferences de l'administrateur.

