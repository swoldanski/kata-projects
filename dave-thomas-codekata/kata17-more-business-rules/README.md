# Kata17: More Business Rules

Source: http://codekata.com/kata/kata17-more-business-rules/

## Problem

Extend the business rules engine (Kata16) with advanced features for real-world complexity.

## Goals

- Temporal rules (valid from/to dates)
- Rule priorities and conflict resolution
- Rule groups/namespaces
- Partial evaluation (streaming rules)
- Rule testing framework
- Visual rule editor/builder

## Advanced Features

1. **Temporal validity**: Rules active only during certain periods
2. **Priority/Precedence**: Higher priority rules override
3. **Mutual exclusion**: Rule groups where only one can fire
4. **Rule chaining**: Output of one rule feeds another
5. **Stateful rules**: Rules that track state across evaluations
6. **Machine learning integration**: ML model as a rule

## Examples

```python
# Advanced rules with temporal validity
rules = AdvancedRulesEngine()
rules.add_rule("summer_promo",
    And(
        Field("customer.tier") == "premium",
        DateBetween("2024-06-01", "2024-08-31")
    ),
    Action("apply_discount", percent=20),
    priority=10
)

# Conflict resolution: higher priority wins
```

## Exercises

1. Add effective/expiry dates to rules
2. Implement priority-based conflict resolution
3. Build a rule test harness (given facts, expect outcomes)
4. Rule coverage analysis
5. A/B testing framework for rules
6. Rule performance profiling
7. Migration: v1 rules → v2 rules