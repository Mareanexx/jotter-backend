# controllers/collections.py
from fastapi import APIRouter, Depends, UploadFile, File, Form

router = APIRouter(prefix="/articles", tags=["Article"])


# @router.post("/", response_model=PostRead)
# async def create_post(
#     title: str = Form(...),
#     content: str = Form(...),
#     visibility_type: str = Form(...),
#     is_published: bool = Form(True),
#     category_ids: str = Form("[]"),
#     media: List[UploadFile] = File([]),
#     db: AsyncSession = Depends(get_db),
#     current_user: Profile = Depends(get_current_profile),
# ):
#     category_ids = json.loads(category_ids)
#     post_data = PostCreate(
#         title=title,
#         content=content,
#         visibility_type=visibility_type,
#         is_published=is_published,
#         category_ids=category_ids,
#     )
#     post = await create_post_service(
#         db=db, post_data=post_data, author_id=current_user.id, media_files=media
#     )
#     return post
