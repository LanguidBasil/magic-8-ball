from sqlalchemy import select

from database import session_maker, User
from routers.profiles.schemas import (
    GetProfiles_QuerySortField,
    GetProfiles_QuerySortOrder,
    CreateProfile_Body,
) 


async def get_profile__get_profile(profile_id: str) -> User | None:
    
    async with session_maker.begin() as session:
        res = (await session.execute(
            select(User).
            where(User.id == profile_id)
        )).scalar()
        return res
    
    
async def get_profiles__get_profiles(
        page: int,
        results_per_page: int,
        sort_field: GetProfiles_QuerySortField,
        sort_order: GetProfiles_QuerySortOrder,
    ) -> list[User]:
    
    query = (
        select(User).
        offset((page - 1) * results_per_page).
        limit(results_per_page)
    )
    
    if sort_field != GetProfiles_QuerySortField.none:
        column_sort_mapping = {
            GetProfiles_QuerySortField.full_name: User.full_name,
            GetProfiles_QuerySortField.creation_date: User.creation_date,
        }
        column_to_sort = column_sort_mapping[sort_field]
        if sort_order == GetProfiles_QuerySortOrder.descending:
            column_to_sort = column_to_sort.desc()
        
        query = query.order_by(column_to_sort)
    
    
    async with session_maker.begin() as session:
        return list((await session.execute(query)).scalars())


async def create_profile__create_profile(body: CreateProfile_Body) -> User:
    
    p = User(full_name = body.full_name)
    
    async with session_maker.begin() as session:
        session.add(p)
    
    return p
