from tests.test_base import TestBase
from mosaicode.model.commentmodel import CommentModel


class TestCommentModel(TestBase):

    def setUp(self):
        pass

    def test_new(self):
        comment = CommentModel()
        str(comment)

