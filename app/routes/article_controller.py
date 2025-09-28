from litestar import Controller, get, post, put, delete
from app.schemas.response_schemas import ArticleList, Article, Comment, CommentList
from app.schemas.request_schemas import (
    GetArticlesType,
    GetFeedType,
    CreateArticleType,
    UpdateArticleType,
)


class ArticleController(Controller):
    path = "api/articles"

    @get()
    async def get_articles(self, query: GetArticlesType) -> ArticleList:
        pass

    @get(path="/feed")
    async def get_article_feed(self, query: GetFeedType) -> ArticleList:
        pass

    @get(path="/{slug:str}")
    async def get_article(self) -> Article:
        pass

    @post()
    async def create_article(self, data: CreateArticleType) -> Article:
        pass

    @put(path="/{slug:str}")
    async def update_article(self, data: UpdateArticleType) -> Article:
        pass

    @delete(path="/{slug:str}")
    async def delete_article(self) -> None:
        pass

    @post(path="/{slug:str}/comments")
    async def add_comment(self) -> Comment:
        pass

    @get(path="/{slug:str}/comments")
    async def get_comments(self) -> CommentList:
        pass

    @delete(path="/{slug:str}/comments/{id:int}")
    async def delete_comment(self) -> None:
        pass

    @post(path="/{slug:str}/favorite")
    async def favorite_article(self) -> Article:
        pass

    @delete(path="/{slug:str}/favorite")
    async def unfavorite_article(self) -> None:
        pass
