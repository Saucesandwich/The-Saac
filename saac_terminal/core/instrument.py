"""
The Saac Terminal - Universal Instrument Model & Registry
Agnostic schema for financial assets, equity indices, commodities, and forex pairs.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Callable, Optional, List

@dataclass
class SecondarySeriesConfig:
    id: str
    name: str
    ticker: str
    unit: str = ""
    decimals: int = 2
    default_val: float = 0.0

@dataclass
class InstrumentConfig:
    id: str
    symbol: str
    name: str
    ticker: str
    unit: str = "unit"
    currency: str = "USD"
    theme_color: str = "#ff9800"
    default_price: float = 0.0
    exchange: str = "Exchange"
    secondary_series: List[SecondarySeriesConfig] = field(default_factory=list)
    conversions: Dict[str, Callable[[float, Dict[str, float]], float]] = field(default_factory=dict)
    historical_records: List[Dict[str, Any]] = field(default_factory=list)

class InstrumentRegistry:
    def __init__(self):
        self._instruments: Dict[str, InstrumentConfig] = {}

    def register(self, instrument: InstrumentConfig):
        self._instruments[instrument.id.lower()] = instrument
        self._instruments[instrument.symbol.upper()] = instrument
        self._instruments[instrument.ticker.upper()] = instrument

    def get(self, key: str) -> Optional[InstrumentConfig]:
        if not key:
            return None
        return self._instruments.get(key.lower()) or self._instruments.get(key.upper())

    def list_instruments(self) -> List[InstrumentConfig]:
        seen = set()
        unique = []
        for inst in self._instruments.values():
            if inst.id not in seen:
                seen.add(inst.id)
                unique.append(inst)
        return unique

registry = InstrumentRegistry()
