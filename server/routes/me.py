"""Routes requiring an authenticated user."""

from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from pydantic import Field
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Lesson, User
from schemas import (
    UserBase,
    Course as CourseSchema,
    UserSchema,
    UserWithPassword,
    UserWithAuthToken,
    VocabSchema,
)
from middleware.auth import get_verified_user
from db.models.user_vocab_progress import UserVocabProgress


me_routes = APIRouter(prefix="/me")


@me_routes.get("/", response_model=UserSchema)
def get_me(user: User = Depends(get_verified_user)):
    return user


@me_routes.get("/courses", response_model=list)
def get_my_courses(user: User = Depends(get_verified_user)):
    return [
        {
            "title": course.title,
            "slug": course.slug,
            "id": course.id,
            "created_at": course.created_at,
            "target_language": course.target_language,
            "source_language": course.source_language,
        }
        for course in user.owned_courses
    ]


@me_routes.get("/lesson/{id}")
def get_next_vocab(
    id: str, user: User = Depends(get_verified_user), db=Depends(get_db)
):
    lesson = Lesson.get(db=db, value=id, key="id")
    accomplishment = user.accomplishment(db=db, lesson_id=lesson.id)

    return {
        "vocab": user.next_vocab_in_lesson(lesson_id=lesson.id),
        "accomplishment": accomplishment,
    }


@me_routes.post("/vocab/{id}")
def vocab_progress(
    id: int,
    body: dict,
    user: User = Depends(get_verified_user),
    db=Depends(get_db),
):
    answer_correct = body["answer_correct"]

    vocab_id = id
    additional_progress = str(int(answer_correct))

    vocab_progress = (
        db.query(UserVocabProgress)
        .filter(UserVocabProgress.user_id == user.id)
        .filter(UserVocabProgress.vocab_id == vocab_id)
        .first()
    )

    if not vocab_progress:
        vocab_progress = UserVocabProgress(
            vocab_id=vocab_id,
            user_id=user.id,
            progress="",
        )

    vocab_progress.progress += additional_progress

    db.add(vocab_progress)
    db.commit()
