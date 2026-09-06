from marshmallow import Schema, fields, validate, ValidationError


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    category = fields.String(
        required=True,
        validate=validate.OneOf(["cardio", "strength", "flexibility", "balance"])
    )
    equipment_needed = fields.Boolean()

    workouts = fields.List(
        fields.Nested(lambda: WorkoutSchema(exclude=("exercises",))),
        dump_only=True
    )


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))
    notes = fields.String()

    exercises = fields.List(
        fields.Nested(lambda: ExerciseSchema(exclude=("workouts",))),
        dump_only=True
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
