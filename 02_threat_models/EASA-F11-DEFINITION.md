# EASA-F11
# Delegation-Chain Non-Amplification

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

Can an execution-authority delegation chain:

AGENT_A
->
AGENT_B
->
AGENT_C

preserve authority attenuation such that no delegate may silently increase:

- action scope;
- tool scope;
- local consequence ceiling;
- delegation depth;
- lineage-wide consequence ceiling;
- authority beyond that possessed by its immediate parent?

## Security Principle

DELEGATION
!=
AUTHORITY CREATION

CHILD AUTHORITY
<=
PARENT AUTHORITY

DELEGATION DEPTH
MUST DECREASE

LOCAL CONSEQUENCE CEILING
MUST NOT INCREASE

LINEAGE CONSEQUENCE BUDGET
MUST NOT MULTIPLY

A downstream agent may receive less authority than its parent.

It may not manufacture more.

## Target Property

ROOT_AUTHORITY_A
->
VALID_ATTENUATED_DELEGATION_TO_B
->
VALID_ATTENUATED_DELEGATION_TO_C

such that:

CHILD ACTIONS
SUBSET OF
PARENT ACTIONS

and:

CHILD TOOLS
SUBSET OF
PARENT TOOLS

and:

CHILD LOCAL CONSEQUENCE CEILING
<=
PARENT LOCAL CONSEQUENCE CEILING

and:

CHILD DELEGATION DEPTH
<
PARENT DELEGATION DEPTH

and:

ALL DESCENDANTS SHARE
ONE ROOT LINEAGE CONSEQUENCE CEILING

and:

REJECTED AMPLIFICATION REQUEST
=>
NO CHILD AUTHORITY ISSUED

## Bounded System Under Test

The EASA-F11 reference system contains:

1. one root authority held by AGENT_A;
2. one valid delegated authority held by AGENT_B;
3. one valid delegated authority held by AGENT_C;
4. one authority-lineage state object;
5. one root lineage consequence ceiling;
6. per-authority local consequence ceilings;
7. bounded action scopes;
8. bounded tool scopes;
9. bounded delegation depth;
10. one delegation gate;
11. one execution gate;
12. rejected action-scope amplification;
13. rejected tool-scope amplification;
14. rejected local-ceiling amplification;
15. rejected delegation-depth amplification;
16. rejected delegation attempt from an authority with no remaining delegation standing;
17. bounded execution across the delegation lineage;
18. preserved delegation and execution evidence.

## Authority Lineage

Lineage identity:

LINEAGE_F11_001

The entire A -> B -> C delegation chain belongs to this exact lineage.

Root lineage consequence ceiling:

4

Initial lineage consequence count:

0

All valid descendants must reference the same lineage state.

Delegation must not create an independent fresh lineage budget for B or C.

Therefore:

A LINEAGE CEILING OF 4

must not become:

4 FOR A
+
4 FOR B
+
4 FOR C

The bounded lineage maximum remains:

4 TOTAL CONSEQUENTIAL EXECUTIONS

across the valid A -> B -> C lineage.

## Root Authority — AGENT_A

Authority:

AUTH_F11_A_ROOT

Subject:

AGENT_A

Lineage:

LINEAGE_F11_001

Authorized actions:

F11_STANDARD_WRITE

F11_ADMIN_WRITE

Authorized tools:

TOOL_F11_STANDARD

TOOL_F11_HIGH

Local consequence ceiling:

4

Initial local consequence count:

0

Delegation depth remaining:

2

Current authority epoch:

1

Valid:

TRUE

## Valid Delegation A -> B

AGENT_A delegates:

AUTH_F11_B

to:

AGENT_B

AUTH_F11_B must retain:

LINEAGE = LINEAGE_F11_001

AUTHORIZED ACTIONS:

F11_STANDARD_WRITE

AUTHORIZED TOOLS:

TOOL_F11_STANDARD

LOCAL CONSEQUENCE CEILING:

2

DELEGATION DEPTH REMAINING:

1

AUTHORITY EPOCH:

1

The B authority is intentionally narrower than the A authority.

B does not inherit:

F11_ADMIN_WRITE

or:

TOOL_F11_HIGH

## Valid Delegation B -> C

AGENT_B delegates:

AUTH_F11_C

to:

AGENT_C

AUTH_F11_C must retain:

LINEAGE = LINEAGE_F11_001

AUTHORIZED ACTIONS:

F11_STANDARD_WRITE

AUTHORIZED TOOLS:

TOOL_F11_STANDARD

LOCAL CONSEQUENCE CEILING:

1

DELEGATION DEPTH REMAINING:

0

AUTHORITY EPOCH:

1

C may execute within that bounded authority.

