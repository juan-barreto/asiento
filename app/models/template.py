from pydantic import BaseModel


class TemplateColumn(BaseModel):
    source: str
    title: str
    position: int


class TemplateConfig(BaseModel):
    name: str
    format: str
    columns: list[TemplateColumn]