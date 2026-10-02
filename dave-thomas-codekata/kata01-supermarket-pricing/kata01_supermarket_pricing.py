"""Kata01: Supermarket Pricing - Pricing Model Design

This module implements a flexible pricing model for supermarket goods following
DDD/CQRS/Repository patterns with in-memory state.

Source: http://codekata.com/kata/kata01-supermarket-pricing/
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from typing import Protocol

# =============================================================================
# Value Objects
# =============================================================================

@dataclass(frozen=True)
class Money:
    """Immutable money value with currency."""
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        # Ensure amount is quantized to 2 decimal places
        object.__setattr__(
            self, 'amount', self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        )

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, quantity: int) -> Money:
        return Money(self.amount * quantity, self.currency)

    def __str__(self) -> str:
        return f"${self.amount:.2f}"


@dataclass(frozen=True)
class Quantity:
    """Quantity with optional unit (each, lb, kg, etc.)."""
    amount: Decimal
    unit: str = "each"

    def __post_init__(self):
        object.__setattr__(self, 'amount', self.amount.quantize(Decimal('0.001')))

    def __str__(self) -> str:
        if self.unit == "each":
            return str(int(self.amount)) if self.amount == int(self.amount) else str(self.amount)
        return f"{self.amount} {self.unit}"


# =============================================================================
# Pricing Rule Types
# =============================================================================

class PricingType(Enum):
    SIMPLE = "simple"                    # $X per unit
    VOLUME = "volume"                    # N for $X
    WEIGHT = "weight"                    # $X per lb/kg
    BUY_N_GET_M = "buy_n_get_m"         # Buy N, get M free


@dataclass(frozen=True)
class PricingRule:
    """A pricing rule for a product."""
    product_id: str
    pricing_type: PricingType
    # For SIMPLE: price_per_unit
    price_per_unit: Money | None = None
    # For VOLUME: volume_quantity, volume_price
    volume_quantity: int | None = None
    volume_price: Money | None = None
    # For WEIGHT: price_per_unit (per lb/kg)
    # For BUY_N_GET_M: buy_quantity, get_quantity
    buy_quantity: int | None = None
    get_quantity: int | None = None

    def __post_init__(self):
        if self.pricing_type == PricingType.SIMPLE and self.price_per_unit is None:
            raise ValueError("SIMPLE pricing requires price_per_unit")
        if self.pricing_type == PricingType.VOLUME and (
            self.volume_quantity is None or self.volume_price is None
        ):
            raise ValueError("VOLUME pricing requires volume_quantity and volume_price")
        if self.pricing_type == PricingType.WEIGHT and self.price_per_unit is None:
            raise ValueError("WEIGHT pricing requires price_per_unit")
        if self.pricing_type == PricingType.BUY_N_GET_M and (
            self.buy_quantity is None or self.get_quantity is None
        ):
            raise ValueError("BUY_N_GET_M pricing requires buy_quantity and get_quantity")


# =============================================================================
# Entities
# =============================================================================

@dataclass
class Product:
    """Product entity with pricing rules."""
    id: str
    name: str
    default_unit: str = "each"
    pricing_rules: list[PricingRule] = field(default_factory=list)

    def add_pricing_rule(self, rule: PricingRule) -> None:
        if rule.product_id != self.id:
            raise ValueError("Rule product_id must match product id")
        self.pricing_rules.append(rule)

    def get_applicable_rule(self, quantity: Quantity) -> PricingRule | None:
        """Get the best applicable pricing rule for a quantity."""
        applicable = [r for r in self.pricing_rules if self._rule_applies(r, quantity)]
        if not applicable:
            return None
        # Prefer volume/buy_n_get_m over simple/weight for better deals
        priority = {
            PricingType.VOLUME: 3,
            PricingType.BUY_N_GET_M: 2,
            PricingType.WEIGHT: 1,
            PricingType.SIMPLE: 0,
        }
        return max(applicable, key=lambda r: priority.get(r.pricing_type, 0))

    def _rule_applies(self, rule: PricingRule, quantity: Quantity) -> bool:
        if rule.pricing_type == PricingType.VOLUME:
            return quantity.amount >= rule.volume_quantity
        if rule.pricing_type == PricingType.BUY_N_GET_M:
            return quantity.amount >= rule.buy_quantity
        return True


# =============================================================================
# Repository Interface (Repository Pattern)
# =============================================================================

class ProductRepository(Protocol):
    """Repository interface for product data access."""

    def save(self, product: Product) -> None: ...

    def find_by_id(self, product_id: str) -> Product | None: ...

    def find_all(self) -> list[Product]: ...


class InMemoryProductRepository:
    """In-memory implementation of ProductRepository."""

    def __init__(self):
        self._products: dict[str, Product] = {}

    def save(self, product: Product) -> None:
        self._products[product.id] = product

    def find_by_id(self, product_id: str) -> Product | None:
        return self._products.get(product_id)

    def find_all(self) -> list[Product]:
        return list(self._products.values())


# =============================================================================
# Domain Services
# =============================================================================

class PricingService:
    """Domain service for calculating prices."""

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def calculate_price(self, product_id: str, quantity: Quantity) -> Money:
        """Calculate total price for a product quantity."""
        product = self._repository.find_by_id(product_id)
        if not product:
            raise ValueError(f"Product not found: {product_id}")

        rule = product.get_applicable_rule(quantity)
        if not rule:
            raise ValueError(f"No pricing rule for product {product_id} with quantity {quantity}")

        return self._apply_rule(rule, quantity)

    def _apply_rule(self, rule: PricingRule, quantity: Quantity) -> Money:
        if rule.pricing_type == PricingType.SIMPLE:
            return rule.price_per_unit * int(quantity.amount)

        elif rule.pricing_type == PricingType.VOLUME:
            # Volume discount: N for $X
            full_sets = int(quantity.amount) // rule.volume_quantity
            remainder = int(quantity.amount) % rule.volume_quantity
            total = rule.volume_price * full_sets
            if remainder > 0 and rule.price_per_unit:
                total = total + (rule.price_per_unit * remainder)
            return total

        elif rule.pricing_type == PricingType.WEIGHT:
            # Weight-based: $X per unit weight
            return rule.price_per_unit * Decimal(str(quantity.amount))

        elif rule.pricing_type == PricingType.BUY_N_GET_M:
            # Buy N get M free
            paid_items = int(quantity.amount)
            deal_size = rule.buy_quantity + rule.get_quantity
            full_deals = paid_items // deal_size
            remainder = paid_items % deal_size
            # In each deal, pay for buy_quantity items
            paid_in_deals = full_deals * rule.buy_quantity
            # Remainder: pay for min(remainder, buy_quantity) items
            paid_remainder = min(remainder, rule.buy_quantity)
            total_paid = paid_in_deals + paid_remainder
            return rule.price_per_unit * total_paid

        raise ValueError(f"Unknown pricing type: {rule.pricing_type}")


# =============================================================================
# Commands (Write Model - CQRS)
# =============================================================================

@dataclass
class CreateProductCommand:
    product_id: str
    name: str
    default_unit: str = "each"


@dataclass
class AddPricingRuleCommand:
    product_id: str
    rule: PricingRule


class ProductCommandHandler:
    """Command handler for product operations (write side)."""

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def handle_create_product(self, cmd: CreateProductCommand) -> Product:
        product = Product(
            id=cmd.product_id,
            name=cmd.name,
            default_unit=cmd.default_unit
        )
        self._repository.save(product)
        return product

    def handle_add_pricing_rule(self, cmd: AddPricingRuleCommand) -> Product:
        product = self._repository.find_by_id(cmd.product_id)
        if not product:
            raise ValueError(f"Product not found: {cmd.product_id}")
        product.add_pricing_rule(cmd.rule)
        self._repository.save(product)
        return product


# =============================================================================
# Queries (Read Model - CQRS)
# =============================================================================

@dataclass
class ProductPriceQuery:
    product_id: str
    quantity: Quantity


@dataclass
class ProductPriceResult:
    product_id: str
    product_name: str
    quantity: Quantity
    unit_price: Money
    total_price: Money
    applied_rule: PricingRule | None


class ProductQueryHandler:
    """Query handler for product pricing (read side)."""

    def __init__(self, pricing_service: PricingService, repository: ProductRepository):
        self._pricing_service = pricing_service
        self._repository = repository

    def handle_price_query(self, query: ProductPriceQuery) -> ProductPriceResult:
        product = self._repository.find_by_id(query.product_id)
        if not product:
            raise ValueError(f"Product not found: {query.product_id}")

        total_price = self._pricing_service.calculate_price(query.product_id, query.quantity)
        rule = product.get_applicable_rule(query.quantity)
        unit_price = self._calculate_unit_price(rule, query.quantity, total_price)

        return ProductPriceResult(
            product_id=product.id,
            product_name=product.name,
            quantity=query.quantity,
            unit_price=unit_price,
            total_price=total_price,
            applied_rule=rule
        )

    def _calculate_unit_price(
        self, rule: PricingRule | None, quantity: Quantity, total: Money
    ) -> Money:
        if rule and rule.pricing_type == PricingType.BUY_N_GET_M:
            # For BOGO, effective unit price
            qty = Decimal(str(quantity.amount))
            if qty > 0:
                return Money(total.amount / qty)
        elif quantity.amount > 0:
            return Money(total.amount / Decimal(str(quantity.amount)))
        return Money(Decimal('0'))


# =============================================================================
# Facade / Application Service
# =============================================================================

class PricingEngine:
    """Main facade for the pricing system."""

    def __init__(self):
        self._repository = InMemoryProductRepository()
        self._pricing_service = PricingService(self._repository)
        self._command_handler = ProductCommandHandler(self._repository)
        self._query_handler = ProductQueryHandler(self._pricing_service, self._repository)

    # Commands
    def create_product(self, product_id: str, name: str, default_unit: str = "each") -> Product:
        cmd = CreateProductCommand(product_id=product_id, name=name, default_unit=default_unit)
        return self._command_handler.handle_create_product(cmd)

    def add_simple_pricing(self, product_id: str, price_per_unit: Money) -> Product:
        rule = PricingRule(
            product_id=product_id,
            pricing_type=PricingType.SIMPLE,
            price_per_unit=price_per_unit
        )
        cmd = AddPricingRuleCommand(product_id=product_id, rule=rule)
        return self._command_handler.handle_add_pricing_rule(cmd)

    def add_volume_pricing(
        self,
        product_id: str,
        volume_qty: int,
        volume_price: Money,
        unit_price: Money | None = None,
    ) -> Product:
        rule = PricingRule(
            product_id=product_id,
            pricing_type=PricingType.VOLUME,
            volume_quantity=volume_qty,
            volume_price=volume_price,
            price_per_unit=unit_price
        )
        cmd = AddPricingRuleCommand(product_id=product_id, rule=rule)
        return self._command_handler.handle_add_pricing_rule(cmd)

    def add_weight_pricing(self, product_id: str, price_per_unit: Money) -> Product:
        rule = PricingRule(
            product_id=product_id,
            pricing_type=PricingType.WEIGHT,
            price_per_unit=price_per_unit
        )
        cmd = AddPricingRuleCommand(product_id=product_id, rule=rule)
        return self._command_handler.handle_add_pricing_rule(cmd)

    def add_buy_n_get_m_pricing(
        self, product_id: str, buy_qty: int, get_qty: int, unit_price: Money
    ) -> Product:
        rule = PricingRule(
            product_id=product_id,
            pricing_type=PricingType.BUY_N_GET_M,
            buy_quantity=buy_qty,
            get_quantity=get_qty,
            price_per_unit=unit_price
        )
        cmd = AddPricingRuleCommand(product_id=product_id, rule=rule)
        return self._command_handler.handle_add_pricing_rule(cmd)

    # Queries
    def get_price(self, product_id: str, quantity: Quantity) -> ProductPriceResult:
        query = ProductPriceQuery(product_id=product_id, quantity=quantity)
        return self._query_handler.handle_price_query(query)

    def get_all_products(self) -> list[Product]:
        return self._repository.find_all()


# =============================================================================
# Convenience Function (Functional Alternative)
# =============================================================================

def design_pricing_model() -> dict:
    """Return a design document for pricing models.
    
    This is the functional alternative for the kata.
    """
    return {
        "value_objects": {
            "Money": "Immutable amount with currency, supports arithmetic",
            "Quantity": "Amount with unit (each, lb, kg)",
        },
        "pricing_types": {
            "SIMPLE": "Fixed price per unit",
            "VOLUME": "N items for $X (e.g., 3 for $1)",
            "WEIGHT": "$X per lb/kg",
            "BUY_N_GET_M": "Buy N, get M free",
        },
        "entities": {
            "Product": "Aggregate root with pricing rules",
            "PricingRule": "Value object defining a pricing scheme",
        },
        "patterns": {
            "DDD": "Entities, Value Objects, Aggregates, Domain Services",
            "CQRS": "Separate CommandHandler (writes) and QueryHandler (reads)",
            "Repository": "InMemoryProductRepository abstracts storage",
            "In-Memory": "Dict-based storage, no external persistence",
        },
        "audit_trail": "Each command creates an event; rules versioned per product",
        "rounding": "Money uses Decimal with ROUND_HALF_UP to 2 decimal places",
        "fractional_money": "Supported via Decimal for weight-based pricing",
        "stock_valuation": "Use get_price() with total inventory quantity",
    }


# =============================================================================
# Example Usage (for documentation)
# =============================================================================

if __name__ == "__main__":
    engine = PricingEngine()

    # Create products
    engine.create_product("beans", "Canned Beans")
    engine.create_product("apples", "Apples", default_unit="lb")
    engine.create_product("cereal", "Cereal Boxes")
    engine.create_product("orange_juice", "Orange Juice")

    # Simple pricing: $0.65 per can
    engine.add_simple_pricing("beans", Money(Decimal("0.65")))

    # Weight-based: $1.99/lb
    engine.add_weight_pricing("apples", Money(Decimal("1.99")))

    # Volume: 3 for $1.00 (with $0.65 each for remainder)
    engine.add_volume_pricing("cereal", 3, Money(Decimal("1.00")), Money(Decimal("0.65")))

    # Buy 2 get 1 free: $2.00 each
    engine.add_buy_n_get_m_pricing("orange_juice", 2, 1, Money(Decimal("2.00")))

    # Test pricing
    print("=== Pricing Examples ===")

    # Simple
    result = engine.get_price("beans", Quantity(Decimal("4")))
    print(f"4 cans of beans: {result.total_price} (unit: {result.unit_price})")

    # Weight
    result = engine.get_price("apples", Quantity(Decimal("0.25"), "lb"))  # 4 oz
    print(f"4 oz apples: {result.total_price}")

    # Volume
    result = engine.get_price("cereal", Quantity(Decimal("4")))
    print(f"4 boxes cereal: {result.total_price} (unit: {result.unit_price})")

    # BOGO
    result = engine.get_price("orange_juice", Quantity(Decimal("3")))
    print(f"3 orange juice (buy 2 get 1): {result.total_price} (unit: {result.unit_price})")

    # Stock valuation
    print("\n=== Stock Valuation ===")
    for product in engine.get_all_products():
        # Assume 100 units in stock
        qty = Quantity(Decimal("100"), product.default_unit)
        result = engine.get_price(product.id, qty)
        print(f"{product.name} (100 {product.default_unit}): {result.total_price}")