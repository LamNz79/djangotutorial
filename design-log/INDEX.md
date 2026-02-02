## DL-01 — Question Detail BFF Aggregation
Status: Active
Affects: bff/routes/questions.ts, polls app APIs
Core rule: BFF contracts must be rooted in real domain entities (Question), never app namespaces.
Related: —
## DL-02 — User Vote Lookup API
Status: Active
Affects: polls app (Django), vote queries
Core rule: User-specific vote state must be queried from Django, never inferred in BFF.
Related: DL-01
