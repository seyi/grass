#!/usr/bin/env python3
"""
Create an interactive map of Kogi State, Nigeria with terrain, boundaries, and roads.
"""

import folium
from folium import plugins
import json

# Kogi State center coordinates
KOGI_CENTER = [7.25, 7.0]  # Approximate center of Kogi State

# Create the base map
m = folium.Map(
    location=KOGI_CENTER,
    zoom_start=9,
    tiles=None,  # We'll add custom tiles
)

# Add different base map options
folium.TileLayer(
    'OpenStreetMap',
    name='Street Map',
    overlay=False,
    control=True
).add_to(m)

folium.TileLayer(
    'CartoDB positron',
    name='Light Map',
    overlay=False,
    control=True
).add_to(m)

folium.TileLayer(
    'CartoDB dark_matter',
    name='Dark Map',
    overlay=False,
    control=True
).add_to(m)

# Add terrain/satellite layer
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite',
    overlay=False,
    control=True
).add_to(m)

# Add topographic layer
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Topographic',
    overlay=False,
    control=True
).add_to(m)

# Add Kogi State boundary (approximate rectangle)
# Note: For actual boundaries, we'd need GeoJSON data from GADM or similar
kogi_bounds = [
    [6.0, 6.0],   # Southwest corner
    [6.0, 8.0],   # Southeast corner
    [8.5, 8.0],   # Northeast corner
    [8.5, 6.0],   # Northwest corner
    [6.0, 6.0]    # Close the polygon
]

folium.Polygon(
    locations=kogi_bounds,
    color='red',
    fill=False,
    weight=3,
    popup='Kogi State (Approximate Boundary)',
    tooltip='Kogi State',
).add_to(m)

# Add markers for major cities in Kogi State
cities = [
    {'name': 'Lokoja (Capital)', 'coords': [7.8, 6.75], 'info': 'State capital, located at the confluence of Niger and Benue rivers'},
    {'name': 'Okene', 'coords': [7.55, 6.23], 'info': 'Major commercial center'},
    {'name': 'Kabba', 'coords': [7.83, 6.08], 'info': 'Administrative center'},
    {'name': 'Idah', 'coords': [7.11, 6.93], 'info': 'Historic town'},
    {'name': 'Ankpa', 'coords': [7.4, 7.63], 'info': 'Local government area'},
]

for city in cities:
    folium.Marker(
        location=city['coords'],
        popup=f"<b>{city['name']}</b><br>{city['info']}",
        tooltip=city['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Add elevation info
folium.Marker(
    location=[7.5, 7.5],
    popup="""
    <b>Kogi State Terrain Info</b><br>
    Elevation Range: -1m to 665m<br>
    Mean Elevation: 184m<br>
    Data Source: SRTM 90m
    """,
    icon=folium.Icon(color='green', icon='stats', prefix='fa')
).add_to(m)

# Add minimap
minimap = plugins.MiniMap(toggle_display=True)
m.add_child(minimap)

# Add fullscreen button
plugins.Fullscreen(
    position='topright',
    title='Enter fullscreen',
    title_cancel='Exit fullscreen',
    force_separate_button=True
).add_to(m)

# Add measure control
plugins.MeasureControl(
    position='topleft',
    primary_length_unit='kilometers',
    secondary_length_unit='miles',
    primary_area_unit='sqkilometers',
    secondary_area_unit='acres'
).add_to(m)

# Add mouse position
plugins.MousePosition().add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Add title
title_html = '''
<div style="position: fixed;
     top: 10px; left: 50px; width: 400px; height: 90px;
     background-color: white; border:2px solid grey; z-index:9999;
     font-size:14px; padding: 10px; opacity: 0.9; border-radius: 5px;">
     <h4 style="margin-top:0;">Kogi State, Nigeria - Interactive Terrain Map</h4>
     <p style="margin-bottom:0;">Elevation data from SRTM 90m. Click markers for info.</p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save the map
output_file = 'kogi_interactive_map.html'
m.save(output_file)
print(f'Interactive map saved to {output_file}')
print(f'Open this file in your web browser to view the map.')
