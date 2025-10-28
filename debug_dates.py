#!/usr/bin/env python
"""Debug date extraction."""

import re

line = "2021 - 2023"

# Find all 4-digit years
dates = re.findall(r'\b(19|20)\d{2}\b', line)
print(f"Line: {line}")
print(f"Dates found: {dates}")
print(f"Start: {dates[0]}, End: {dates[1]}")

# Actually let's just use a simpler pattern
dates2 = re.findall(r'\d{4}', line)
print(f"Simpler pattern: {dates2}")
