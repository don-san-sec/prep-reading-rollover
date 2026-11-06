"""Meter-reading and meter-exchange models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Reading:
    """A cumulative register reading taken from one meter on one day.

    Produced by the ingestion service when a smart meter sends a reading.
    `value_kwh` is the total energy the meter has recorded since install.
    """

    meter_id: str
    taken_on: date
    value_kwh: int


@dataclass
class MeterExchange:
    """A meter swapped inside a billing period.

    `old_meter_final` is the old meter's last reading, taken on the exchange
    date. `new_meter_opening` is the new meter's register value when it was
    installed — often a small non-zero figure left over from factory or bench
    testing.
    """

    exchanged_on: date
    old_meter_final: int
    new_meter_opening: int