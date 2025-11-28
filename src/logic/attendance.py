"""Attendance tracking and summarization."""

from typing import Dict


def add_entry(store: Dict[str, int], activity: str, count: int) -> Dict[str, int]:
    """
    Add an attendance entry to the store.
    
    Args:
        store: Dictionary mapping activity names to counts
        activity: Name of the activity
        count: Number of attendees (must be >= 0)
        
    Returns:
        Updated store dictionary
        
    Raises:
        ValueError: If count is negative
    """
    if count < 0:
        raise ValueError(f"Count must be non-negative, got {count}")
    
    activity_clean = activity.strip()
    if activity_clean:
        store[activity_clean] = store.get(activity_clean, 0) + count
    
    return store


def summarize(store: Dict[str, int]) -> Dict:
    """
    Summarize attendance data.
    
    Args:
        store: Dictionary mapping activity names to counts
        
    Returns:
        Dictionary with summary statistics:
        {
            "total": int,
            "avg_per_activity": float,
            "by_activity": dict
        }
    """
    if not store:
        return {
            "total": 0,
            "avg_per_activity": 0.0,
            "by_activity": {}
        }
    
    total = sum(store.values())
    num_activities = len(store)
    avg_per_activity = total / num_activities if num_activities > 0 else 0.0
    
    return {
        "total": total,
        "avg_per_activity": avg_per_activity,
        "by_activity": store.copy()
    }

