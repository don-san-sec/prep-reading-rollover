"""Usage for a billing period (MTR-77).

Meter registers are cumulative, so a period's usage normally falls out of the
two readings taken on the period's start and end dates. Exchanges inside the
period are not handled yet — that is the limitation MTR-77 exists to fix.
"""

from __future__ import annotations

from metering.models import MeterExchange, Reading


def period_usage(
    start_reading: Reading,
    end_reading: Reading,
    exchanges: list[MeterExchange],
) -> int:
    """Usage in kWh for one billing period.

    Known limitation: only the no-exchange case is implemented. A period that
    spans a meter exchange raises NotImplementedError until MTR-77 lands.
    """
    if exchanges:
        raise NotImplementedError("exchange handling lands with MTR-77")

    return end_reading.value_kwh - start_reading.value_kwh