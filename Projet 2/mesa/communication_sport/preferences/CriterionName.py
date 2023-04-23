#!/usr/bin/env python3

from enum import Enum


class CriterionName(Enum):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName."""
    
    SKILL_REQUIRED = 1
    PHYSICAL_INTENSITY = 2
    POPULARITY = 3
    ENTERTAINMENT_VALUE = 4
    TEAM_PLAY = 5
    
