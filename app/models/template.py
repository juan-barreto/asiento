from pydantic import BaseModel

AVAILABLE_COLUMNS = {
    "Fecha": "Fecha",
    "Descripcion": "Descripción",
    "Detalle": "Detalle",
    "Debito": "Débito",
    "Credito": "Crédito",
    "Saldo": "Saldo"
}


class TemplateColumn(BaseModel):
    source: str
    title: str
    enabled: bool = True


class TemplateConfig(BaseModel):
    name: str
    format: str
    columns: list[TemplateColumn]