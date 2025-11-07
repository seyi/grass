#!/usr/bin/env python3
"""
Create an interactive map of Kogi State, Nigeria with terrain overlay.
"""

import folium
from folium import plugins
import rasterio
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
import base64
from io import BytesIO
from PIL import Image

# Kogi State center coordinates
KOGI_CENTER = [7.25, 7.0]

print("Loading elevation data...")
# Load the SRTM elevation data
with rasterio.open('/tmp/kogi_srtm/srtm_38_11.tif') as src:
    # Read the data
    elevation = src.read(1)
    bounds = src.bounds

    # Set region to Kogi State (6°N-8.5°N, 6°E-8°E)
    kogi_bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]

    print(f"Elevation range: {elevation.min()} to {elevation.max()} meters")
    print(f"Bounds: {bounds}")

# Create the base map
print("Creating interactive map...")
m = folium.Map(
    location=KOGI_CENTER,
    zoom_start=9,
    tiles=None,
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

# Add satellite layer
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

# Add elevation overlay using ImageOverlay
print("Adding elevation overlay...")
# Create colored elevation overlay
norm = Normalize(vmin=0, vmax=700)  # Normalize elevation values
colormap = cm.get_cmap('terrain')  # Use terrain colormap

# Apply colormap to elevation data
colored_elevation = colormap(norm(np.ma.masked_less(elevation, -100)))
# Convert to PIL Image
img = Image.fromarray((colored_elevation[:, :, :3] * 255).astype(np.uint8))

# Convert to base64 for embedding
buffered = BytesIO()
img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Add as ImageOverlay
folium.raster_layers.ImageOverlay(
    image=f'data:image/png;base64,{img_str}',
    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
    opacity=0.6,
    interactive=True,
    cross_origin=False,
    zindex=1,
    name='Elevation Data (SRTM 90m)'
).add_to(m)

# Add Kogi State boundary (approximate)
kogi_state_bounds = [
    [6.0, 6.0],   # Southwest
    [6.0, 8.0],   # Southeast
    [8.5, 8.0],   # Northeast
    [8.5, 6.0],   # Northwest
    [6.0, 6.0]    # Close polygon
]

folium.Polygon(
    locations=kogi_state_bounds,
    color='red',
    fill=False,
    weight=3,
    popup='Kogi State (Approximate Boundary)',
    tooltip='Kogi State',
).add_to(m)

# Add markers for major cities
cities = [
    {'name': 'Lokoja (Capital)', 'coords': [7.8, 6.75], 'info': 'State capital, confluence of Niger and Benue rivers'},
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

# Add elevation legend
legend_html = '''
<div style="position: fixed;
     bottom: 50px; right: 50px; width: 150px; height: 200px;
     background-color: white; border:2px solid grey; z-index:9999;
     font-size:12px; padding: 10px; opacity: 0.9; border-radius: 5px;">
     <h4 style="margin-top:0;">Elevation (m)</h4>
     <div style="background: linear-gradient(to top,
          #0d5302 0%, #1a7a05 20%, #8bc34a 40%,
          #fff59d 60%, #d4a574 80%, #8b4513 100%);
          height: 120px; width: 30px; float: left;"></div>
     <div style="float: left; margin-left: 10px;">
         <div style="height: 20px;">700</div>
         <div style="height: 20px; margin-top: 20px;">560</div>
         <div style="height: 20px; margin-top: 20px;">420</div>
         <div style="height: 20px; margin-top: 20px;">280</div>
         <div style="height: 20px; margin-top: 20px;">140</div>
         <div style="height: 20px; margin-top: 6px;">0</div>
     </div>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

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
     top: 10px; left: 50px; width: 450px; height: 100px;
     background-color: white; border:2px solid grey; z-index:9999;
     font-size:14px; padding: 10px; opacity: 0.9; border-radius: 5px;">
     <h4 style="margin-top:0;">Kogi State, Nigeria - Interactive Terrain Map</h4>
     <p style="margin-bottom:0;">
         <b>Elevation:</b> -1m to 665m | <b>Mean:</b> 184m<br>
         Data: SRTM 90m | Click markers for info | Toggle layers
     </p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save the map
output_file = 'kogi_interactive_map_with_elevation.html'
m.save(output_file)
print(f'\n✓ Interactive map with elevation overlay saved to {output_file}')
print(f'✓ Open this file in your web browser to view the map.')
print(f'✓ Use the layer control to toggle the elevation overlay on/off')
