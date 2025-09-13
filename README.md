# Entretien Technique – DevOps / Systèmes

Ce projet est un exercice conçu pour tester des compétences orientées **administration système** et **DevOps** à travers une petite application FastAPI.

---

## Objectif

L’objectif est de manipuler une API FastAPI qui :
- Génère un **token éphémère** (valide 1 seconde) visible dans un ASCII art.
- Demande une petite transformation du token avant usage.
- Protège l’accès à son propre code source avec ce token.
- S’exécute dans un conteneur Docker et via docker-compose.

---

## Instructions de l’exercice

### Étape 1 : Découverte de l’API
- Faites un `GET /` pour lire les instructions.
- Faites un `GET /token` pour récupérer un token éphémère.

### Étape 2 : Transformation du token
- Le token est modifié volontairement.
- Vous devez :
  - Remplacer toutes les lettres **`Z` par `A`**
  - Convertir le token en **minuscules**

### Étape 3 : Authentification
- Faites un `POST /token` avec le header :
  ```
  Authorization: Bearer <token_transformé>
  ```
- Si le token est correct et encore valide, l’API retourne le **code source du script**.

### Étape 4 : Poursuite
- Une fois le code source obtenu, vous découvrirez un endpoint supplémentaire en `GET /custom-tasks/{ENTREPRISE}`
- Cette endpoint contient des tâches supplémentaires customisable par variables d'env

---

## Configuration du test

Le test ce configure avec des variables d'environnement:
- `TT_COMPANY` (default: 'THOSTED')
- `TT_CUSTOMTASKS` (default: None)

l'ascii art ainsi que l'endpoint des tâches customs dépend de `TT_COMPANY`.

les taches supplémentaires sont séparées par `\n\n` et afficher dans l'endpoint des tâches customs. (exemple dans le docker-compose)

---

## Installation & Exécution
### Avec docker seul
Construire l’image :
```bash
docker build -t entretien-technique .
docker run -p 8000:8000 entretien-technique
```


### Avec docker-compose
```bash
docker-compose up --build
```

API disponible sur : [http://localhost:8000](http://localhost:8000)

---

## Tâches additionnelles possibles

- **Dockerfile** : rédiger un Dockerfile et un docker-compose.
- **Reverse proxy** : déployer derrière Nginx ou Traefik.
- **Monitoring** : ajouter Prometheus + Grafana.
- **CI/CD** : automatiser build, tests et push sur Docker Hub.
- **Kubernetes** : préparer un manifeste YAML pour déploiement en cluster.

---

## 📄 Licence
Ce projet est publié sous licence **MIT**. Vous êtes libre de l’utiliser, le modifier et le redistribuer.
