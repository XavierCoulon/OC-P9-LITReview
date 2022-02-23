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
- visualisation d'un flux de tickets / critiques,
- recherche d'un livre via l'API Google Books (cf [google doc](https://developers.google.com/books/docs/v1/using))

## 2. <u> Documentation</u>

Sont disponibles sous le répertoire "[doc](doc)" les documents suivants, fournis par OC :
- Diagramme UML de la base de données (LITReview_UML_Diagram.pdf),
- Cahier des charges (LITReview_CDC.docx),
- Wireframes (LITReview_Wireframes.pdf).

## 3. <u> Installation</u>


```bash
git clone https://github.com/XavierCoulon/OC-P9-LITReview.git
cd OC-P9-LITReview
python3.9 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
Site accessible via http://127.0.0.1:8000/

## 4. <u> Données </u>

La base de données contient initialement 7 utilisateurs dont les login / password sont les suivants:
- user1 / passworduser1,
- user2 / passworduser2,
- user3 / passworduser3,
- user4 / passworduser4,
- user5 / passworduser5,
- user6 / passworduser6,
- user7 / passworduser7.