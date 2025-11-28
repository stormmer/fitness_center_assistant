"""Pricing calculations for membership plans."""

from typing import Dict, Optional


def price_membership(
    plan: str,
    months: int,
    is_student_or_staff: bool,
    promo: Optional[str],
    plans: Dict[str, float],
    promo_codes: Dict[str, float]
) -> Dict:
    """
    Calculate membership pricing with discounts and promo codes.
    
    Args:
        plan: Membership plan name (must exist in plans dict)
        months: Number of months (must be > 0)
        is_student_or_staff: Whether user qualifies for student/staff discount
        promo: Optional promo code string
        plans: Dictionary of plan names to monthly prices
        promo_codes: Dictionary of promo codes to discount rates
        
    Returns:
        Dictionary with pricing breakdown:
        {
            "plan": str,
            "months": int,
            "monthly_price": float,
            "base_cost": float,
            "student_staff_discount": float,
            "promo_applied": str | None,
            "promo_rate": float,
            "final_cost": float
        }
        
    Raises:
        ValueError: If plan is invalid or months <= 0
    """
    if plan not in plans:
        raise ValueError(f"Invalid plan: {plan}. Available plans: {list(plans.keys())}")
    
    if months <= 0:
        raise ValueError(f"Months must be greater than 0, got {months}")
    
    monthly_price = plans[plan]
    base_cost = monthly_price * months
    
    # Student/staff discount: 15% off
    student_staff_discount_rate = 0.15 if is_student_or_staff else 0.0
    student_staff_discount = base_cost * student_staff_discount_rate
    cost_after_student_discount = base_cost - student_staff_discount
    
    # Promo code discount (applied after student/staff discount)
    promo_applied = None
    promo_rate = 0.0
    promo_discount = 0.0
    
    if promo:
        promo_upper = promo.strip().upper()
        if promo_upper in promo_codes:
            promo_applied = promo_upper
            promo_rate = promo_codes[promo_upper]
            promo_discount = cost_after_student_discount * promo_rate
        else:
            # Invalid promo code - we'll note it but don't apply
            promo_applied = None
    
    final_cost = cost_after_student_discount - promo_discount
    
    return {
        "plan": plan,
        "months": months,
        "monthly_price": monthly_price,
        "base_cost": base_cost,
        "student_staff_discount": student_staff_discount,
        "promo_applied": promo_applied,
        "promo_rate": promo_rate,
        "final_cost": max(0.0, final_cost)  # Ensure non-negative
    }

