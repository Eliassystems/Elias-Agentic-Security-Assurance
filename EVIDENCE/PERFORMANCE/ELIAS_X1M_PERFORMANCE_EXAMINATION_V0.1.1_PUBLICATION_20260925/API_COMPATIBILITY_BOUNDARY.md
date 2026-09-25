# API Compatibility Boundary

## Established

The persisted Shadow V3 examination compared 21 corresponding decision
values against the frozen `ExecutionDecision` field order.

Across the bounded 100,000-case generated sequential comparison:

- compared values: 21
- observed mismatches: 0

## Representation difference

The frozen baseline returns an `ExecutionDecision` frozen dataclass.

Shadow V3 returns a raw Python tuple containing the examined values in
the validated field order.

Those are not the same Python representation or public object type.

In particular, the V3 tuple does not by itself preserve dataclass-style
named attribute access such as:

`decision.verdict`

## Standing

FIELD-VALUE EQUIVALENCE WITHIN TESTED POPULATION:
SUPPORTED

FIELD ORDER WITHIN TESTED SCHEMA:
SUPPORTED

PYTHON OBJECT-TYPE EQUIVALENCE:
NOT ESTABLISHED

NAMED-ATTRIBUTE API COMPATIBILITY:
NOT ESTABLISHED

DROP-IN REPLACEMENT COMPATIBILITY:
NOT ESTABLISHED

PRODUCTION REPLACEMENT AUTHORITY:
NOT ESTABLISHED

Any future adoption as a successor implementation requires either an
explicit compatibility boundary / adapter or a separate API
compatibility examination.

Evidence stops where the evidence stops.
