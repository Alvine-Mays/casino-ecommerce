# Casino E-commerce — Intégration Front (Vite) ↔ Back (Django)

Ce document décrit la configuration d’intégration entre le frontend (Vite/React) et le backend (Django), ainsi que les tests rapides pour valider la connectivité en développement.

## Aperçu
- Backend: Django — http://127.0.0.1:8000 (dev)
- Frontend client (Vite): http://127.0.0.1:5173
- Frontend staff (Vite): http://127.0.0.1:5174
- Endpoint de santé: `GET /api/health/` → `{ "status": "ok" }`

## Variables d’environnement
### Backend (.env à la racine du repo)
Voir `./.env.example` (copiez-le en `.env`). Principales variables:
- `DEBUG`: Active le mode debug en dev (True/False).
- `SECRET_KEY`: Clé secrète Django (mettez une vraie valeur en prod).
- `ALLOWED_HOSTS`: Hôtes autorisés (ex: `localhost,127.0.0.1`).
- `DB_ENGINE`: `sqlite3` par défaut en dev/tests (simple et sans dépendance).
- `SQLITE_NAME` (optionnel): chemin du fichier SQLite (par défaut `./db.sqlite3`).
- `CORS_ALLOW_ALL`: `0` en dev pour restreindre aux origines listées.
- `CORS_ALLOWED_ORIGINS`: 
  `http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174`
- `CSRF_TRUSTED_ORIGINS`: mêmes origines que ci-dessus.
- `CORS_ALLOW_CREDENTIALS`: `1` pour autoriser l’envoi de cookies/headers cross-origin.
- `CLIENT_URL`: origine du client (utile pour certains liens sortants).

### Frontend (Vite)
- `frontend/client/.env.development` → `VITE_API_URL=http://127.0.0.1:8000`
- `frontend/staff/.env.development` → `VITE_API_URL=http://127.0.0.1:8000`

Ces valeurs sont lues par le client HTTP centralisé (`src/lib/api.js`) via `import.meta.env.VITE_API_URL`.

## Installation rapide
### Backend
1) Créez le fichier `.env` à partir de `.env.example` (SQLite par défaut):
```
cp .env.example .env
```
2) Installez les dépendances Python minimales (exemple pip):
```
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-filter channels channels-redis python-json-logger redis celery
```
3) Appliquez les migrations et lancez le serveur (ASGI, Channels):
```
python manage.py makemigrations
python manage.py migrate

# Dév simple:
python manage.py runserver 127.0.0.1:8000
# Prod (exemple): daphne -b 0.0.0.0 -p 8000 backend.config.asgi:application
```

### Frontend client (Vite)
```
cd frontend/client
cp .env.example .env.development  # si besoin
npm install
npm run dev  # http://127.0.0.1:5173
```

### Frontend staff (Vite)
```
cd frontend/staff
cp .env.example .env.development  # si besoin
npm install
npm run dev  # http://127.0.0.1:5174
```

## Tests
### Test unitaire backend (endpoint de santé)
```
python manage.py test tests.test_health
```
Attendu: statut 200 et `{ "status": "ok" }`.

### Smoke test d’intégration (frontend → backend)
Depuis `frontend/client` (le backend doit être démarré sur `VITE_API_URL`):
```
npm run test:integration
```
Le script lit `VITE_API_URL` et effectue un `GET ${VITE_API_URL}/api/health/`.

## Détails techniques
- CORS/CSRF: configurés pour accepter les origines Vite 5173/5174 et autoriser `withCredentials`.
- Client HTTP centralisé: `frontend/*/src/lib/api.js` (Axios), utilise `VITE_API_URL`.
- Auth côté client: intercepteurs sur le client central pour injecter le Bearer token et rediriger sur 401.
- Endpoint de santé: `backend/config/urls.py` → `api/health/`.

