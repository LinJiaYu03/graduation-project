# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Campus Activity Management System - a dual-platform application for managing campus clubs and activities.

- **Backend**: Spring Boot REST API (Java 17, MyBatis-Plus, MySQL)
- **Frontend**: UniApp Vue 3 WeChat mini-program

## Build & Run Commands

### Backend (project-system)

```bash
cd project-system
./mvnw spring-boot:run        # Development (runs on port 8080)
./mvnw clean package           # Build JAR
./mvnw test                    # Run tests
```

**Database**: MySQL `ljy` schema (configured in `application.yml`)

**Response format**: All APIs return `Results` object with `{code, message, success, data}`. Paginated results wrap in `PageResult` with `{total, currentPage, pageSize, totalPage, records[]}`. Time fields (registrationStartTime, startTime, endTime, etc.) are Unix timestamps in milliseconds.

### Frontend (campus_activity)

HBuilderX IDE is required for development. Key configurations in `manifest.json`:
- App ID: `__UNI__D37EE2B`
- WeChat mini-program App ID: `wx2caaaf47aead807a`

## Architecture

### Backend Structure

```
project-system/src/main/java/com/example/projectsystem/
├── commons/            # Results, PageResult (统一响应封装)
├── config/             # CrossOriginConfig, MybatisPlusConfig
├── controller/         # REST endpoints (/api/*)
├── service/Impl/       # Business logic implementations
├── mapper/             # MyBatis-Plus mappers
├── domain/             # Entity classes
├── dto/                # Request/Response objects
├── exception/          # GlobalExceptionHandler
└── util/               # QrCodeUtil (ZXing QR码生成)
```

**Key domains**: `User`, `Club`, `ClubMember`, `Activity`, `ActivityRegistration`, `ActivityCheckin`

**API prefix**: `/api/activities`, `/api/clubs`, `/api/users`, `/api/campus-info`

**Layered flow**: Controller → Service → Mapper → Database

### Frontend Structure

```
campus_activity/
├── pages/
│   ├── activity/       # Activity browsing & details
│   ├── clubList/       # Club browsing
│   ├── user/           # User dashboard, my activities/clubs
│   ├── index/         # Home page, search
│   ├── scanCode/      # QR check-in
│   └── system/        # Login, registration
├── static/            # Images, fonts
├── uni_modules/       # uni-icons, uni-search-bar, uni-notice-bar
└── manifest.json     # Platform config (mp-weixin)
```

## Key Patterns

### Activity Lifecycle
Activities flow through states: `审核中` → `已通过/已拒绝` → `报名中/等待中/进行中/已结束`

Check-in requires: (1) approved registration, (2) activity within start/end time window, (3) QR code scan

### Permission Model
- `isBoss=true` users: super admins (can review activities)
- `isManager=true` in ClubMember: club administrators (manage club activities, review registrations)

### Image Storage
Image URLs stored as comma-separated strings in database (e.g., `"url1,url2,url3"`)

### Time Handling
LocalDateTime stored in database; API converts to Unix timestamps (ms) for frontend consumption via `ZoneId.systemDefault().toInstant().toEpochMilli()`
