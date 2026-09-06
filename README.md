# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend API for tracking workouts and the
exercises performed within them. Built for personal trainers to log workouts,
maintain a reusable library of exercises, and record sets/reps/duration for
each exercise performed in a given workout.

## Description

This API manages three related resources:

- **Exercise** — a reusable exercise (e.g. Push Up, Running) with a name,
  category, and whether equipment is needed.
- **Workout** — a single workout session with a date, duration, and notes.
- **WorkoutExercise** — a join resource linking a `Workout` to an `Exercise`,
  recording reps, sets, and/or duration for that exercise within that workout.

A `Workout` has many `Exercises` through `WorkoutExercise`, and an `Exercise`
has many `Workouts` through `WorkoutExercise`, implemented with SQLAlchemy
association proxies. Marshmallow schemas serialize nested relationships while
avoiding infinite recursion by excluding circular back-references.

### Validations

- **Table constraints:** `Exercise.name` cannot be blank; `Workout.duration_minutes`
  must be greater than 0 (enforced at the database level).
- **Model validations:** `Exercise.category` must be one of `cardio`, `strength`,
  `flexibility`, `balance`; `Exercise.name` cannot be empty/whitespace;
  `Workout.duration_minutes` must be a positive integer.
- **Schema validations:** `Exercise.name` must have length >= 1;
  `Exercise.category` must be one of the allowed categories;
  `Workout.duration_minutes` must be >= 1.

## Installation

```bash
git clone https://github.com/moses-kebee/flask-sqlalchemy-workout-api.git
cd flask-sqlalchemy-workout-api
pipenv install
pipenv shell
cd server
```

## Database Setup

```bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
python seed.py
```

## Running the App

```bash
flask run --port=5555
```

The API will be available at `http://localhost:5555`.

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/workouts` | List all workouts, each with nested exercises |
| GET | `/workouts/<id>` | Get a single workout with its associated exercises |
| POST | `/workouts` | Create a workout. Body: `{"date": "YYYY-MM-DD", "duration_minutes": int, "notes": "string"}` |
| DELETE | `/workouts/<id>` | Delete a workout (and its associated workout-exercise links) |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise