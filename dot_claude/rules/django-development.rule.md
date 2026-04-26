---
paths:
  - "**/*.py"
---

# Django Development Standards

## Responsibility of Django Models

* While Django Models primarily handle persistence, they permit the following:
  * Constraints related to database integrity (e.g., unique, null, FK constraints)
  * Lightweight immutable validation checks (e.g., value ranges, formats)
* They should not contain business logic (use-case-specific behavior)

## Domain Models

* Business logic should be implemented in dataclasses defined in domain.py
* These dataclasses should default to frozen=True, treating them as immutable objects
* State changes should be expressed not through mutation but by returning new instances (using dataclasses.replace)
* Entities should explicitly define their "identity" (typically based on IDs)

## Repository Layer

* Define Repository classes for each Django Model in repositories.py
* Repositories are responsible for:
  * Converting between Django Models and domain models (to_domain(), from_domain())
  * Handling persistence operations (get, save, delete, etc.)
* Implement as instance methods to enable dependency injection (DI)
* Define interfaces using typing.Protocol when necessary for testability

## Transaction Management

* Transaction boundaries should be defined in the Application Service layer
* @transaction.atomic should generally be applied to service layer methods
* Repositories should focus on single operations and not handle transaction control themselves (or only minimally)

## Application Services

* Handle processing at the use case level
* Manage coordination between multiple Repositories and external API integrations here
* Clearly define transaction boundaries

## Storage Rules

* Never call .save() directly on Django Models
* Always persist data through Repositories
* Exceptionally, consider updates from admin interfaces, and detect/control deviations using either:
  * Guards implemented by overriding Model's save() method
  * Detection by linters (e.g., ruff)
  * Module isolation to limit imports

## Guidelines for Using Value Objects

* Define primitive types as Value Objects when meeting the following criteria:
  1. Values with critical consequences for errors (e.g., monetary amounts, currencies, dates)
  2. Identifiers with multiple meanings using the same primitive type (e.g., CustomerId, OrderId)
  3. Values where validation and formatting are crucial (e.g., Email, URL, Postcode)
* Value Objects must satisfy:
  * Immutability
  * Definition of __eq__ and __hash__
  * Explicit serialization methods (for DB storage and JSON conversion)

## Coexistence with Django Features

* Clearly delineate responsibilities between Django's Field validation and Value Objects:
  * Basic field-level validation → Django Model
  * Domain rules → Value Objects / Domain Models
* Keep complex QuerySet queries confined within the Repository layer

## Application Guidelines

* These rules are particularly recommended for cases involving:
  * Complex domain logic
  * Mid-to-large scale development
  * Long-term operational requirements
* For simple CRUD-focused applications, consider simplified approaches
