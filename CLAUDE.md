# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Campus Activity Management System - a WeChat mini-program application for managing campus clubs and activities.

- **Frontend**: UniApp Vue 3 WeChat mini-program (`frontend/`)
- **Backend**: FastAPI REST API (Python 3.13, SQLAlchemy, MySQL) (`backend/`)
- **Database**: MySQL `ljy` schema (schema/seed data in `ljy.sql` at the repository root)

## Build & Run Commands

### Backend (backend/)

```powershell
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload --reload-dir app
```

Or use the `FastAPI (app.main:app :8080)` debug configuration. Dependencies live in `backend/.venv` (see `backend/requirements.txt`); manage them with `backend\.venv\Scripts\python.exe -m pip ...`.

### Frontend (frontend/)

HBuilderX IDE is required for development. Key configurations in `manifest.json`:
- App ID: `__UNI__D37EE2B`
- WeChat mini-program App ID: `wx2caaaf47aead807a`

## Architecture

### Backend Structure

```
backend/app/
├── api/            # REST endpoints (/api/*): user, club, activity, campus
├── services/       # Business logic
├── schemas/        # Pydantic request/response models (camelCase field names)
├── models/         # SQLAlchemy entities
├── core/           # respones.py (unified response helpers), middleware, context, exceptions
├── db/             # database.py (engine/session, get_db)
└── utils/          # time_util.py (millisecond timestamp conversion)
```

**Key entities**: `User`, `Club`, `ClubMember`, `Activity`, `ActivityRegistration`, `ActivityCheckin`

**API prefix**: `/api/activities`, `/api/clubs`, `/api/users`, `/api/campus-info`

**Layered flow**: `api/` (router) → `services/` (business logic) → `models/` → database

**Response format**: All APIs return `{code, message, success, data}` (see `app/core/respones.py`). Paginated results wrap in `page` with `{total, currentPage, pageSize, totalPage, records[]}`. Time fields (registrationStartTime, startTime, endTime, etc.) are Unix timestamps in milliseconds, converted via `app/utils/time_util.py`.

Endpoints may declare `response_model=ApiResponse[...]` using the generic wrapper `ApiResponse` in `app/core/respones.py`; field names in those models match the camelCase keys produced by the serializers.

### Frontend Structure

```
frontend/
├── api/               # API call wrappers
├── pages/
│   ├── activity/      # Activity browsing & details
│   ├── clubList/      # Club browsing
│   ├── user/          # User dashboard, my activities/clubs
│   ├── index/         # Home page, search
│   ├── scanCode/      # QR check-in
│   └── system/        # Login, registration
├── static/            # Images, fonts
├── uni_modules/       # uni-icons, uni-search-bar, uni-notice-bar
└── manifest.json      # Platform config (mp-weixin)
```

API base URL is defined in `frontend/utils/request.js` (`BASE_URL`), currently `http://localhost:8080/api`.

## Key Patterns

### Activity Lifecycle
Activities flow through states: `审核中` → `已通过/已拒绝` → `报名中/等待中/进行中/已结束`

Check-in requires: (1) approved registration, (2) activity within start/end time window, (3) QR code scan

### Permission Model
- RBAC tables: `user_role` → `role` → `role_permission` → `permission`
- `user_role.club_id = 0` means a global role; a non-zero value scopes the role to that club
- Roles: `ADMIN` (global super admin), `CLUB_MANAGER` (club-scoped), `USER` (basic logged-in user)
- Authorization uses `assert_permission` / `require_permission`; `club_member.is_manager` is membership/display data only
- `user.is_boss` / `user.is_manager` no longer exist

### Image Storage
Image URLs stored as comma-separated strings in database (e.g., `"url1,url2,url3"`)
