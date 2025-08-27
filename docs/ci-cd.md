# CI/CD Pipeline - Sumātosensā

Cette documentation décrit l'infrastructure CI/CD mise en place pour le projet Sumātosensā.

## Vue d'ensemble

Le pipeline CI/CD est basé sur GitHub Actions et comprend :
- Tests automatiques pour le backend et frontend
- Build des images Docker
- Tests d'intégration end-to-end
- Déploiement automatique vers staging et production
- Scans de sécurité

## Structure des Workflows

### 1. CI Pipeline (`ci.yml`)

Déclenché sur :
- Push vers `main` et `develop`
- Pull requests vers `main` et `develop`

**Jobs :**
- `backend-tests`: Tests unitaires Python/FastAPI avec PostgreSQL et MQTT
- `frontend-tests`: Tests unitaires, linting, type checking et build Vue.js
- `docker-build`: Construction des images Docker (uniquement sur push)
- `e2e-tests`: Tests end-to-end avec Cypress (uniquement sur main)

### 2. Staging Deployment (`deploy-staging.yml`)

Déclenché sur :
- Push vers `develop`
- Déclenchement manuel

**Fonctionnalités :**
- Build et push des images vers GitHub Container Registry
- Tagging automatique (branch, SHA, staging)
- Configuration des variables d'environnement staging

### 3. Production Deployment (`deploy-production.yml`)

Déclenché sur :
- Publication d'une release
- Déclenchement manuel avec sélection de tag

**Fonctionnalités :**
- Scan de sécurité avec Trivy
- Environment de protection "production"
- Build et push des images avec tags de version
- Création d'un enregistrement de déploiement

## Configuration des Tests

### Backend Tests

**Dépendances de test :**
```txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
pytest-cov>=4.1.0
factory-boy>=3.3.0
faker>=19.0.0
pytest-mock>=3.11.0
```

**Services requis :**
- PostgreSQL (TimescaleDB)
- MQTT (Eclipse Mosquitto)

**Configuration :**
- Base de données de test isolée
- Variables d'environnement de test
- Coverage reporting avec Codecov

### Frontend Tests

**Scripts disponibles :**
```json
{
  "test:unit": "vitest",
  "test:e2e": "start-server-and-test preview http://localhost:4173 'cypress run --e2e'",
  "test:e2e:dev": "start-server-and-test 'vite dev --port 4173' http://localhost:4173 'cypress open --e2e'",
  "lint": "eslint . --fix",
  "type-check": "vue-tsc --build"
}
```

## Variables d'Environnement

### Secrets GitHub requis

- `GITHUB_TOKEN`: Token automatique pour accès au registry
- Variables d'environnement spécifiques au déploiement (à configurer selon l'infrastructure)

### Variables par environnement

**Test :**
```yaml
POSTGRES_DB: sumatosensa_test
POSTGRES_USER: test_user
POSTGRES_PASSWORD: test_password
SECRET_KEY: test-secret-key-for-ci
```

**Staging :**
```yaml
VITE_API_URL: https://api-staging.sumatosensa.com
VITE_WS_URL: wss://api-staging.sumatosensa.com/ws
```

**Production :**
```yaml
VITE_API_URL: https://api.sumatosensa.com
VITE_WS_URL: wss://api.sumatosensa.com/ws
```

## Images Docker

Les images sont stockées dans GitHub Container Registry :
- `ghcr.io/{owner}/{repo}-backend`
- `ghcr.io/{owner}/{repo}-frontend`

**Tags :**
- Staging: `develop`, `develop-{sha}`, `staging`
- Production: `{version}`, `latest`

## Sécurité

- Scan de vulnérabilités avec Trivy avant déploiement production
- Environment de protection pour la production
- Images construites avec cache GitHub Actions
- Secrets gérés via GitHub Secrets

## Utilisation

### Développement
1. Créer une branche feature
2. Les tests s'exécutent automatiquement sur les PR
3. Merger vers `develop` déclenche le déploiement staging

### Release
1. Créer une release depuis `main`
2. Le déploiement production s'exécute automatiquement
3. Possibilité de déploiement manuel avec sélection de tag

### Commandes locales

**Backend :**
```bash
cd backend
pip install -r requirements-dev.txt
pytest tests/ -v --cov=app
```

**Frontend :**
```bash
cd frontend
npm install
npm run test:unit
npm run lint
npm run type-check
npm run build
```

## Monitoring

- Couverture de code avec Codecov
- Logs des workflows disponibles dans GitHub Actions
- Historique des déploiements dans l'onglet Environments

## Troubleshooting

**Tests backend échouent :**
- Vérifier la connexion PostgreSQL/MQTT
- Contrôler les variables d'environnement
- Examiner les logs pytest

**Build Docker échoue :**
- Vérifier les Dockerfiles
- Contrôler les dépendances
- Examiner les logs de build

**Déploiement bloqué :**
- Vérifier les secrets GitHub
- Contrôler les permissions du registry
- Examiner les logs de déploiement