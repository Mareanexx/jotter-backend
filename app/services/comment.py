# services/comment.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentOut


async def create_comment(db: AsyncSession, data: CommentCreate, author_id: int) -> Comment:
    comment = Comment(**data.model_dump(), author_id=author_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(db: AsyncSession, comment_id: int, author_id: int) -> bool:
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment or comment.author_id != author_id:
        return False
    await db.delete(comment)
    await db.commit()
    return True


async def get_comments_for_post(db: AsyncSession, post_id: int) -> list[CommentOut]:
    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at)
    )
    comments = list(result.scalars().all())
    return build_comment_tree(comments)


def build_comment_tree(comments: list[Comment]) -> list[Comment]:
    comment_map = {c.id: c for c in comments}
    tree = []

    for comment in comments:
        comment.replies = []
    for comment in comments:
        if comment.parent_comment_id:
            parent = comment_map.get(comment.parent_comment_id)
            if parent:
                parent.replies.append(comment)
        else:
            tree.append(comment)
    return tree
