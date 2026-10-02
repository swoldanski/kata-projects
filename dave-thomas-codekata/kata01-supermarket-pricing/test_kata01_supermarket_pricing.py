"""Tests for Kata01: Supermarket Pricing."""

from decimal import Decimal

import pytest
from kata01_supermarket_pricing import (
    InMemoryProductRepository,
    Money,
    PricingEngine,
    PricingRule,
    PricingService,
    PricingType,
    Product,
    Quantity,
    design_pricing_model,
)


class TestSupermarketPricing:
    """Test cases for Kata01: Supermarket Pricing."""

    def setup_method(self):
        """Create a fresh pricing engine for each test."""
        self.engine = PricingEngine()
        self._setup_products()

    def _setup_products(self):
        """Set up the standard product catalog from the kata."""
        # Simple pricing: beans at $0.65 each
        self.engine.create_product("beans", "Canned Beans")
        self.engine.add_simple_pricing("beans", Money(Decimal("0.65")))

        # Weight-based: apples at $1.99/lb
        self.engine.create_product("apples", "Apples", default_unit="lb")
        self.engine.add_weight_pricing("apples", Money(Decimal("1.99")))

        # Volume: cereal 3 for $1.00, $0.65 each for remainder
        self.engine.create_product("cereal", "Cereal Boxes")
        self.engine.add_volume_pricing("cereal", 3, Money(Decimal("1.00")), Money(Decimal("0.65")))

        # Buy 2 get 1 free: orange juice at $2.00 each
        self.engine.create_product("orange_juice", "Orange Juice")
        self.engine.add_buy_n_get_m_pricing("orange_juice", 2, 1, Money(Decimal("2.00")))

    # =========================================================================
    # Basic Cases from README
    # =========================================================================

    def test_simple_pricing_single_item(self):
        """Simple price: 1 can of beans at $0.65."""
        result = self.engine.get_price("beans", Quantity(Decimal("1")))
        assert result.total_price == Money(Decimal("0.65"))
        assert result.applied_rule.pricing_type == PricingType.SIMPLE

    def test_simple_pricing_multiple_items(self):
        """Simple price: 4 cans of beans at $0.65 each = $2.60."""
        result = self.engine.get_price("beans", Quantity(Decimal("4")))
        assert result.total_price == Money(Decimal("2.60"))

    def test_volume_pricing_exact_multiple(self):
        """Volume: 3 boxes cereal for $1.00."""
        result = self.engine.get_price("cereal", Quantity(Decimal("3")))
        assert result.total_price == Money(Decimal("1.00"))

    def test_volume_pricing_with_remainder(self):
        """Volume: 4 boxes cereal = 3 for $1.00 + 1 at $0.65 = $1.65."""
        result = self.engine.get_price("cereal", Quantity(Decimal("4")))
        assert result.total_price == Money(Decimal("1.65"))

    def test_volume_pricing_large_quantity(self):
        """Volume: 10 boxes cereal = 3 sets of 3 for $1.00 + 1 at $0.65 = $3.65."""
        result = self.engine.get_price("cereal", Quantity(Decimal("10")))
        assert result.total_price == Money(Decimal("3.65"))

    def test_weight_pricing(self):
        """Weight: 4 oz apples = 0.25 lb at $1.99/lb = $0.50."""
        result = self.engine.get_price("apples", Quantity(Decimal("0.25"), "lb"))
        assert result.total_price == Money(Decimal("0.50"))

    def test_weight_pricing_one_pound(self):
        """Weight: 1 lb apples = $1.99."""
        result = self.engine.get_price("apples", Quantity(Decimal("1"), "lb"))
        assert result.total_price == Money(Decimal("1.99"))

    def test_buy_n_get_m_free_exact(self):
        """Buy 2 get 1 free: 3 orange juice = pay for 2 at $2.00 = $4.00."""
        result = self.engine.get_price("orange_juice", Quantity(Decimal("3")))
        assert result.total_price == Money(Decimal("4.00"))

    def test_buy_n_get_m_free_multiple_deals(self):
        """Buy 2 get 1 free: 6 orange juice = 2 deals = pay for 4 = $8.00."""
        result = self.engine.get_price("orange_juice", Quantity(Decimal("6")))
        assert result.total_price == Money(Decimal("8.00"))

    def test_buy_n_get_m_free_with_remainder(self):
        """Buy 2 get 1 free: 4 orange juice = 1 deal (3) + 1 at $2.00 = $6.00."""
        result = self.engine.get_price("orange_juice", Quantity(Decimal("4")))
        assert result.total_price == Money(Decimal("6.00"))

    def test_buy_n_get_m_free_remainder_less_than_buy(self):
        """Buy 2 get 1 free: 5 orange juice = 1 deal (3) + 2 at $2.00 = $8.00."""
        result = self.engine.get_price("orange_juice", Quantity(Decimal("5")))
        assert result.total_price == Money(Decimal("8.00"))

    # =========================================================================
    # Edge Cases
    # =========================================================================

    def test_zero_quantity(self):
        """Zero quantity should return $0.00."""
        result = self.engine.get_price("beans", Quantity(Decimal("0")))
        assert result.total_price == Money(Decimal("0.00"))

    def test_product_not_found(self):
        """Unknown product should raise ValueError."""
        with pytest.raises(ValueError, match="Product not found"):
            self.engine.get_price("unknown", Quantity(Decimal("1")))

    def test_no_pricing_rule(self):
        """Product without pricing rule should raise ValueError."""
        self.engine.create_product("no_price", "No Price Product")
        with pytest.raises(ValueError, match="No pricing rule"):
            self.engine.get_price("no_price", Quantity(Decimal("1")))

    def test_fractional_money_precision(self):
        """Money calculations should use proper decimal precision."""
        # 3 for $1.00 means each is $0.333..., but we use $0.65 for remainder
        result = self.engine.get_price("cereal", Quantity(Decimal("4")))
        # $1.00 + $0.65 = $1.65 (not $1.33)
        assert result.total_price == Money(Decimal("1.65"))

    def test_money_arithmetic(self):
        """Money value object should support arithmetic."""
        m1 = Money(Decimal("1.00"))
        m2 = Money(Decimal("2.50"))
        assert m1 + m2 == Money(Decimal("3.50"))
        assert m1 * 3 == Money(Decimal("3.00"))

    def test_money_equality(self):
        """Money equality should work correctly."""
        assert Money(Decimal("1.00")) == Money(Decimal("1.00"))
        assert Money(Decimal("1.00")) != Money(Decimal("1.01"))

    def test_quantity_with_units(self):
        """Quantity should support different units."""
        qty_each = Quantity(Decimal("5"), "each")
        qty_lb = Quantity(Decimal("2.5"), "lb")
        assert qty_each.unit == "each"
        assert qty_lb.unit == "lb"
        # Quantity normalizes to 3 decimal places
        assert str(qty_lb) == "2.500 lb"

    # =========================================================================
    # TDD Progression - Following the kata's suggested progression
    # =========================================================================

    def test_tdd_step_1_simple_price_per_item(self):
        """Step 1: Simple price per item (beans at $0.65)."""
        result = self.engine.get_price("beans", Quantity(Decimal("1")))
        assert result.total_price == Money(Decimal("0.65"))

    def test_tdd_step_2_volume_pricing_three_for_dollar(self):
        """Step 2: Three for a dollar (cereal)."""
        result = self.engine.get_price("cereal", Quantity(Decimal("3")))
        assert result.total_price == Money(Decimal("1.00"))

    def test_tdd_step_3_volume_pricing_four_items(self):
        """Step 3: What's the price if I buy 4?"""
        result = self.engine.get_price("cereal", Quantity(Decimal("4")))
        assert result.total_price == Money(Decimal("1.65"))

    def test_tdd_step_4_weight_based_pricing(self):
        """Step 4: $1.99/pound (4 ounces = 0.25 lb)."""
        result = self.engine.get_price("apples", Quantity(Decimal("0.25"), "lb"))
        assert result.total_price == Money(Decimal("0.50"))

    def test_tdd_step_5_buy_two_get_one_free(self):
        """Step 5: Buy two, get one free."""
        result = self.engine.get_price("orange_juice", Quantity(Decimal("3")))
        assert result.total_price == Money(Decimal("4.00"))

    def test_tdd_step_6_stock_valuation(self):
        """Step 6: Value shelf of 100 cans with buy 2 get 1 free."""
        # 100 items with buy 2 get 1 free = 33 deals (99) + 1 = 67 paid
        result = self.engine.get_price("orange_juice", Quantity(Decimal("100")))
        # 33 deals * 2 paid = 66, remainder 1 = 67 paid * $2.00 = $134.00
        assert result.total_price == Money(Decimal("134.00"))

    # =========================================================================
    # Design Document Tests
    # =========================================================================

    def test_design_pricing_model_returns_document(self):
        """design_pricing_model() should return a design document dict."""
        doc = design_pricing_model()
        assert isinstance(doc, dict)
        assert "value_objects" in doc
        assert "pricing_types" in doc
        assert "entities" in doc
        assert "patterns" in doc
        assert "DDD" in doc["patterns"]
        assert "CQRS" in doc["patterns"]
        assert "Repository" in doc["patterns"]
        assert "In-Memory" in doc["patterns"]

    # =========================================================================
    # Architecture Pattern Tests
    # =========================================================================

    def test_repository_pattern(self):
        """Repository should abstract storage."""
        repo = InMemoryProductRepository()
        product = Product(id="test", name="Test")
        repo.save(product)
        assert repo.find_by_id("test") == product
        assert repo.find_all() == [product]

    def test_cqrs_separation(self):
        """Commands and queries should be separated."""
        # Write through command handler
        self.engine.create_product("new_product", "New Product")
        self.engine.add_simple_pricing("new_product", Money(Decimal("5.00")))
        # Read through query handler
        result = self.engine.get_price("new_product", Quantity(Decimal("1")))
        assert result.total_price == Money(Decimal("5.00"))

    def test_domain_service_encapsulation(self):
        """Pricing logic should be in domain service."""
        service = PricingService(self.engine._repository)
        # Repository has product, service calculates
        result = service.calculate_price("beans", Quantity(Decimal("2")))
        assert result == Money(Decimal("1.30"))

    def test_aggregate_root_product(self):
        """Product should be aggregate root managing pricing rules."""
        product = Product(id="test", name="Test")
        rule = PricingRule(
            product_id="test",
            pricing_type=PricingType.SIMPLE,
            price_per_unit=Money(Decimal("1.00"))
        )
        product.add_pricing_rule(rule)
        assert len(product.pricing_rules) == 1
        assert product.get_applicable_rule(Quantity(Decimal("1"))) == rule

    def test_value_object_immutability(self):
        """Money and Quantity should be immutable."""
        money = Money(Decimal("1.00"))
        qty = Quantity(Decimal("1"), "each")
        # Can't modify frozen dataclass
        with pytest.raises(AttributeError):
            money.amount = Decimal("2.00")
        with pytest.raises(AttributeError):
            qty.amount = Decimal("2")

    def test_money_rounding(self):
        """Money should round to 2 decimal places."""
        m = Money(Decimal("1.005"))  # Should round to 1.01
        assert m.amount == Decimal("1.01")
        m = Money(Decimal("1.004"))  # Should round to 1.00
        assert m.amount == Decimal("1.00")

    def test_money_currency_mismatch(self):
        """Adding different currencies should raise error."""
        m1 = Money(Decimal("1.00"), "USD")
        m2 = Money(Decimal("1.00"), "EUR")
        with pytest.raises(ValueError, match="different currencies"):
            m1 + m2


class TestPricingRules:
    """Tests for specific pricing rule validation."""

    def test_simple_rule_requires_price(self):
        """SIMPLE rule requires price_per_unit."""
        with pytest.raises(ValueError, match="price_per_unit"):
            PricingRule(product_id="p1", pricing_type=PricingType.SIMPLE)

    def test_volume_rule_requires_volume_params(self):
        """VOLUME rule requires volume_quantity and volume_price."""
        with pytest.raises(ValueError, match="volume_quantity"):
            PricingRule(
                product_id="p1", pricing_type=PricingType.VOLUME,
                volume_price=Money(Decimal("1")),
            )

    def test_weight_rule_requires_price(self):
        """WEIGHT rule requires price_per_unit."""
        with pytest.raises(ValueError, match="price_per_unit"):
            PricingRule(product_id="p1", pricing_type=PricingType.WEIGHT)

    def test_buy_n_get_m_requires_quantities(self):
        """BUY_N_GET_M rule requires buy_quantity and get_quantity."""
        with pytest.raises(ValueError, match="buy_quantity"):
            PricingRule(product_id="p1", pricing_type=PricingType.BUY_N_GET_M, get_quantity=1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])