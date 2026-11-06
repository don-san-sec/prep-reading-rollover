from datetime import date

import pytest

from metering.billing import period_usage
from metering.models import MeterExchange, Reading


def test_usage_is_end_minus_start_when_no_exchange() -> None:
    start = Reading("mta-001", date(2026, 10, 1), 4_100)
    end = Reading("mta-001", date(2026, 10, 31), 4_320)

    assert period_usage(start, end, []) == 220


def test_usage_spans_a_mid_period_exchange() -> None:
    start = Reading("mta-001", date(2026, 10, 1), 4_100)
    end = Reading("mta-002", date(2026, 10, 31), 190)
    exchange = MeterExchange(date(2026, 10, 14), 4_180, 0)

    # Old meter: 4,180 - 4,100. New meter: 190 - 0.
    assert period_usage(start, end, [exchange]) == 270


def test_exchange_date_outside_the_period_is_rejected() -> None:
    start = Reading("mta-001", date(2026, 10, 1), 4_100)
    end = Reading("mta-002", date(2026, 10, 31), 190)
    exchange = MeterExchange(date(2026, 11, 5), 4_180, 0)

    with pytest.raises(ValueError):
        period_usage(start, end, [exchange])
