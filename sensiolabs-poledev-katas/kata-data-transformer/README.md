# Kata 1: Data Transformer

Source: https://github.com/devdrops/Katas/tree/kata-data-transformers

## Problem

Build a data transformer that can convert data between different formats and structures.

## Goals

- Transform objects/arrays between formats
- Support: JSON, XML, CSV, YAML, arrays
- Flatten/nest structures
- Map fields with custom transformations
- Chain transformations

## Features

1. **Format conversion**: JSON ↔ XML ↔ CSV ↔ YAML
2. **Field mapping**: rename, move, restructure
3. **Value transformation**: type conversion, formatting, computation
4. **Filtering**: include/exclude fields
5. **Aggregation**: group, sum, average

## Examples

```python
# Data transformation
transformer = DataTransformer()
result = transformer.transform(
    input_data={"user": {"name": "John", "age": 30}},
    mapping={"user_name": "user.name", "user_age": "user.age"},
    output_format="csv"
)
# => "user_name,user_age\nJohn,30"
```

## Exercises

1. Basic JSON to CSV
2. Nested object flattening
3. Custom field transformers (date formats, currency)
4. Transformation pipeline/chain
5. Schema validation before/after
6. Streaming large datasets
7. Reversible transformations