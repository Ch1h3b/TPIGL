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

Le premier utilisateur inscript est par default l'administrateur.
Pour visualiser les fonctionalité d'un simple utilisateur s'inscrire avec une second compte, ou alors modifier .env!

Une section de app.py (voir commentaire) doit etre modifié selon les preferences de l'administrateur.

