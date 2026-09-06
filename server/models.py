from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    # Table constraint: an exercise name should never be blank.
    __table_args__ = (
        CheckConstraint("name != ''", name='check_exercise_name_not_empty'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # An Exercise has many WorkoutExercises, and many Workouts through them.
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan'
    )

    # Model validation: category must be one of a known set of values.
    VALID_CATEGORIES = ('cardio', 'strength', 'flexibility', 'balance')

    @validates('category')
    def validate_category(self, key, value):
        if value not in self.VALID_CATEGORIES:
            raise ValueError(
                f"category must be one of {self.VALID_CATEGORIES}, got '{value}'"
            )
        return value

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty")
        return value

    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    # Table constraint: duration must be a positive number of minutes.
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # A Workout has many WorkoutExercises, and many Exercises through them.
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan'
    )

    # Model validation: duration_minutes must be a positive integer.
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("duration_minutes must be a positive integer")
        return value

    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes} min>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # A WorkoutExercise belongs to a Workout and belongs to an Exercise.
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def __repr__(self):
        return f'<WorkoutExercise {self.id}, workout={self.workout_id}, exercise={self.exercise_id}>'