# Section 5.2: Common Issues — Code Evidence

## 1. Left Recursion Detection

**Source: `src/org/intellij/grammar/inspection/BnfLeftRecursionInspection.java:22-44`**

Error message: `"'<ruleName>' employs left-recursion unsupported by generator"`

Detection: uses `BnfFirstNextAnalyzer.calcFirst(rule)` and checks if rule name appears in its own FIRST set. Excludes expression-parsing rules (which handle left recursion via Pratt parsing).

## 2. Unresolved References

**Source: `src/org/intellij/grammar/inspection/BnfResolveInspection.java:30-121`**

Three types detected:
- `"Unresolved rule reference"` — in attribute values
- `"Unresolved rule or method reference"` — for external references
- `"Unresolved method reference"` — in `methods` attribute list entries
- `"Pattern does not match any rule"` — for attribute patterns

## 3. Suspicious Token Detection

**Source: `src/org/intellij/grammar/inspection/BnfSuspiciousTokenInspection.java:28-58`**

Warning: `"'<text>' token looks like a reference to a missing rule"`

A token is suspicious if:
- It's not all-lowercase AND not all-uppercase, OR
- It's all-lowercase but contains `-` or `_`

Quick fix: `CreateRuleFromTokenFix` — creates a new rule definition.

## 4. Unused Rule Detection

**Source: `src/org/intellij/grammar/inspection/BnfUnusedRuleInspection.java:36-130`**

Five categories:
- `"Unused rule"` — not referenced from any expression
- `"Unreachable rule"` — referenced but not reachable from root/extra roots
- `"Unused fake rule"` — fake rule not referenced in expressions or attributes
- `"Reachable fake rule"` — fake rule referenced in rule body (likely mistake)
- `"Non-private recovery rule"` — recovery rule should be private

Uses transitive closure from root rules + extra roots.

## 5. Duplicate Rules

**Source: `src/org/intellij/grammar/inspection/BnfDuplicateRuleInspection.java`**

Detects rules with the same name.

## 6. Identical Choice Branches

**Source: `src/org/intellij/grammar/inspection/BnfIdenticalChoiceBranchesInspection.java`**

Detects duplicate alternatives in choice expressions (e.g., `a | b | a`).

## 7. Unreachable Choice Branches

**Source: `src/org/intellij/grammar/inspection/BnfUnreachableChoiceBranchInspection.java`**

Detects branches that are masked by earlier alternatives.

## 8. Text-Matched Token Warning

**Source: `src/org/intellij/grammar/editor/BnfAnnotator.java:140-151`**

Annotator message: `"Tokens matched by text are slower than tokens matched by types"`

Triggered when a quoted string in a rule body is not found in the token name-to-text map.

## 9. Inspection Suppression

**Source: `plugin.xml:54`, `CHANGELOG.md:152`**

Comment-based suppression: `//noinspection BnfUnusedRule`

Supported via `BnfInspectionSuppressor`.

## 10. Common Error Patterns from CHANGELOG

**Source: `CHANGELOG.md`**

Historical fixes indicating common issues:
- Endless cycle on cyclic inheritance (#234) — fixed in 2020.1
- Missing generated files on cold start — fixed in 1.0.9
- Left rule with several usages detected as recursive — fixed in 2017.1.6
- NPE for "exact-types" + factory method (#286) — fixed in 2021.1.2
- Incorrect method spec warning (#252) — fixed in 2020.3.1
- Double annotations for compiled elements (#251) — fixed in 2020.3.1
