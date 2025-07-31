# Configuration Railway - Sumātosensā

Guide pour configurer le déploiement automatique sur Railway.

## Étape 1 : Créer les projets Railway

1. **Aller sur [railway.app](https://railway.app)**
2. **Se connecter avec GitHub**
3. **Créer 2 projets :**
   - `sumatosensa-staging`
   - `sumatosensa-production`

## Étape 2 : Configurer chaque projet

### Pour chaque projet, ajouter 3 services :

#### 1. Service Backend
- **Type** : GitHub Repo
- **Repo** : Votre repository
- **Root Directory** : `backend`
- **Build Command** : Automatique (Dockerfile)

#### 2. Service Frontend  
- **Type** : GitHub Repo
- **Repo** : Votre repository
- **Root Directory** : `frontend` 
- **Build Command** : Automatique (Dockerfile)

#### 3. Service PostgreSQL
- **Type** : PostgreSQL Database
- **Version** : Latest

## Étape 3 : Variables d'environnement

### Backend (dans Railway)

**Staging :**
```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
MQTT_BROKER_HOST=test.mosquitto.org
MQTT_BROKER_PORT=1883
SECRET_KEY=staging-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=8
CORS_ORIGINS=https://your-frontend-staging.railway.app
PORT=8000
```

**Production :**
```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
MQTT_BROKER_HOST=your-mqtt-broker.com
MQTT_BROKER_PORT=1883
SECRET_KEY=production-secret-key-very-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=8
CORS_ORIGINS=https://your-frontend-production.railway.app
PORT=8000
```

### Frontend (dans Railway)

**Staging :**
```env
VITE_API_URL=https://your-backend-staging.railway.app
VITE_WS_URL=wss://your-backend-staging.railway.app/ws
```

**Production :**
```env
VITE_API_URL=https://your-backend-production.railway.app
VITE_WS_URL=wss://your-backend-production.railway.app/ws
```

## Étape 4 : Secrets GitHub

Dans **Settings > Secrets and variables > Actions**, ajouter :

### Staging
```
RAILWAY_TOKEN_STAGING=<token-from-railway-settings>
RAILWAY_BACKEND_SERVICE_ID_STAGING=<service-id-backend>
RAILWAY_FRONTEND_SERVICE_ID_STAGING=<service-id-frontend>
```

### Production  
```
RAILWAY_TOKEN_PRODUCTION=<token-from-railway-production>
RAILWAY_BACKEND_SERVICE_ID_PRODUCTION=<service-id-backend-prod>
RAILWAY_FRONTEND_SERVICE_ID_PRODUCTION=<service-id-frontend-prod>
```

## Étape 5 : Obtenir les tokens et IDs

### Railway Token
1. **Railway Dashboard** > **Account Settings** > **Tokens**
2. **Create New Token** > Copier le token

### Service IDs
1. **Dans chaque service Railway**
2. **Settings** > **General** 
3. **Copier le Service ID**

## Étape 6 : Premier déploiement

### Manuel (pour tester)
```bash
# Installer Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login
railway login

# Déployer backend
cd backend
railway link <service-id>
railway up

# Déployer frontend
cd ../frontend  
railway link <service-id>
railway up
```

### Automatique
- **Push vers `main`** → Déploiement staging
- **Créer Release** → Déploiement production

## URLs d'accès

Après déploiement, Railway génère des URLs :
- **Backend** : `https://your-backend.railway.app`
- **Frontend** : `https://your-frontend.railway.app`
- **API Docs** : `https://your-backend.railway.app/docs`

## Monitoring

- **Logs** : Railway Dashboard > Service > Deployments > Logs
- **Métriques** : Railway Dashboard > Service > Observability
- **Base de données** : Railway Dashboard > PostgreSQL > Data

## Troubleshooting

**Build échoue :**
- Vérifier les Dockerfiles
- Contrôler les variables d'environnement
- Examiner les logs Railway

**Connexion DB échoue :**
- Vérifier `DATABASE_URL` dans les variables
- Contrôler que PostgreSQL est bien créé

**Frontend ne charge pas :**
- Vérifier `VITE_API_URL` et `VITE_WS_URL`
- Contrôler CORS dans le backend

## Coûts Railway

- **Gratuit** : 500h/mois, 1GB RAM, 1GB stockage
- **Dépassement** : $0.000463/GB-heure
- **PostgreSQL** : Inclus dans le plan gratuit