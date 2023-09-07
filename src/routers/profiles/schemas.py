from enum import Enum
from pydantic import BaseModel, Field, constr, conint


class GetProfile_Response(BaseModel):
    full_name: constr(strip_whitespace=True)
    
    
class GetProfiles_QuerySortOrder(str, Enum):
    ascending = "ascending"
    descending = "descending"
    
class GetProfiles_QuerySortField(str, Enum):
    none = "none"
    creation_date = "creation_date"
    full_name = "full_name"
    
class GetProfiles_Query(BaseModel):
    page: conint(ge=1) = Field(1, description="10 items per page")
    sort_field: GetProfiles_QuerySortField = GetProfiles_QuerySortField.none
    sort_order: GetProfiles_QuerySortOrder = GetProfiles_QuerySortOrder.ascending

class GetProfiles_ResponseProfile(BaseModel):
    profile_id: int
    full_name: constr(strip_whitespace=True)

class GetProfiles_Response(BaseModel):
    profiles: list[GetProfiles_ResponseProfile]


class CreateProfile_Body(BaseModel):
    full_name: constr(strip_whitespace=True)

class CreateProfile_Response(BaseModel):
    profile_id: int