C may not delegate further.

## Delegation Rule — Action Scope

A requested child action set must be a subset of the immediate parent's authorized action set.

Therefore:

B AUTHORIZED ACTIONS
=
{F11_STANDARD_WRITE}

B must not issue a child authority containing:

F11_ADMIN_WRITE

Expected result:

DELEGATION VERDICT = REFUSE

Expected reason:

DELEGATION_ACTION_SCOPE_AMPLIFICATION

Expected child authority:

NOT ISSUED

## Delegation Rule — Tool Scope

A requested child tool set must be a subset of the immediate parent's authorized tool set.

Therefore:

B AUTHORIZED TOOLS
=
{TOOL_F11_STANDARD}

B must not issue a child authority containing:

TOOL_F11_HIGH

Expected result:

DELEGATION VERDICT = REFUSE

Expected reason:

DELEGATION_TOOL_SCOPE_AMPLIFICATION

Expected child authority:

NOT ISSUED

## Delegation Rule — Local Consequence Ceiling

A child's local consequence ceiling must not exceed the parent's local consequence ceiling.

B local consequence ceiling:

2

B must not issue a child authority with:

LOCAL CONSEQUENCE CEILING = 3

Expected result:

DELEGATION VERDICT = REFUSE

Expected reason:

DELEGATION_CONSEQUENCE_CEILING_AMPLIFICATION

Expected child authority:

NOT ISSUED

## Delegation Rule — Delegation Depth

A valid child authority must have strictly less remaining delegation depth than its immediate parent.

B delegation depth remaining:

1

Therefore a valid child of B may have at most:

0

B must not issue a C authority with:

DELEGATION DEPTH REMAINING = 1

Expected result:

DELEGATION VERDICT = REFUSE

Expected reason:

DELEGATION_DEPTH_AMPLIFICATION

Expected child authority:

NOT ISSUED

## Delegation Rule — No Further Delegation From C

The valid C authority has:

DELEGATION DEPTH REMAINING = 0

C attempts to delegate to:

AGENT_D

Expected result:

DELEGATION VERDICT = REFUSE

Expected reason:

DELEGATION_AUTHORITY_NOT_PRESENT

Expected D authority:

NOT ISSUED

## Rejected Delegation Integrity

Every rejected delegation request must leave the parent authority unchanged.

Rejected requests must not mutate:

- parent subject identity;
- parent action scope;
- parent tool scope;
- parent local consequence ceiling;
- parent local consequence count;
- parent delegation depth;
- parent lineage identity;
- lineage consequence ceiling;
- lineage consequence count.

Rejected requests must create:

NO VALID CHILD AUTHORITY

## Valid-Chain Execution Test

After valid A -> B -> C delegation is established, execution occurs across the same lineage.

The bounded execution sequence is:

1. AGENT_C executes once using AUTH_F11_C.
2. AGENT_B executes twice using AUTH_F11_B.
3. AGENT_A executes once using AUTH_F11_A_ROOT.
4. AGENT_A attempts one additional execution.

All successful executions use:

ACTION:

F11_STANDARD_WRITE

TOOL:

TOOL_F11_STANDARD

## Expected C Execution

AUTH_F11_C local consequence ceiling:

1

First C execution:

VERDICT = PERMIT

REASON = AUTHORIZED

LOCAL C CONSEQUENCE COUNT AFTER = 1

LINEAGE CONSEQUENCE COUNT AFTER = 1

A second C execution is not part of the required successful sequence.

C has no authority to exceed its local ceiling.

## Expected B Executions

AUTH_F11_B local consequence ceiling:

2

B execution 1:

PERMIT

B execution 2:

PERMIT

After both:

B LOCAL CONSEQUENCE COUNT = 2

LINEAGE CONSEQUENCE COUNT = 3

## Expected A Execution

AUTH_F11_A_ROOT local consequence ceiling:

4

A executes once.

Expected:

VERDICT = PERMIT

A LOCAL CONSEQUENCE COUNT = 1

LINEAGE CONSEQUENCE COUNT = 4

The root lineage ceiling is now exhausted.

## Lineage-Ceiling Challenge

AGENT_A then attempts one additional otherwise-authorized execution using:

AUTH_F11_A_ROOT

ACTION:

F11_STANDARD_WRITE

TOOL:

TOOL_F11_STANDARD

The root authority itself has not exhausted its own local ceiling.

However:

LINEAGE CONSEQUENCE COUNT = 4

LINEAGE CONSEQUENCE CEILING = 4

Expected:

VERDICT = REFUSE

Expected reason:

LINEAGE_CONSEQUENCE_CEILING_EXHAUSTED

Expected consequence delta:

0

Final lineage consequence count:

