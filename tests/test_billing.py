from datetime import date

from metering.billing import period_usage
from metering.models import MeterExchange, Reading


def test_usage_is_end_minus_start_when_no_exchange() -> None:
    start = Reading("mta-001", date(2026, 10, 1), 4_100)
    end = Reading("mta-001", date(2026, 10, 31), 4_320)

    assert period_usage(start, end, []) == 220


def test_exchange_in_period_is_not_yet_supported() -> None:
    start = Reading("mta-001", date(2026, 10, 1), 4_100)
    end = Reading("mta-002", date(2026, 10, 31), 190)
    exchange = MeterExchange(date(2026, 10, 14), 4_180, 12)

    try:
        period_usage(start, end, [exchange])
    except NotImplementedError:
        pass
    else:
        raise AssertionError("expected NotImplementedError until MTR-77 lands")
