from litestar import Controller, get, post, put, delete
from app.schemas import ArticleList, Article, Comment, CommentList


class ArticleController(Controller):
    path = "api/articles"

    @get()
    async def get_articles(
        self,
        tag: str | None,
        author: str | None,
        favorited: str | None,
        limit: int = 20,
        offset: int = 0,
    ) -> ArticleList:
        pass

    @get(path="/feed")
    async def get_article_feed(self, limit: int = 20, offset: int = 0) -> ArticleList:
        pass

    @get(path="/{slug:str}")
    async def get_article(self) -> Article:
        pass

    @post()
    async def create_article(
        self, title: str, description: str, body: str, tag_list: list[str] | None
    ) -> Article:
        pass

    @put(path="/{slug:str}")
    async def update_article(
        self, title: str | None, description: str | None, body: str | None
    ) -> Article:
        pass

    @delete(path="/{slug:str}")
    async def delete_article(self) -> Article:
        pass

    @post(path="/{slug:str}/comments")
    async def add_comment(self) -> Comment:
        pass

    @get(path="/{slug:str}/comments")
    async def get_comments(self) -> CommentList:
        pass

    @delete(path="/{slug:str}/comments/{id:int}")
    async def delete_comment(self) -> Comment:
        pass

    @post(path="/{slug:str}/favorite")
    async def favorite_article(self) -> Article:
        pass

    @delete(path="/{slug:str}/favorite")
    async def unfavorite_article(self) -> Article:
        pass
