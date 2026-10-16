"""
The Saac Terminal - Modular Multi-Asset Financial Terminal & Asset Tracker Engine.
Institutional 2020s Bloomberg-style market tracking for commodities, equities, forex, and crypto.
"""

from .core.instrument import InstrumentConfig, SecondarySeriesConfig, registry
from .instruments.gold import GOLD_INSTRUMENT, calculate_thai_gold
from .instruments.nasdaq import NASDAQ_INSTRUMENT
from .instruments.indices import SP500_INSTRUMENT

# Register standard default instruments
registry.register(GOLD_INSTRUMENT)
registry.register(NASDAQ_INSTRUMENT)
registry.register(SP500_INSTRUMENT)

__version__ = "2.0.0"
__all__ = [
    "InstrumentConfig",
    "SecondarySeriesConfig",
    "registry",
    "GOLD_INSTRUMENT",
    "NASDAQ_INSTRUMENT",
    "SP500_INSTRUMENT",
    "calculate_thai_gold"
]
