import logging
from typing_extensions import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4

from routers.profiles.schemas import (
    GetProfile_Response, 
    GetProfiles_ResponseProfile,
    GetProfiles_Response, 
    GetProfiles_Query,
    CreateProfile_Body,
    CreateProfile_Response,
) 
from routers.profiles.service import (
    get_profile__get_profile,
    get_profiles__get_profiles,
    create_profile__create_profile,
)
from routers._utils.schemas import make_dependable


router = APIRouter(prefix="/profiles")
logger = logging.getLogger("default")


@router.get("/{profile_id}", response_model=GetProfile_Response | None)
async def get_profile(profile_id: UUID4):
    
    res = await get_profile__get_profile(profile_id)
    if res is None:
        return None
    
    return GetProfile_Response(full_name=res.full_name)

@router.get("/", response_model=GetProfiles_Response)
async def get_profiles(
        body: Annotated[GetProfiles_Query, Depends(make_dependable(GetProfiles_Query))]
    ):
    
    res = await get_profiles__get_profiles(
        page=body.page,
        results_per_page=10,
        sort_field=body.sort_field,
        sort_order=body.sort_order,
    )
    
    return GetProfiles_Response(
        profiles=[
            GetProfiles_ResponseProfile(
                profile_id = p.id,
                full_name  = p.full_name,
            )
            for p in res
        ]
    )

@router.post("/", response_model=CreateProfile_Response)
async def create_profile(body: CreateProfile_Body):
    profile = await create_profile__create_profile(body)
    
    return CreateProfile_Response(
        profile_id = profile.id,
    )