## Journalisation (logs)
- Format JSON via `python-json-logger` (stdout): niveau INFO par défaut.
- Corrélation: `RequestIdMiddleware` ajoute/retourne `X-Request-ID`.
- Traçabilité requêtes: `RequestLoggingMiddleware` journalise méthode, chemin, statut, durée, user et IP (`logger` "request").
- Configuration: voir `config/settings/base.py` (section LOGGING) et `config/middleware.py`.

## Staff — Dashboard par sections
- Navigation côté staff: `/orders`, `/products`, `/inventory`, `/categories`, `/users`.
- Commandes: page existante (préparer/prête) avec rafraîchissement via WebSocket.
- Produits: liste + recherche; création via `POST /api/catalog/staff/products`.
- Stocks: liste `/api/inventory/staff/inventory` + ajustements via PATCH `/api/inventory/staff/inventory/<product_id>`.
- Catégories: liste + création via `POST /api/catalog/staff/categories` (image_url optionnelle). Si aucune image, le front affiche un visuel par défaut.
- Import: `/api/catalog/staff/import` (CSV/JSON/Excel) pour importer des produits/prix en masse (colonnes name, category, price).
- Utilisateurs: liste + recherche via `/api/auth/staff/users`.

Accès: nécessite un utilisateur staff (voir `accounts.permissions.IsStaffRole`).

## Paiements: CinetPay + MTN Mobile Money (CG)
- Provider par défaut: `PAYMENT_PROVIDER=cinetpay` (ou `mtn_momo` pour MTN).
- MTN MoMo (mode maquette si non configuré): variables d’environnement à définir pour activer l’appel réel:
  - `MTN_MOMO_BASE_URL` (ex: `https://sandbox.momodeveloper.mtn.com`)
  - `MTN_MOMO_SUBSCRIPTION_KEY`
  - `MTN_MOMO_API_USER`
  - `MTN_MOMO_API_KEY`
  - `MTN_MOMO_TARGET_ENV` (sandbox|production)
  - `MTN_MOMO_CURRENCY` (par défaut XAF)

## SMS (MTN)
- Provider: MTN (mode maquette si variables absentes).
- Variables d’environnement:
  - `MTN_SMS_BASE_URL` (ex: `https://api.mtn.com/sms`)
  - `MTN_SMS_API_KEY` (ou `MTN_SMS_SUBSCRIPTION_KEY`)
  - `MTN_SMS_SENDER` (SenderID/shortcode; défaut `GCShop`)
- Implémentation: voir `backend/apps/notifications/sms.py`.

## Déploiement (production)
### Pré-requis
- Redis (Channels + Celery): `REDIS_URL`
- Base de données (SQLite par défaut; MySQL possible)
- Reverse proxy (Nginx) en frontal

### Étapes
1) Copier `.env` et mettre `DEBUG=False`, configurer `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `CORS_ALLOWED_ORIGINS`.
2) Activer la sécurité: `SECURE_SSL_REDIRECT=1`, `SESSION_COOKIE_SECURE=1`, `CSRF_COOKIE_SECURE=1`, HSTS si HTTPS.
3) Installer deps, migrer, collecter statiques:
```
pip install -r requirements.txt  # ou pip install ... (liste ci-dessus)
python manage.py migrate
python manage.py collectstatic --noinput
```
4) Lancer l’ASGI (Channels) avec daphne/uvicorn + superviser (systemd):
```
daphne -b 0.0.0.0 -p 8000 backend.config.asgi:application
```
5) Lancer Celery worker + beat:
```
celery -A backend.config.celery worker -l info
celery -A backend.config.celery beat -l info
```
6) Construire les frontends et servir avec Nginx:
```
cd frontend/client && npm ci && npm run build
cd ../staff && npm ci && npm run build
```

## Dépannage
- Erreurs CORS: vérifiez `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS` et `withCredentials`.
- 401/403: en dev, assurez-vous que les tokens sont présents ou testez une route publique.
- Échec du smoke test: assurez-vous que le backend est démarré sur `VITE_API_URL`.


