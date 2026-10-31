from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class TransactionResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    detail: str
    debit: float
    credit: float
    balance: float
    confidence: float = 0.0

class StatsResponse(BaseModel):
    total_movements: int
    total_validated_movements: int
    total_pending_movements: int


class StatementResponse(BaseModel):
    bank: str
    transactions: list
    validated_transactions: list
    pending_review: list
    stats: StatsResponse
