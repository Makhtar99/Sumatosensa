# SmartSensors (SumatoSensa)

Une plateforme IoT complète pour la surveillance et la gestion de capteurs intelligents avec interface web moderne et architecture microservices.

## 🚀 Fonctionnalités

- **Tableau de bord en temps réel** - Surveillance des données des capteurs (température, humidité, pression)
- **Système d'authentification** - Inscription, connexion et gestion des utilisateurs
- **Gestion des dispositifs** - Configuration et monitoring des capteurs connectés
- **Alertes et notifications** - Système de notifications pour les seuils critiques
- **Export de données** - Export des données vers Excel/CSV
- **Interface responsive** - Application web moderne avec Vue.js et TailwindCSS
- **Communication MQTT** - Protocol IoT pour la communication avec les capteurs
- **Base de données TimescaleDB** - Stockage optimisé pour les données temporelles

## 🏗️ Architecture

```
SmartSensors/
├── backend/          # API FastAPI + MQTT
├── frontend/         # Interface Vue.js
├── database/         # Configuration TimescaleDB
├── mqtt/             # Broker Mosquitto
├── docs/             # Documentation
└── scripts/          # Scripts utilitaires
```

## 📋 Prérequis

- Docker et Docker Compose
- Python 3.8+ (pour le développement local)
- Node.js 18+ (pour le développement frontend)

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd SmartSensors
```

### 2. Variables d'environnement
Créer un fichier `.env` à la racine :
```env
POSTGRES_DB=sumatosensa
POSTGRES_USER=sumatosensa_user
POSTGRES_PASSWORD=your_secure_password
JWT_SECRET_KEY=your-super-secret-jwt-key
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

### 3. Démarrage avec Docker
```bash
# Production
docker-compose up -d

# Développement
docker-compose -f docker-compose.dev.yml up -d
```

L'application sera accessible sur :
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentation API: http://localhost:8000/docs

## 🔧 Développement

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev
```

### Tests
```bash
# Tests backend
cd backend
pytest

# Tests frontend
cd frontend
npm run test:unit
npm run test:e2e
```

## 📊 Services

- **TimescaleDB**: Base de données PostgreSQL optimisée pour les séries temporelles
- **Mosquitto**: Broker MQTT pour la communication IoT
- **FastAPI**: API REST backend avec authentification JWT
- **Vue.js**: Interface utilisateur moderne et responsive
- **Nginx**: Serveur web pour le frontend en production

## 🔐 Sécurité

- Authentification JWT avec expiration configurable
- Hachage des mots de passe avec bcrypt
- Variables d'environnement pour les secrets
- Validation des données avec Pydantic/Zod

## 📱 Interface utilisateur

- **Dashboard**: Vue d'ensemble des capteurs et données
- **Dispositifs**: Gestion des capteurs connectés
- **Historique**: Consultation des données passées
- **Alertes**: Configuration et suivi des notifications
- **Export**: Téléchargement des données
- **Paramètres**: Configuration du système

## 🔧 API Endpoints

- `POST /auth/login` - Authentification
- `POST /auth/register` - Inscription
- `GET /sensors/data` - Données des capteurs
- `GET /sensors/devices` - Liste des dispositifs
- `POST /admin/users` - Gestion utilisateurs (admin)

Documentation complète: http://localhost:8000/docs

## 🐛 Dépannage

### Problèmes courants
- **Erreur de connexion DB**: Vérifier les variables d'environnement
- **MQTT non accessible**: S'assurer que le port 1883 est disponible
- **Frontend ne charge pas**: Vérifier les variables VITE_*

### Logs
```bash
# Voir les logs des services
docker-compose logs -f [service_name]

# Logs spécifiques
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📝 Documentation

- [Architecture](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Déploiement](docs/deployment.md)
- [CI/CD](docs/ci-cd.md)

