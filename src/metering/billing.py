"""Usage for a billing period (MTR-77).

Meter registers are cumulative, so a period's usage normally falls out of the
two readings taken on the period's start and end dates. When a meter is
exchanged inside the period, the register rolls over to the new meter and the
period splits into an old-meter segment and a new-meter segment.
"""

from __future__ import annotations

from metering.models import MeterExchange, Reading


def period_usage(
    start_reading: Reading,
    end_reading: Reading,
    exchanges: list[MeterExchange],
) -> int:
    """Usage in kWh for one billing period.

    With no exchange, usage is the end reading minus the start reading. With
    an exchange inside the period, the old meter is billed up to its final
    reading and the new meter is billed from installation to the end reading.
    """
    if not exchanges:
        return end_reading.value_kwh - start_reading.value_kwh

    exchange = exchanges[0]
    if not (start_reading.taken_on <= exchange.exchanged_on <= end_reading.taken_on):
        raise ValueError("exchange date falls outside the billing period")

    # The old meter runs up to and including the exchange date.
    old_usage = exchange.old_meter_final - start_reading.value_kwh

    # New meters are zeroed on install, so the whole of the new register at
    # the end reading is usage since the exchange.
    new_usage = end_reading.value_kwh

    return old_usage + new_usage