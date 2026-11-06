# Meter-reading rollover across meter exchanges

Brightwatt Energy smart-meter usage: turning meter readings into the kWh figure
that goes on a customer's bill.

## Context

Brightwatt Energy is an app-first UK domestic energy supplier. About 180,000
customers pay a monthly bill, and almost all of them have smart meters that
send readings automatically. Meter registers are **cumulative**: a reading is
the total energy the meter has recorded since it was first installed.

Meters do get swapped — faults, battery end-of-life, comms upgrades. When an
engineer exchanges a meter, the old meter is removed and a new one installed
the same day.

The ticket for this work is MTR-77:

> "Bill a billing period that spans a meter exchange."

## The billing rules for a period

A billing period runs from a start date to an end date. Readings are taken on
the period's start and end dates, and the register is cumulative. These are the
rules the billing team's handbook gives for turning those readings into usage.

1. Normally — same meter for the whole period — usage over the period is
   **end reading − start reading**.
2. When a meter is exchanged **inside** the period, the exchange record carries
   the exchange date (`exchanged_on`), the old meter's last reading
   (`old_meter_final`, taken on the exchange date), and the new meter's
   register value when it was installed (`new_meter_opening`). Period usage is
   **(old_meter_final − start_reading) + (end_reading − new_meter_opening)**:
   the old meter's segment plus the new meter's segment.
3. The exchange day belongs to the **old** meter. The old side counts up to and
   including the exchange date's reading; the new meter's usage counts
   strictly after the exchange date.
4. If the period contains **multiple** exchanges, each exchange contributes its
   own segment, and the segments sum.
5. Usage can **never be negative**. Negative usage means bad data (a misread,
   a rolled-back register) and must **raise an error** — never produce a bill.

One wrinkle worth calling out: new meters often carry a small **non-zero**
opening register value left over from factory or bench testing before
installation. That is exactly why the exchange record stores
`new_meter_opening` rather than assuming the new meter starts at zero.

Worked examples from the handbook:

- Same meter all month: start 4,100 kWh, end 4,320 kWh → **220 kWh** used.
- Meter exchanged on the 14th: start 4,100, old meter's final 4,180, new
  meter's opening 12, end 190 → (4,180 − 4,100) + (190 − 12) =
  **258 kWh**.

## How it works

```
src/metering/
  models.py           Reading, MeterExchange
  billing.py          period_usage(); usage for a billing period, per rule 1
tests/
```

Exchange handling is not implemented yet — `period_usage()` bills the
no-exchange case only and raises `NotImplementedError` when a period contains
an exchange. That is the known limitation MTR-77 exists to fix. Reading
collection itself lives in the ingestion service, not here; this service owns
the model and the usage calculation that feeds the bill.

## Running locally

```
uv sync
uv run pytest -q
```

## Your task

A colleague has opened a PR: https://github.com/don-san-sec/prep-reading-rollover/pull/1. You are the owner of this feature. Review the PR and decide whether to accept or reject it, and explain why.
