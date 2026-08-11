from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class MovimientoRaw(BaseModel):
    fecha: str
    bloque: list[str]


class Movimiento(BaseModel):

    id: UUID = Field(default_factory=uuid4)

    fecha: str
    descripcion: str
    detalle: str
    debito: float
    credito: float
    saldo: float
    confidence: float = 0.0

    @field_validator("saldo")
    @classmethod
    def validar_saldo(cls, v):

        if v < 0:
            raise ValueError("Saldo inválido")

        return v
    
        # v = valor del campo actual (ej: 100.0)
        # values = otros campos ya validados (ej: {"debito": 100.0, "saldo": 500.0})
        # field = info del campo actual (ej: "debito" o "credito")
class StatsPipeline(BaseModel):

    total_movimientos : int
    total_seguros : int
    total_revisar: int
    
class ResultadoPipeline(BaseModel):

    banco : str
    movimientos: list[Movimiento]
    seguros : list[Movimiento]
    revisar : list[Movimiento]
    stats: StatsPipeline


