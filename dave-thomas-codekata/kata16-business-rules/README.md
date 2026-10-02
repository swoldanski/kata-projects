# Kata16: Business Rules

Source: http://codekata.com/kata/kata16-business-rules/

## Problem

Implement a business rules engine that can evaluate complex, changing business logic without code changes.

## Goals

- Separate rules from code
- Support rule composition (AND, OR, NOT)
- Rules as data (JSON, YAML, DSL)
- Hot-reload rules at runtime
- Audit trail (which rules fired, why)

## Rule Types

- **Threshold**: value > 1000
- **Range**: 18 <= age <= 65
- **Set membership**: country in {US, CA, MX}
- **Date/time**: before 2024-01-01, business hours
- **Compound**: (premium AND (age > 65 OR disabled))
- **Cross-field**: shipping != billing AND value > 500

## Examples

```python
# Business rules engine
rules = RulesEngine()
rules.add_rule("premium_discount", 
    And(
        Field("customer.tier") == "premium",
        Field("order.total") > 100
    ),
    Action("apply_discount", percent=15)
)

result = rules.evaluate({"customer": {"tier": "premium"}, "order": {"total": 150}})
# => {"apply_discount": {"percent": 15}}
```

## Exercises

1. Simple rule evaluator (single condition)
2. Composite rules (boolean logic)
3. Rule DSL or JSON schema
4. Rule registry with versioning
5. Explain facility (why did this fire?)
6. Performance: 10k rules, 1M evaluations/sec
7. Integration: discount engine, fraud detection, eligibility