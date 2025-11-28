"""Schedule utilities for class management."""

from typing import List, Dict


def normalized_day(day: str) -> str:
    """
    Normalize day name to lowercase full day name.
    
    Args:
        day: Day string (case-insensitive, can be abbreviation)
        
    Returns:
        Normalized day name (monday, tuesday, etc.)
    """
    day_lower = day.lower().strip()
    
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
    
    return day_mapping.get(day_lower, day_lower)


def day_classes(day: str, schedule: Dict[str, List[str]]) -> List[str]:
    """
    Get classes for a specific day from the schedule.
    
    Args:
        day: Day of the week
        schedule: Dictionary mapping days to lists of class strings
        
    Returns:
        List of class strings for the day
    """
    normalized = normalized_day(day)
    return schedule.get(normalized, [])

