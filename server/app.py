from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/workouts", methods=["GET", "POST"])
def workouts():
    if request.method == "GET":
        all_workouts = Workout.query.all()
        return make_response(workouts_schema.dump(all_workouts), 200)

    if request.method == "POST":
        data = request.get_json()
        try:
            validated = workout_schema.load(data)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            new_workout = Workout(
                date=validated["date"],
                duration_minutes=validated["duration_minutes"],
                notes=validated.get("notes"),
            )
            db.session.add(new_workout)
            db.session.commit()
        except ValueError as err:
            db.session.rollback()
            return make_response(jsonify({"errors": [str(err)]}), 400)

        return make_response(workout_schema.dump(new_workout), 201)


@app.route("/workouts/<int:id>", methods=["GET", "DELETE"])
def workout_by_id(id):
    workout = Workout.query.filter_by(id=id).first()

    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    if request.method == "GET":
        return make_response(workout_schema.dump(workout), 200)

    if request.method == "DELETE":
        db.session.delete(workout)
        db.session.commit()
        return make_response(jsonify({}), 204)


@app.route("/exercises", methods=["GET", "POST"])
def exercises():
    if request.method == "GET":
        all_exercises = Exercise.query.all()
        return make_response(exercises_schema.dump(all_exercises), 200)

    if request.method == "POST":
        data = request.get_json()
        try:
            validated = exercise_schema.load(data)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            new_exercise = Exercise(
                name=validated["name"],
                category=validated["category"],
                equipment_needed=validated.get("equipment_needed", False),
            )
            db.session.add(new_exercise)
            db.session.commit()
        except ValueError as err:
            db.session.rollback()
            return make_response(jsonify({"errors": [str(err)]}), 400)

        return make_response(exercise_schema.dump(new_exercise), 201)


@app.route("/exercises/<int:id>", methods=["GET", "DELETE"])
def exercise_by_id(id):
    exercise = Exercise.query.filter_by(id=id).first()

    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    if request.method == "GET":
        return make_response(exercise_schema.dump(exercise), 200)

    if request.method == "DELETE":
        db.session.delete(exercise)
        db.session.commit()
        return make_response(jsonify({}), 204)


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    if not workout or not exercise:
        return make_response(jsonify({"error": "Workout or Exercise not found"}), 404)

    data = request.get_json() or {}

    new_workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds"),
    )
    db.session.add(new_workout_exercise)
    db.session.commit()

    return make_response(workout_exercise_schema.dump(new_workout_exercise), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
