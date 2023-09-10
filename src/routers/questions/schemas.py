from datetime import datetime
from pydantic import BaseModel, constr, conint


_r_any_unicode_character_and_space = "[\p{L}\p{M}* ]"

class Post_Body(BaseModel):
    # pattern is for any unicode character and space
    text: constr(strip_whitespace=True, to_lower=True, pattern=_r_any_unicode_character_and_space)

class Post_Response(BaseModel):
    id: conint(strict=True, ge=1)
    
    creation_date: datetime
    text: constr(strip_whitespace=True, to_lower=True, pattern=_r_any_unicode_character_and_space)
    total_voices: conint(strict=True, ge=1)
