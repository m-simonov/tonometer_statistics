from sqlalchemy import extract, select, func
from db.models.feedback import Feedback
from db.repositories.base import AbstractRepository


class FeedbackRepository(AbstractRepository):
    model = Feedback
