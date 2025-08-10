# Configuration Render - Sumātosensā

Guide pour déployer automatiquement sur Render.

## Étape 1 : Créer un compte Render

1. Aller sur [render.com](https://render.com)
2. **Sign up with GitHub**
3. Autoriser l'accès à vos repositories

## Étape 2 : Déploiement automatique

### Méthode simple (recommandée)
1. **New** > **Blueprint**
2. **Connect GitHub repository**
3. Sélectionner votre repo `Sumatosensa`
4. Render détecte automatiquement le fichier `render.yaml`
5. **Apply Blueprint**

### Services créés automatiquement
- **sumatosensa-backend** : API FastAPI
- **sumatosensa-frontend** : Interface Vue.js
- **sumatosensa-db** : Base de données PostgreSQL

## Étape 3 : URLs d'accès

Après déploiement, Render génère :
- **Backend** : `https://sumatosensa-backend.onrender.com`
- **Frontend** : `https://sumatosensa-frontend.onrender.com`
- **API Docs** : `https://sumatosensa-backend.onrender.com/docs`

## Configuration incluse

### Backend
- **Port** : Automatique (variable $PORT)
- **Health Check** : `/health`
- **Base de données** : PostgreSQL connectée automatiquement
- **MQTT** : Broker de test (test.mosquitto.org)

### Frontend  
- **Build** : Multi-stage Docker avec Nginx
- **Routing** : SPA routing configuré
- **Cache** : Assets statiques optimisés
- **Sécurité** : Headers de sécurité inclus

### Base de données
- **PostgreSQL** : Plan gratuit (90 jours puis $7/mois)
- **Connection** : Automatique via `DATABASE_URL`
- **Backup** : Quotidien automatique

## Plan gratuit Render

- **750 heures/mois** par service
- **512 MB RAM** par service
- **Base de données** : 90 jours gratuit puis payant
- **SSL** : Inclus
- **Custom domains** : Inclus

## Déploiement automatique

- **Push vers `main`** → Déploiement automatique
- **Pull Request** → Tests uniquement
- **Release** → Déploiement production

## Variables d'environnement

Configurées automatiquement via `render.yaml` :

```yaml
# Backend
DATABASE_URL: Auto-générée
MQTT_BROKER_HOST: test.mosquitto.org
SECRET_KEY: Auto-générée

# Frontend
VITE_API_URL: Auto-reliée au backend
VITE_WS_URL: Auto-configurée
```

## Monitoring

- **Logs** : Dashboard Render > Service > Logs
- **Métriques** : Dashboard > Service > Metrics
- **Events** : Dashboard > Service > Events
- **Health** : Auto-monitoring avec `/health`

## Mise à jour

Pour mettre à jour la configuration :
1. Modifier `render.yaml`
2. Commit et push
3. Render applique automatiquement les changements

## Troubleshooting

**Build échoue :**
- Vérif Dockerfile dans logs Render
- Contrôler les dépendances package.json/requirements.txt

**Service ne démarre pas :**
- Vérifier les logs de démarrage
- Contrôler la variable `PORT` pour le backend
- Vérifier `DATABASE_URL`

**Frontend erreur 404 :**
- Contrôler `nginx.conf`
- Vérifier le build `npm run build`
- Examiner les logs Nginx

**Base de données inaccessible :**
- Vérifier `DATABASE_URL` dans les variables
- Contrôler l'état du service PostgreSQL
- Regarder les logs de connexion

## Migration depuis Railway

1. **Exporter les données** Railway si nécessaire
2. **Supprimer les services** Railway
3. **Déployer sur Render** avec cette configuration
4. **Importer les données** dans PostgreSQL Render

## Coûts

- **Web Services** : Gratuit 750h/mois, puis $7/mois
- **PostgreSQL** : 90 jours gratuit, puis $7/mois
- **Bandwidth** : 100GB/mois inclus
- **Build minutes** : 500/mois inclus