import re

from pydantic import BaseModel, ValidationError, constr, model_validator, field_validator


class GetLogs_Query(BaseModel):
    contains: constr(strip_whitespace=True) | None = None
    regex: str | None = None
    
    @model_validator(mode="after")
    def only_one(self):        
        if self.contains and self.regex:
            raise ValueError("Parameters 'contains' and 'regex' are mutually exclusive")
        return self
    
    @field_validator("regex")
    @classmethod
    def regex_valid(cls, value: str | None):
        if value is not None:
            try:
                re.compile(value)
            except re.error as e:
                raise ValueError(f"Invalid regex: {value}") from e
        return value
