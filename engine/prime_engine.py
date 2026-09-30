from dataclasses import dataclass
import pandas as pd
from .config import PrimeConfig

@dataclass
class PrimeSignal:
    symbol: str
    signal_type: str
    signal_time: pd.Timestamp
    breakout_level: float
    close: float
    volume: float
    volume_sma20: float
    score: float
    grade: str

def grade(score: float) -> str:
    if score >= 90: return "PRIME A+"
    if score >= 80: return "PRIME A"
    if score >= 70: return "STRONG"
    if score >= 60: return "GOOD"
    if score >= 50: return "WATCH"
    return "WEAK"

def detect_first_break(df: pd.DataFrame, pdh: float, pdl: float, symbol: str, cfg: PrimeConfig):
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {required - set(df.columns)}")
    work = df.sort_values("timestamp").copy()
    work["volume_sma20"] = work["volume"].rolling(cfg.volume_length).mean()
    signals = []
    pdh_broken = False
    pdl_broken = False
    for i in range(1, len(work)):
        row, prev = work.iloc[i], work.iloc[i-1]
        if row["timestamp"].hour * 60 + row["timestamp"].minute >= 600:
            continue
        vol_ok = row["volume"] >= row["volume_sma20"] * cfg.volume_multiple
        if not vol_ok or pd.isna(row["volume_sma20"]):
            continue
        if not pdh_broken and prev["close"] <= pdh and row["close"] > pdh:
            pdh_broken = True
            signals.append(_signal(row, symbol, "BUY", pdh))
        if not pdl_broken and prev["close"] >= pdl and row["close"] < pdl:
            pdl_broken = True
            signals.append(_signal(row, symbol, "SELL", pdl))
    return signals

def _signal(row, symbol, side, level):
    score = 70.0
    return PrimeSignal(symbol, side, row["timestamp"], level, row["close"], row["volume"], row["volume_sma20"], score, grade(score))
