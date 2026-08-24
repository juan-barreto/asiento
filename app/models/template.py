from pydantic import BaseModel

AVAILABLE_COLUMNS = {
    "id": "ID",
    "fecha": "Fecha",
    "descripcion": "Descripción",
    "detalle": "Detalle",
    "debito": "Débito",
    "credito": "Crédito",
    "saldo": "Saldo",
    "confidence": "Confidence"
}


class TemplateColumn(BaseModel):
    source: str
    title: str
    enabled: bool = True


class TemplateConfig(BaseModel):
    name: str
    format: str
    columns: list[TemplateColumn]