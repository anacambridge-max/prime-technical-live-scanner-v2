from dataclasses import dataclass
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

@dataclass(frozen=True)
class PrimeConfig:
    timeframe_minutes: int = 3
    scan_start: str = "09:15"
    scan_end: str = "10:00"
    volume_length: int = 20
    volume_multiple: float = 2.0
    minimum_body_ratio: float = 0.50
    minimum_close_location: float = 0.60
    range_expansion_ratio: float = 1.30
    range_average_length: int = 10
    break_trigger_mode: str = "Close Confirmed"
    level_buffer_pct: float = 0.0
    allow_1m: bool = False
    allow_3m: bool = True
    allow_5m: bool = False

PRIME_CONFIG = PrimeConfig()
