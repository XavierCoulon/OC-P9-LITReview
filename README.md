LITReview - Critiques de livres
=

<u>Openclassrooms - DA Python - Projet 9 :</u><br>

Création d'une application web permettant la sollicitation et la publication de critiques de livres ou articles.
<br><br>
Version MVP.<br>
Utilisation du framework Django + base de données locale SQLIte.
## 1. <u>Principales fonctionnalités</u> :

- inscription et connexion au site,
- création de tickets pour demandes de critiques,
- création de critiques en réponse à des tickets,
- création directe d'un ticket / critique,
- modification & suppression de ses tickets et critiques,
- gestion d'aboonement à d'autres utilisateurs,
- visualisation d'un flux de tickets / critiques

This app has been built on an MVC approach.

## 2. <u> Documentation</u>

Sont disponibles sous le répertoire "doc" les documents suivants, fournis par OC :
- Diagramme UML de la base de données (LITReview_UML_Diagram.pdf),
- Cahier des charges (LITReview_CDC.docx),
- Wireframes (LITReview_Wireframes.pdf).

## 3. <u> Installation</u>


```bash
git clone https://github.com/XavierCoulon/OC-P9-LITReview.git
cd OC-P4-Chess-Tournament
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python main.py
```
## 2. How to use the app

The app is meant to be used from terminal. To launch the program, use the following command line.
```bash
python main.py
```


Menus:
> Home menu _(access to the menus)_ 

> Players
- create a player
- change player's ranking
> Tournament

- create a new round
- result the last round
> Reports
  - lists of players, tournaments, rounds, matches...

## 3. How to generate  a flake8-html file

```bash
flake8 --format=html --htmldir=flake-report
```
- "index.html" will be stored in folder "flake-report".