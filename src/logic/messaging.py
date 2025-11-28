"""Messaging functions for greetings and reminders."""

from typing import List


def build_welcome(name: str, center: str = "Baun Fitness Center") -> str:
    """
    Build a personalized welcome message.
    
    Args:
        name: User's name
        center: Name of the fitness center
        
    Returns:
        Formatted welcome message string
    """
    return f"Welcome to {center}, {name}! We're excited to help you achieve your fitness goals. 🏋️"


def reminders(day: str, schedule: dict[str, list[str]]) -> List[str]:
    """
    Get class reminders for a specific day.
    
    Args:
        day: Day of the week (case-insensitive)
        schedule: Dictionary mapping days to lists of class strings
        
    Returns:
        List of class strings for the day, or empty list if no classes
    """
    day_lower = day.lower().strip()
    
    # Normalize day name
    day_mapping = {
        "monday": "monday",
        "tuesday": "tuesday",
        "wednesday": "wednesday",
        "thursday": "thursday",
        "friday": "friday",
        "saturday": "saturday",
        "sunday": "sunday",
        "mon": "monday",
        "tue": "tuesday",
        "wed": "wednesday",
        "thu": "thursday",
        "fri": "friday",
        "sat": "saturday",
        "sun": "sunday"
    }
    
    normalized = day_mapping.get(day_lower, day_lower)
    return schedule.get(normalized, [])

