# Kata 3: Inherit Data / Virtual Form

Source: https://github.com/devdrops/Katas/tree/kata-inherit-data

## Problem

Implement form inheritance where child forms inherit fields, validation, and behavior from parent forms.

## Goals

- Form class hierarchy
- Field inheritance (merge parent + child fields)
- Validation inheritance
- Override specific fields
- Virtual forms (computed/derived fields)

## Features

1. **Base form** with common fields (CSRF, timestamps)
2. **Child forms** extend base, add specific fields
3. **Field merging**: parent fields + child fields
4. **Validation merging**: parent rules + child rules
5. **Virtual fields**: computed from other fields
6. **Form composition**: embed forms within forms

## Examples

```python
# Form inheritance
class UserForm(Form):
    name = StringField()
    email = EmailField()

class AdminForm(UserForm):
    # Inherits name, email
    permissions = MultiSelectField()
    # Virtual field
    @property
    def display_name(self):
        return f"Admin: {self.name}"
```

## Exercises

1. Base form with CSRF token
2. User registration extends base
3. Admin user extends user registration
4. Override validation (stricter email)
5. Virtual field: full_name from first+last
6. Nested forms (address within user)
7. Form factory from class hierarchy