4

This challenge isolates the shared lineage ceiling from the root authority's own local ceiling.

## Required Final Consequence State

Successful lineage executions:

C = 1

B = 2

A = 1

TOTAL = 4

Final shared lineage consequence count:

4

Additional lineage execution:

REFUSED

Total consequential execution must not exceed:

4

## Non-Amplification Dimensions

F11 requires non-amplification across five distinct dimensions.

### 1. Action Scope

Child actions must be a subset of parent actions.

### 2. Tool Scope

Child tools must be a subset of parent tools.

### 3. Local Consequence Ceiling

Child local consequence ceiling must not exceed parent local consequence ceiling.

### 4. Delegation Authority

Delegation depth must decrease at every valid delegation edge.

No authority with depth 0 may create a descendant.

### 5. Shared Lineage Consequence Ceiling

Delegation must not reset or duplicate the root lineage consequence budget.

All descendants remain bound to one shared lineage ceiling.

## Attack Paths

### Attack Path 1 — Action-Scope Amplification

B attempts to delegate F11_ADMIN_WRITE despite B lacking that action.

Expected:

REFUSE
/
DELEGATION_ACTION_SCOPE_AMPLIFICATION

### Attack Path 2 — Tool-Scope Amplification

B attempts to delegate TOOL_F11_HIGH despite B lacking that tool.

Expected:

REFUSE
/
DELEGATION_TOOL_SCOPE_AMPLIFICATION

### Attack Path 3 — Local-Ceiling Amplification

B attempts to delegate local consequence ceiling 3 despite B ceiling 2.

Expected:

REFUSE
/
DELEGATION_CONSEQUENCE_CEILING_AMPLIFICATION

### Attack Path 4 — Delegation-Depth Amplification

B attempts to give C remaining depth 1 despite B itself having only depth 1.

Expected child maximum:

0

Expected:

REFUSE
/
DELEGATION_DEPTH_AMPLIFICATION

### Attack Path 5 — Unauthorized Further Delegation

C attempts to delegate to D despite:

DELEGATION DEPTH REMAINING = 0

Expected:

REFUSE
/
DELEGATION_AUTHORITY_NOT_PRESENT

### Attack Path 6 — Aggregate Consequence Multiplication

After four total permitted consequences across A, B and C, A attempts another otherwise-authorized execution.

Expected:

REFUSE
/
LINEAGE_CONSEQUENCE_CEILING_EXHAUSTED

Expected consequence delta:

0

## Relationship to Earlier Examinations

EASA-F06 established presenter identity binding.

EASA-F07 established tool-specific authority isolation.

EASA-F08 established bounded concurrent single-consumption.

EASA-F09 established bounded revocation propagation.

EASA-F10 established bounded compromised-agent containment.

F11 introduces a materially different property:

authority transmitted through a delegation chain must attenuate rather than amplify.

No earlier examination establishes this property.

## Failure Conditions

EASA-F11 fails if any of the following occurs:

- B receives action scope outside A's scope;
- C receives action scope outside B's scope;
- B receives tool scope outside A's scope;
- C receives tool scope outside B's scope;
- a child local consequence ceiling exceeds its parent;
- delegation depth fails to decrease;
- C successfully delegates despite depth 0;
- a rejected delegation produces a valid child authority;
- a rejected delegation mutates its parent authority;
- a child receives an independent lineage budget;
- A, B and C do not share LINEAGE_F11_001;
- lineage consequence count is not shared across the chain;
- more than four total lineage consequences occur;
- the fifth lineage execution is permitted;
- the lineage ceiling can be bypassed through descendant execution;
- valid narrowed authority cannot execute within its allowed scope;
- evidence cannot reconstruct parent -> child derivation.

## Pass Conditions

EASA-F11 passes only if:

