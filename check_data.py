#!/usr/bin/env python
"""Check candidate data in database."""

import sys
sys.path.insert(0, '/Resumeparser')

from app import create_app
from app.models import Candidate

app = create_app()
with app.app_context():
    candidates = Candidate.query.all()
    print(f'Total candidates: {len(candidates)}')
    for c in candidates:
        print(f'\nCandidate ID {c.id}: {c.name}')
        print(f'  Email: {c.email}')
        print(f'  Phone: {c.phone}')
        print(f'  Location: {c.location}')
        print(f'  Summary: {c.summary[:100] if c.summary else "None"}...')
        print(f'  Skills: {len(c.skills)}')
        print(f'  Education: {len(c.educations)}')
        print(f'  Experience: {len(c.experiences)}')
