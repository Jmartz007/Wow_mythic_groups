---
applyTo: "**"
---

# Copilot Instructions for Wow Mythic Groups

## Project Overview

This repository is a full-stack application for managing World of Warcraft Mythic+ groups, with a Flask backend and a React/TypeScript frontend. The backend integrates with Blizzard's Battle.net API for character/account data.

## Architecture

### Backend (Backend-Flask)

-Flask app with modular blueprints: auth, playersview, Oauth, dungeonsviews, wow_profile.
-Service layer (service/) handles business logic, e.g., CharacterService.py for character CRUD.
-Data access via datagatherer/ modules.
-API endpoints are registered in **init**.py and exposed via blueprints.
-External integration: Blizzard API via OAuth2, with access tokens managed in the backend and used for API calls.
-CORS is enabled for local frontend development (http://localhost:5173).
###Frontend (Frontend-React)
-React + TypeScript, built with Vite.
-Main pages in src/pages/, components in src/components/.
-Data tables and selection UIs use MUI and custom table components.
-Communicates with backend via REST API endpoints (e.g., /groups/api/profile/import-characters).

## Developer Workflows

### Backend

-Start Flask app (see **init**.py for app factory).
-Environment variables managed via .env and dotenv.
-Logging is verbose; all requests and errors are logged.
-Error handling uses custom exceptions (utils/customexceptions.py).
-Docker build/push workflow in docker-push-image.yml (uses version from **init**.py).

### Frontend

-Start with Vite (npm run dev).
-TypeScript strictness and ESLint rules are recommended (see README.md).
-API calls use fetch; authentication tokens are passed in Authorization headers.

## Patterns & Conventions

-Blueprints: Each major backend feature is a Flask blueprint, registered in **init**.py.
-Service Layer: Business logic is separated from route handlers (see CharacterService.py).
-Error Handling: Use custom exceptions and error handlers for API responses.
-API Auth: Frontend sends JWT for app auth; backend uses Blizzard OAuth token for Blizzard API calls.
-Character Import: Frontend collects selected characters and POSTs them to a backend endpoint for DB import (see -CharacterSelect.tsx).
-Data Table: Use DataTable.tsx for displaying and interacting with tabular data.

## Integration Points

-Blizzard API: All calls use OAuth2 access tokens; see wow_profile.py for fetching character/account data.
-Docker: CI builds and pushes backend images to Docker Hub on main branch pushes.

## Examples

-Registering a Blueprint:

```python
from .wow_profile import wow_profile as wow_profile_bp
app.register_blueprint(wow_profile_bp)
```

-Frontend API Call:

```typescript
fetch("/groups/api/profile/import-characters", {
  headers: { Authorization: `Bearer ${accessToken}` },
});
```

## Key Files

-**init**.py: App factory, blueprint registration, error handling.
-wow_profile.py: Blizzard API integration.
-CharacterService.py: Character business logic.
-CharacterSelect.tsx: Character selection and import logic.
-docker-push-image.yml: CI/CD for backend Docker images.
