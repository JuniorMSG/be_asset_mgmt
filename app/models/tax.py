# app/models/tax.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Numeric, DateTime, func, Integer, UniqueConstraint

class Base(DeclarativeBase):
    pass

class TaxRate(Base):
    __tablename__ = "tax_rates"
    __table_args__ = (
        UniqueConstraint("country_code", name="uq_tax_rates_country_code"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)  # 예: 20.00 (%)
    updated_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<TaxRate {self.country_code}={self.rate}>"
