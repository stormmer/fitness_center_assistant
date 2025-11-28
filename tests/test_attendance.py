"""Tests for attendance logic."""

import pytest
from src.logic.attendance import add_entry, summarize


def test_add_entry_new_activity():
    """Test adding entry for new activity."""
    store = {}
    result = add_entry(store, "Yoga", 10)
    
    assert result["Yoga"] == 10
    assert store == result


def test_add_entry_existing_activity():
    """Test adding entry aggregates counts."""
    store = {"Yoga": 10}
    result = add_entry(store, "Yoga", 5)
    
    assert result["Yoga"] == 15


def test_add_entry_multiple_activities():
    """Test adding entries for multiple activities."""
    store = {}
    add_entry(store, "Yoga", 10)
    add_entry(store, "Spin", 15)
    add_entry(store, "Yoga", 5)
    
    assert store["Yoga"] == 15
    assert store["Spin"] == 15


def test_add_entry_negative_count():
    """Test that negative count raises ValueError."""
    store = {}
    with pytest.raises(ValueError, match="Count must be non-negative"):
        add_entry(store, "Yoga", -1)


def test_summarize_empty():
    """Test summarizing empty store."""
    store = {}
    result = summarize(store)
    
    assert result['total'] == 0
    assert result['avg_per_activity'] == 0.0
    assert result['by_activity'] == {}


def test_summarize_single_activity():
    """Test summarizing single activity."""
    store = {"Yoga": 10}
    result = summarize(store)
    
    assert result['total'] == 10
    assert result['avg_per_activity'] == 10.0
    assert result['by_activity'] == {"Yoga": 10}


def test_summarize_multiple_activities():
    """Test summarizing multiple activities."""
    store = {"Yoga": 10, "Spin": 20, "Pilates": 15}
    result = summarize(store)
    
    assert result['total'] == 45
    assert result['avg_per_activity'] == 15.0
    assert result['by_activity'] == {"Yoga": 10, "Spin": 20, "Pilates": 15}

