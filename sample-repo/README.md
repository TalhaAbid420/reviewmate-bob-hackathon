# Task Manager API (Sample Repo)

A small Express.js API used as the demo target for **ReviewMate**
(IBM Bob 2.0 Hackathon).

## Endpoints
- `POST /tasks` — create a task (`{ "title": "..." }`)
- `GET /tasks/:id` — fetch a task by id
- `DELETE /tasks/:id` — delete a task by id

## Setup
```
npm install
npm start      # runs on http://localhost:3000
npm test       # runs the test suite
```

## Seeded issues (for the ReviewMate demo)
This repo intentionally contains two issues for ReviewMate's subagents to catch:

1. **No input validation** on `POST /tasks` — `title` is accepted even if
   missing, empty, or not a string. (`src/routes/tasks.js`)
2. **No test coverage** for `DELETE /tasks/:id` — only `POST` and `GET`
   are tested. (`tests/tasks.test.js`)

These are deliberate, for demo purposes — not real production issues.
