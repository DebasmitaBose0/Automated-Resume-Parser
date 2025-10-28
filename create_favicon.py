#!/usr/bin/env python
"""Create favicon.png for the Resume Parser application"""

try:
    from PIL import Image, ImageDraw
    
    # Create a new image with gradient-like background
    size = 64
    img = Image.new('RGB', (size, size), color=(102, 126, 234))
    
    # Draw gradient background
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Fill with purple gradient
    for i in range(size):
        r = int(102 + (118 - 102) * i / size)
        g = int(126 + (75 - 126) * i / size)
        b = int(234 + (162 - 234) * i / size)
        draw.line([(0, i), (size, i)], fill=(r, g, b))
    
    # Draw document background
    draw.rectangle([12, 8, 44, 52], fill='white', outline=None)
    
    # Draw lines (text representation)
    draw.line([(16, 14), (40, 14)], fill=(102, 126, 234), width=2)
    draw.line([(16, 20), (40, 20)], fill=(102, 126, 234), width=2)
    draw.line([(16, 26), (40, 26)], fill=(102, 126, 234), width=2)
    draw.line([(16, 32), (32, 32)], fill=(118, 75, 162), width=2)
    
    # Draw checkmark circle
    draw.ellipse([36, 36, 56, 56], fill=(254, 202, 87))
    
    # Draw checkmark
    draw.line([(41, 45), (45, 49)], fill='white', width=2)
    draw.line([(45, 49), (52, 42)], fill='white', width=2)
    
    # Save the image
    img.save('static/favicon.png')
    print('✓ Favicon PNG created successfully!')
    
except ImportError:
    print('Error: Pillow (PIL) not installed. Using SVG-only favicon.')
    print('To create PNG favicon, install Pillow: pip install Pillow')
except Exception as e:
    print(f'Error creating favicon: {e}')
