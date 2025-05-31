from app.models import Comment
from app.database.service import BaseService


class CommentService(BaseService[Comment]):
    model = Comment
