from pydantic import BaseModel

AVAILABLE_COLUMNS = {
    "fecha": "Fecha",
    "descripcion": "Descripción",
    "debito": "Débito",
    "credito": "Crédito",
    "saldo": "Saldo",
}


class TemplateColumn(BaseModel):
    source: str
    title: str
    enabled: bool = True


class TemplateConfig(BaseModel):
    name: str
    format: str
    columns: list[TemplateColumn]