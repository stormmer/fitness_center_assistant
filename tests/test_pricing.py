"""Tests for pricing logic."""

import pytest
from src.logic.pricing import price_membership
from src.data import plans, promo_codes


@pytest.mark.parametrize("plan,months,is_student,promo,expected_final", [
    ("Basic", 1, False, None, 25.0),
    ("Basic", 3, False, None, 75.0),
    ("Plus", 2, False, None, 70.0),
    ("Premium", 1, False, None, 50.0),
    ("Basic", 1, True, None, 21.25),  # 15% discount
    ("Plus", 2, True, None, 59.50),   # 15% discount
    ("Basic", 1, False, "WELCOME10", 22.50),  # 10% promo
    ("Basic", 1, True, "WELCOME10", 19.125),  # 15% + 10% (stacked)
    ("Plus", 2, False, "FALL5", 66.50),  # 5% promo
])
def test_price_membership(plan, months, is_student, promo, expected_final):
    """Test pricing calculations with various inputs."""
    result = price_membership(
        plan=plan,
        months=months,
        is_student_or_staff=is_student,
        promo=promo,
        plans=plans,
        promo_codes=promo_codes
    )
    
    assert result['plan'] == plan
    assert result['months'] == months
    assert result['monthly_price'] == plans[plan]
    assert abs(result['final_cost'] - expected_final) < 0.01  # Allow floating point tolerance


def test_price_membership_invalid_plan():
    """Test that invalid plan raises ValueError."""
    with pytest.raises(ValueError, match="Invalid plan"):
        price_membership(
            plan="InvalidPlan",
            months=1,
            is_student_or_staff=False,
            promo=None,
            plans=plans,
            promo_codes=promo_codes
        )


def test_price_membership_invalid_months():
    """Test that months <= 0 raises ValueError."""
    with pytest.raises(ValueError, match="Months must be greater than 0"):
        price_membership(
            plan="Basic",
            months=0,
            is_student_or_staff=False,
            promo=None,
            plans=plans,
            promo_codes=promo_codes
        )


def test_price_membership_invalid_promo():
    """Test that invalid promo code is ignored."""
    result = price_membership(
        plan="Basic",
        months=1,
        is_student_or_staff=False,
        promo="INVALID",
        plans=plans,
        promo_codes=promo_codes
    )
    
    assert result['promo_applied'] is None
    assert result['final_cost'] == 25.0

