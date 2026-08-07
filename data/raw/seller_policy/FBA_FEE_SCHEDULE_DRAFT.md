# Proposed Section 8 — "Fulfilled by SoftStore (FBA) Fees"

**For insertion into Document 05 (`Commission and Fee Schedule`).**

## Why this is needed

`documents/src/content_core.py::COMMISSION` (the literal source text `documents/src/build.py` renders into
`05_Commission_and_Fee_Schedule.pdf`) contains **zero** references to FBA or fulfilment. Its own §2
("What is deducted") states plainly: *"At launch a single deduction applies to a delivered marketplace
order: Marketplace commission."* That is no longer true — `FbaFeeService` is live, charging real PKR amounts
into `seller_fee_ledger`, and `system_settings.fba_seller_enrollment_enabled = 1` as of **2026-08-03
09:03:38** (confirmed via direct DB query). A seller reading only the signed document today would have no
way to know FBA fees exist at all.

This file does **not** edit `documents/src/content_legal.py` or `documents/src/content_core.py` — per the
audit's instructions, that is left for the owner to approve and a maintainer to apply, since it is a legal
document and this task is read-only. Every number below is transcribed verbatim from the live
`fba_fee_rates` table (`softstore_db`, queried 2026-08-03) — column values, not a summary.

## Source data (verbatim, `fba_fee_rates`, all rows `tenant_id IS NULL`, `is_active = 1`, `effective_from = 2026-08-01`, `effective_to NULL`)

| id | fee_type | band_label | min_weight_g | max_weight_g | per_unit_amount | per_event_amount |
|---|---|---|---|---|---|---|
| 1 | inbound_handling | NULL | NULL | NULL | 15.00 | 100.00 |
| 2 | fulfilment | Small | 0 | 500 | 0.00 | 60.00 |
| 3 | fulfilment | Standard | 501 | 2000 | 0.00 | 90.00 |
| 4 | fulfilment | Large | 2001 | 5000 | 0.00 | 150.00 |
| 5 | fulfilment | Bulky | 5001 | NULL | 0.00 | 280.00 |
| 6 | return_processing | NULL | NULL | NULL | 10.00 | 70.00 |
| 7 | removal | NULL | NULL | NULL | 25.00 | 150.00 |
| 8 | disposal | NULL | NULL | NULL | 15.00 | 50.00 |

**Live-in-database.** These 8 rows are what `FbaFeeService` (`app/app/services/FbaFeeService.php`) actually
charges today — `chargeInboundHandling()`, `chargeFulfilment()`, `chargeReturnProcessing()`,
`chargeRemoval()`, `chargeDisposal()`. There is no separate "draft" or "proposed" rate; this is the live
production rate card, already shown to sellers in-app at `/fba/fees`.

**Absent from the database — needs an owner decision, not invented here.** There is no `'storage'` value in
the `fba_fee_rates.fee_type` ENUM, no code path charges it, and `FbaFeeService.php:32-36` documents why: it
needs a daily accrual job, and this codebase runs on shared cPanel hosting with no daemons/cron beyond what
already exists (Operating Rule R1). Until the owner sets a policy and a rate, the schedule should say plainly
that storage is not billed — not print a number that doesn't exist anywhere in the system.

## Proposed markup (matches the style of sections 1–7 already in `content_core.py::COMMISSION`)

