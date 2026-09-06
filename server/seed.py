#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    # Clear existing data so re-running this script doesn't duplicate records.
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    # Create exercises
    push_up = Exercise(name='Push Up', category='strength', equipment_needed=False)
    squat = Exercise(name='Squat', category='strength', equipment_needed=False)
    running = Exercise(name='Running', category='cardio', equipment_needed=False)
    yoga_stretch = Exercise(name='Yoga Stretch', category='flexibility', equipment_needed=False)
    plank = Exercise(name='Plank', category='balance', equipment_needed=False)

    db.session.add_all([push_up, squat, running, yoga_stretch, plank])
    db.session.commit()

    # Create workouts
    workout1 = Workout(date=date(2026, 8, 1), duration_minutes=45, notes='Morning strength session')
    workout2 = Workout(date=date(2026, 8, 3), duration_minutes=30, notes='Quick cardio session')
    workout3 = Workout(date=date(2026, 8, 5), duration_minutes=20, notes='Recovery stretch day')

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()

    # Link exercises to workouts through WorkoutExercise
    db.session.add_all([
        WorkoutExercise(workout=workout1, exercise=push_up, reps=15, sets=3),
        WorkoutExercise(workout=workout1, exercise=squat, reps=12, sets=3),
        WorkoutExercise(workout=workout2, exercise=running, duration_seconds=1200),
        WorkoutExercise(workout=workout3, exercise=yoga_stretch, duration_seconds=900),
        WorkoutExercise(workout=workout3, exercise=plank, duration_seconds=60, sets=3),
    ])
    db.session.commit()

    print("Seed data created successfully!")