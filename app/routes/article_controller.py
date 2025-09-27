from litestar import Controller, get, post, put, delete
from app.schemas import ArticleList, Article, Comment, CommentList


class ArticleController(Controller):
    path = "api/articles"

    @get()
    def get_articles(
        tag: str | None,
        author: str | None,
        favorited: str | None,
        limit: int = 20,
        offset: int = 0,
    ) -> ArticleList:
        pass

    @get(path="/feed")
    def get_article_feed(limit: int = 20, offset: int = 0) -> ArticleList:
        pass

    @get(path="/{slug:str}")
    def get_article() -> Article:
        pass

    @post()
    def create_article(
        title: str, description: str, body: str, tag_list: list[str] | None
    ) -> Article:
        pass

    @put(path="{slug:str}")
    def update_article(
        title: str | None, description: str | None, body: str | None
    ) -> Article:
        pass

    @delete(path="/{slug:str}")
    def delete_article() -> Article:
        pass

    @post(path="/{slug:str}/comments")
    def add_comment() -> Comment:
        pass

    @get(path="/{slug:str}/comments")
    def get_comments() -> CommentList:
        pass

    @delete(path="/{slug:str}/comments/{id:int}")
    def delete_comment() -> Comment:
        pass

    @post(path="/{slug:str}/favorite")
    def favorite_article() -> Article:
        pass

    @post(path="/{slug:str}/favorite")
    def unfavorite_article() -> Article:
        pass
