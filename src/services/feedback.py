from db.models.feedback import Feedback

from db.repositories.feedback import FeedbackRepository
from logger import logger
from services.base import AbstractService


class FeedbackService(AbstractService):
    async def add_feedback(self, tid: int, text: str):
        async with self.session.begin():
            await FeedbackRepository(self.session).add(
                [Feedback(user=tid, text=text)],
            )
        logger.debug("Feedback added", user=tid, text=str)
