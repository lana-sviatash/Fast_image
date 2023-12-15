from typing import Type

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session, joinedload

from src.database.models import User, Image, Comment
from src.database.db import get_db

from src.services.auth import auth_service
from src.services.cloud_avatar import CloudAvatar

from src.schemas import (
    UserResponse,
    ChangeRoleRequest,
    UserProfile,
    CommentByUser,
    ImageProfile,
    ProfileMe,
    AllUsersProfiles,
)

from src.repository import users as repository_users
from src.services.roles import admin_and_moder, only_admin, all_roles

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=ProfileMe, dependencies=[Depends(all_roles)])
async def read_users_me(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
) -> User:
    user_profile = await repository_users.get_user_profile_me(db, current_user)
    return user_profile


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    public_id = CloudAvatar.generate_name_avatar(current_user.email)
    r = CloudAvatar.upload_avatar(file.file, public_id)
    src_url = CloudAvatar.get_url_for_avatar(public_id, r)
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user


@router.get(
    "/", response_model=AllUsersProfiles, dependencies=[Depends(admin_and_moder)]
)
async def get_users_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> AllUsersProfiles:
    users = await repository_users.get_users_profiles(db, current_user)
    return users


@router.get(
    "/user", response_model=UserResponse, dependencies=[Depends(admin_and_moder)]
)
async def get_user(
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> User:
    user = await repository_users.get_user_by_email(email, db)
    return user


@router.patch("/user", response_model=UserResponse, dependencies=[Depends(only_admin)])
async def change_user_role(
    body: ChangeRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> User:
    user = await repository_users.change_user_role(body, db)
    return user


@router.get(
    "/{user_name}", response_model=UserProfile, dependencies=[Depends(only_admin)]
)
async def get_user_profile(
    user_name,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    user_profile = await repository_users.get_user_profile_by_name(
        user_name, db, current_user
    )
    return user_profile
