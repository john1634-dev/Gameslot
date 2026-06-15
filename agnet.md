# Gameslot Project Agent Notes

## Project Overview

Gameslot is a Django project with a Vue frontend.

- Backend: Django 6.0.6
- Admin UI: django-simpleui 2026.1.13
- Frontend: Vue 3 with Vite
- Database: SQLite, stored locally as `db.sqlite3`

## Directory Layout

- `Gameslot/`: Django project settings and root URL configuration
- `slots/`: Django app for project-specific backend code
- `frontend/`: Vue 3 frontend source code
- `static/frontend/`: Built Vue frontend served by Django
- `.venv/`: Local Python virtual environment
- `requirements.txt`: Python dependencies
- `manage.py`: Django command entry point

## Backend Commands

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run Django checks:

```powershell
python manage.py check
```

Run migrations:

```powershell
python manage.py migrate
```

Start Django development server:

```powershell
python manage.py runserver
```

Backend URLs:

- Frontend site: `http://127.0.0.1:8000/`
- Admin site: `http://127.0.0.1:8000/admin/`

## Frontend Commands

Install frontend dependencies:

```powershell
cd frontend
npm install
```

Run Vue development server:

```powershell
npm run dev
```

Build Vue frontend for Django:

```powershell
npm run build
```

The production build outputs to:

```text
static/frontend/
```

After changing Vue files, run `npm run build` so Django can serve the updated frontend from `/`.

## Integration Notes

- Django renders the Vue entry page from `static/frontend/index.html`.
- `Gameslot/settings.py` includes `BASE_DIR / 'static' / 'frontend'` in `TEMPLATES['DIRS']`.
- `STATICFILES_DIRS` points to `BASE_DIR / 'static'`.
- `Gameslot/urls.py` maps `/` to `slots.views.frontend`.
- `/admin/` remains handled by Django admin with Simple UI.

## Admin User

Current superuser:

- Username: `john1634`
- Email: `genshin1634@gmail.com`
- Nickname: `CS`

## Development Guidelines

- Keep Django backend logic in `slots/`.
- Keep Vue source changes in `frontend/src/`.
- Do not edit generated files in `static/frontend/` by hand; rebuild from `frontend/`.
- Do not commit `.venv/`, `node_modules/`, `db.sqlite3`, or log files.
- Run these checks before considering a change complete:

```powershell
.\.venv\Scripts\python.exe manage.py check
cd frontend
npm run build
```
