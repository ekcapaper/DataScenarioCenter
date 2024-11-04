from pydantic import BaseModel


def to_camel(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