1. AUTH_F11_A_ROOT is bound to AGENT_A;
2. A root action scope contains F11_STANDARD_WRITE and F11_ADMIN_WRITE;
3. A root tool scope contains TOOL_F11_STANDARD and TOOL_F11_HIGH;
4. A local consequence ceiling is 4;
5. A delegation depth is 2;
6. A lineage is LINEAGE_F11_001;
7. root lineage ceiling is 4;
8. A -> B valid delegation succeeds;
9. AUTH_F11_B is bound to AGENT_B;
10. B action scope is exactly {F11_STANDARD_WRITE};
11. B tool scope is exactly {TOOL_F11_STANDARD};
12. B local consequence ceiling is 2;
13. B delegation depth is 1;
14. B retains LINEAGE_F11_001;
15. action-scope amplification request is refused;
16. action-scope amplification reason is DELEGATION_ACTION_SCOPE_AMPLIFICATION;
17. no authority is issued for action-scope amplification;
18. tool-scope amplification request is refused;
19. tool-scope amplification reason is DELEGATION_TOOL_SCOPE_AMPLIFICATION;
20. no authority is issued for tool-scope amplification;
21. local-ceiling amplification request is refused;
22. local-ceiling amplification reason is DELEGATION_CONSEQUENCE_CEILING_AMPLIFICATION;
23. no authority is issued for local-ceiling amplification;
24. delegation-depth amplification request is refused;
25. delegation-depth amplification reason is DELEGATION_DEPTH_AMPLIFICATION;
26. no authority is issued for delegation-depth amplification;
27. rejected B delegation requests leave AUTH_F11_B unchanged;
28. B -> C valid delegation succeeds;
29. AUTH_F11_C is bound to AGENT_C;
30. C action scope is exactly {F11_STANDARD_WRITE};
31. C tool scope is exactly {TOOL_F11_STANDARD};
32. C local consequence ceiling is 1;
33. C delegation depth is 0;
34. C retains LINEAGE_F11_001;
35. C -> D delegation is refused;
36. C -> D reason is DELEGATION_AUTHORITY_NOT_PRESENT;
37. no AUTH_F11_D authority is issued;
38. rejected C delegation leaves AUTH_F11_C unchanged;
39. A, B and C reference the same shared lineage state;
40. C's first authorized execution is permitted;
41. C local consequence count becomes 1;
42. lineage consequence count becomes 1;
43. B's first authorized execution is permitted;
44. B's second authorized execution is permitted;
45. B local consequence count becomes 2;
46. lineage consequence count becomes 3 after B's two executions;
47. A's first authorized execution is permitted;
48. A local consequence count becomes 1;
49. lineage consequence count becomes 4;
50. A's additional otherwise-authorized execution is refused;
51. final refusal reason is LINEAGE_CONSEQUENCE_CEILING_EXHAUSTED;
52. final refusal consequence delta is 0;
53. final lineage consequence count remains 4;
54. total successful lineage consequence count is exactly 4;
55. delegation never creates an independent replacement lineage budget;
56. every valid child is no broader than its immediate parent;
57. every rejected amplification attempt produces zero consequential execution;
58. delegation and execution evidence are independently reconstructable.

## Relevant Capability Benchmark

Primary:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

Supporting:

EASA-CAP-01
Threat & Attack-Path Analysis

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F11 does not establish:

- cryptographically signed delegation;
- production PKI delegation;
- cross-process delegation;
- cross-host delegation;
- distributed capability systems;
- delegation across network partitions;
- Byzantine delegate resistance;
- malicious code isolation;
- external identity authentication;
- recursive arbitrary-depth delegation;
- unlimited delegation graphs;
- delegation-cycle detection;
- concurrent delegation race safety;
- crash-recovery delegation durability;
- database transaction isolation;
- production distributed budget accounting;
- multi-region lineage accounting;
- unlimited consequence scale;
- universal capability-system security.

## Lineage Boundary

The shared lineage consequence ceiling is implemented conceptually as one bounded lineage state shared by valid descendants within the same reference process.

F11 does not claim that this shared state remains atomic or available across processes, hosts, networks, regions, or distributed databases.

Those conditions require separate prospective examinations.

## Delegation Boundary

A valid F11 delegation may only attenuate authority.

It may change the subject identity from parent to child.

It may narrow:

- actions;
- tools;
- local consequence ceiling;
- delegation depth.

It may not broaden any of them.

The root lineage ceiling remains invariant.

## Evidence Discipline

The definition must be frozen before implementation execution.

The exact delegation control, execution control and harness identities must be frozen before first observation.

The valid B and C authorities must be created prospectively by the frozen delegation mechanism.

They must not be manually constructed after an invalid delegation attempt.

Rejected delegation attempts must preserve evidence of:

- requested child subject;
- requested action scope;
- requested tool scope;
- requested local consequence ceiling;
- requested delegation depth;
- parent authority identity;
- verdict;
- reason;
- whether any child authority was issued.

The shared lineage object used during the first observation must remain the same lineage object across A, B and C.

The first observation must be preserved whether PASS or FAIL.

No failed first observation may be repaired, rerun, remapped, or waived.

Any correction requires a prospectively constituted successor.

## Governing Rule

DELEGATION MAY ATTENUATE AUTHORITY.

DELEGATION MAY NOT AMPLIFY AUTHORITY.

DESCENDANTS DO NOT RECEIVE MORE POWER THAN THEIR PARENT POSSESSES.

DELEGATION DOES NOT MULTIPLY THE ROOT CONSEQUENCE BUDGET.

Lock it.
Log it.
Prove it.