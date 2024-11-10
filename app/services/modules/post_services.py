from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.modules.post import Post

async def create_post(db: AsyncSession, title: str, content: str, user_id: int):
    post = Post(title=title, content=content, author_id=user_id)
    db.add(post)
    await db.commit()
    return post

async def get_posts(db: AsyncSession):
    result = await db.execute(select(Post))
    return result.scalars().all()

async def get_post_by_id(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).filter(Post.id == post_id))
    return result.scalars().first()

async def update_post(db: AsyncSession, post_id: int, title: str, content: str):
    post = await get_post_by_id(db, post_id)
    if post:
        post.title = title
        post.content = content
        await db.commit()
    return post