```html
<h2>8. Fulfilled by SoftStore (FBA) fees</h2>
<p>
  Fulfilled by SoftStore ("FBA") is optional, product-by-product. A seller who never enrols a product pays
  nothing in this section — these fees apply only to products the seller has actively opted into FBA, and
  only for the physical handling described below. They are separate from, and in addition to, the
  marketplace commission in §3, which still applies to every delivered order regardless of fulfilment
  channel.
</p>
<div class="note ok">
  <span class="t">This is not commission</span>
  Commission is a share of a sale and is payable only on delivery. FBA fees are service charges for physical
  work &mdash; receiving a shipment, picking and packing an order, processing a return, removing or disposing
  of stock &mdash; and are charged when that work happens, whether or not the order is ultimately delivered.
</div>

<h3>8.1 Inbound handling</h3>
<p>Charged once, when a shipment is received and counted in at the fulfilment centre. Billed on units
  actually received, not units declared.</p>
<table>
  <thead><tr><th>Fee</th><th class="num">PKR</th></tr></thead>
  <tbody>
    <tr><td>Per shipment</td><td class="num">100.00</td></tr>
    <tr><td>Per unit received</td><td class="num">15.00</td></tr>
  </tbody>
</table>

<h3>8.2 Fulfilment (pick, pack &amp; ship)</h3>
<p>Charged per order, banded by the product's declared weight, at the moment the parcel is booked with the
  courier &mdash; not on delivery. Priced by weight only, never by the product's price or category.</p>
<table>
  <thead><tr><th>Band</th><th>Weight</th><th class="num">Fee per order (PKR)</th></tr></thead>
  <tbody>
    <tr><td>Small</td><td>Up to 500g</td><td class="num">60.00</td></tr>
    <tr><td>Standard</td><td>501g &ndash; 2,000g</td><td class="num">90.00</td></tr>
    <tr><td>Large</td><td>2,001g &ndash; 5,000g</td><td class="num">150.00</td></tr>
    <tr><td>Bulky</td><td>5,001g and up</td><td class="num">280.00</td></tr>
  </tbody>
</table>

<h3>8.3 Return processing</h3>
<p>Charged when a returned or refused parcel is graded back in at the fulfilment centre.</p>
<table>
  <thead><tr><th>Fee</th><th class="num">PKR</th></tr></thead>
  <tbody>
    <tr><td>Per return event</td><td class="num">70.00</td></tr>
    <tr><td>Per unit processed</td><td class="num">10.00</td></tr>
  </tbody>
</table>

<h3>8.4 Removal and disposal</h3>
<p>A seller may ask for enrolled stock to be pulled back out of the fulfilment centre at any time.</p>
<table>
  <thead><tr><th>Request type</th><th>Fee</th><th class="num">PKR</th></tr></thead>
  <tbody>
    <tr><td rowspan="2">Removal (returned to the seller)</td><td>Per request</td><td class="num">150.00</td></tr>
    <tr><td>Per unit</td><td class="num">25.00</td></tr>
    <tr><td rowspan="2">Disposal (destroyed instead of returned)</td><td>Per request</td><td class="num">50.00</td></tr>
    <tr><td>Per unit</td><td class="num">15.00</td></tr>
  </tbody>
</table>

<h3>8.5 Storage</h3>
<div class="note warn">
  <span class="t">Not yet billed &mdash; owner decision required</span>
  There is currently no storage fee. Stock held at a fulfilment centre is not charged a per-day or per-cubic-foot
  holding fee under any circumstance. This is a placeholder pending an operating policy from SoftSkills
  Engineering, not a PKR 0.00 rate &mdash; it is unset. Sellers will receive notice, and this section will be
  updated with an effective date, before any storage charge is introduced.
</div>

<h3>8.6 Where these are recorded</h3>
<p>
  Every FBA fee is written to a fee ledger the seller can inspect line by line, separate from the commission
  ledger described in §5, and nets off the same twice-monthly payout run.
</p>
```

## What is live vs. what needs an owner decision

| Item | Status | Evidence |
|---|---|---|
| Inbound handling: PKR 100/shipment + PKR 15/unit | **Live in DB, live in code** | `fba_fee_rates` id 1; `FbaFeeService::chargeInboundHandling()` |
| Fulfilment: 4 weight bands, PKR 60/90/150/280 | **Live in DB, live in code** | `fba_fee_rates` id 2–5; `FbaFeeService::chargeFulfilment()` |
| Return processing: PKR 70/return + PKR 10/unit | **Live in DB, live in code** | `fba_fee_rates` id 6; `FbaFeeService::chargeReturnProcessing()` |
| Removal: PKR 150/request + PKR 25/unit | **Live in DB, live in code** | `fba_fee_rates` id 7; `FbaFeeService::chargeRemoval()` |
| Disposal: PKR 50/request + PKR 15/unit | **Live in DB, live in code** | `fba_fee_rates` id 8; `FbaFeeService::chargeDisposal()` |
| Storage | **Not implemented — owner must set a policy and a rate before §8.5 can say anything but "not yet billed"** | No `fee_type` ENUM value, no charging code, `/fba/fees` confirms in-app |

## Recommended next step

The owner reviews and approves this section (or amends the weight bands/amounts, which must then also
change in `fba_fee_rates` — the two must never be edited independently, which is the exact failure mode this
whole audit was commissioned to catch). Once approved, a maintainer inserts it as `content_core.py::COMMISSION`
§8 (after the existing §7 "Promotional campaigns", which is currently the last section) and reruns
`documents/src/build.py` to regenerate `05_Commission_and_Fee_Schedule.pdf` with a new effective date and
version bump, per the versioning convention already used by `core.VERSION` / `core.EFFECTIVE` in that file.
