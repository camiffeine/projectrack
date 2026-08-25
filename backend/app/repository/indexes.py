'''Automated index management for MongoDB collections (NFR-005, NFR-006)'''

import logging
from pymongo import ASCENDING
from pymongo.database import Database as MongoDatabase

logger = logging.getLogger("projectrack.indexes")

def init_db_indexes(db: MongoDatabase) -> dict:
    '''Initializes and validates all required indexes across collections for high performance'''
    if db is None:
        logger.warning("Skipping index creation: database instance is None.")
        return {"status": "skipped", "message": "Database not initialized"}

    created = {}
    try:
        # Users collection: Unique index on email
        users_idx = db["users"].create_index([("email", ASCENDING)], unique=True, name="idx_users_email_unique")
        created["users"] = [users_idx]

        # Roles collection: Unique index on role name
        roles_idx = db["roles"].create_index([("role", ASCENDING)], unique=True, name="idx_roles_name_unique")
        created["roles"] = [roles_idx]

        # Classes collection: Index on professor_id for fast class-lookup by professor
        classes_idx = db["classes"].create_index([("professor_id", ASCENDING)], name="idx_classes_professor_id")
        created["classes"] = [classes_idx]

        # Assignments collection: Index on class_id for fast assignment retrieval by class
        assignments_idx = db["assignments"].create_index([("class_id", ASCENDING)], name="idx_assignments_class_id")
        created["assignments"] = [assignments_idx]

        # Submissions collection:
        # 1. Compound index on (assignment_id, student_id) for fast lookup of a student's submission to an assignment
        # 2. Index on student_id for student submission history queries
        sub_compound = db["submissions"].create_index(
            [("assignment_id", ASCENDING), ("student_id", ASCENDING)],
            name="idx_submissions_assignment_student"
        )
        sub_student = db["submissions"].create_index([("student_id", ASCENDING)], name="idx_submissions_student_id")
        created["submissions"] = [sub_compound, sub_student]

        # Student Assignments collection: Index on assignment_id
        student_assign_idx = db["student_assignments"].create_index(
            [("assignment_id", ASCENDING)],
            name="idx_student_assignments_assignment_id"
        )
        created["student_assignments"] = [student_assign_idx]

        # Professors collection: Unique index on user_id (one professor profile per user)
        prof_idx = db["professors"].create_index([("user_id", ASCENDING)], unique=True, name="idx_professors_user_id_unique")
        created["professors"] = [prof_idx]

        # Students collection: Unique index on user_id (one student profile per user)
        stud_idx = db["students"].create_index([("user_id", ASCENDING)], unique=True, name="idx_students_user_id_unique")
        created["students"] = [stud_idx]

        logger.info(f"Database indexes initialized successfully across {len(created)} collections.")
        return {"status": "success", "created_indexes": created}

    except Exception as e:
        logger.warning(f"Error creating database indexes: {e}")
        return {"status": "partial_error", "error": str(e), "created_indexes": created}
