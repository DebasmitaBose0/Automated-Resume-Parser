sample = """Babin Bid
babinbid05@gmail.com
(912) 377-7679"""

lines = sample.split('\n')[:15]
for i, line in enumerate(lines):
    print(f"Line {i}: '{line}'")
    print(f"  Stripped: '{line.strip()}'")
    print(f"  Length: {len(line.strip())}")
    print(f"  Has @: {'@' in line}")
    print(f"  Has phone chars: {any(c in line for c in ['(', ')', '-'])}")
    print()
