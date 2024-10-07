---

# API d'authentification avec FastAPI

## Description

**API d'authentification avec FastAPI** est un projet conçu pour permettre aux développeurs, qu'ils soient débutants ou expérimentés, de mettre en place rapidement un système d'authentification sécurisé. Ce projet utilise une architecture claire et évolutive avec des **routers**, des **services** pour la logique métier, et des **repositories** pour la gestion des interactions avec la base de données.

## Fonctionnalités

- **FastAPI** pour l'API rapide et performante.
- **SQLModel** pour l'ORM (compatibilité MySQL, PostgreSQL, SQLite).
- Intégration avec **Brevo** pour l'envoi d'emails (par exemple, codes de validation).
- Authentification sécurisée et validation de codes.

## Architecture

- **Routers** : Sépare les routes en modules.
- **Services** : Gère la logique métier.
- **Repositories** : Interface avec la base de données.
- **Models** : Géré via SQLModel pour un ORM simple et puissant.

## Prérequis

- Python 3.8+
- MySQL (ou PostgreSQL, SQLite en option)

## Installation

1. Clonez le repository :

```bash
git clone https://github.com/votre-utilisateur/fastapi_api.git
cd fastapi_api
```

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

3. Configurez votre base de données dans `config/db.py` :

```python
DATABASE_URL = "mysql://username:password@localhost/dbname"
# Vous pouvez modifier pour PostgreSQL ou SQLite
```

4. Démarrez l'application et créez les tables :

```bash
python main.py
```

## Utilisation

- L'API inclut des endpoints pour l'inscription, la connexion et la validation de code.
- Les emails de validation sont envoyés via Brevo. Assurez-vous de configurer correctement l'API Brevo.

## Exemple de configuration de l'envoi d'email

Dans `services/email_service.py`, configurez votre clé API Brevo :

```python
BREVO_API_KEY = "votre_cle_brevo"
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à forker ce projet, soumettre des pull requests, ou à l'adapter à vos besoins.
## Démarrage rapide
1. Clonez le projet et installez les dépendances.
2. Configurez la base de données.
3. Démarrez le serveur avec `uvicorn` :

```bash
uvicorn main:app --reload

---

