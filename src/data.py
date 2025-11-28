"""Core data structures for the fitness center assistant."""

from typing import Dict, List

# Membership plans with monthly prices
plans: Dict[str, float] = {
    "Basic": 25.0,
    "Plus": 35.0,
    "Premium": 50.0
}

# Class schedule by day of week
class_schedule: Dict[str, List[str]] = {
    "monday": [
        "Yoga Flow - 6:00 AM",
        "HIIT Training - 7:30 PM"
    ],
    "tuesday": [
        "Spin Class - 6:30 AM",
        "Strength Training - 6:00 PM"
    ],
    "wednesday": [
        "Pilates - 7:00 AM",
        "Cardio Blast - 5:30 PM"
    ],
    "thursday": [
        "Morning Run Club - 6:00 AM",
        "CrossFit - 6:30 PM"
    ],
    "friday": [
        "Yoga Relaxation - 7:00 AM",
        "Dance Fitness - 5:00 PM"
    ],
    "saturday": [
        "Bootcamp - 8:00 AM",
        "Swimming Lessons - 10:00 AM"
    ],
    "sunday": [
        "Stretch & Restore - 9:00 AM",
        "Cycling - 11:00 AM"
    ]
}

# Promo codes with discount rates (as decimals)
promo_codes: Dict[str, float] = {
    "WELCOME10": 0.10,
    "FALL5": 0.05
}

