from uuid import UUID, uuid4

from pydantic import BaseModel, Field


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


