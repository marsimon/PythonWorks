import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Load GeoJSON files for Seoul and Gyeonggi regions
seoul_geojson_path = 'hangjeongdong_서울특별시.geojson'
gyeonggi_geojson_path = 'hangjeongdong_경기도.geojson'

# Read the GeoJSON files into GeoDataFrames
seoul_gdf = gpd.read_file(seoul_geojson_path)
gyeonggi_gdf = gpd.read_file(gyeonggi_geojson_path)

# Handle potential multi-part geometries by exploding them
seoul_gdf_exploded = seoul_gdf.explode(index_parts=True)
gyeonggi_gdf_exploded = gyeonggi_gdf.explode(index_parts=True)

# Load the latitude and longitude data from the provided file
latlong_file_path = 'korea_administrative_division_latitude_longitude.xlsx'
latlong_data = pd.read_excel(latlong_file_path)

# Create a GeoDataFrame for latitude and longitude data
latlong_gdf = gpd.GeoDataFrame(
    latlong_data, 
    geometry=gpd.points_from_xy(latlong_data['longitude'], latlong_data['latitude']),
    crs='EPSG:4326'
)

# Ensure that both GeoDataFrames use the same coordinate reference system (CRS)
seoul_gdf_exploded = seoul_gdf_exploded.to_crs(epsg=4326)
gyeonggi_gdf_exploded = gyeonggi_gdf_exploded.to_crs(epsg=4326)

# Function to assign region names based on latitude and longitude matching
def find_region_name(geometry, latlong_gdf):
    # Check if the point is inside any of the polygons (regions)
    for idx, row in latlong_gdf.iterrows():
        point = row['geometry']
        if geometry.contains(point):
            return row['city']  # Use the 'city' column as the region name
    return None

# Assign region names to each polygon in the GeoJSON file based on latitude and longitude data
seoul_gdf_exploded['Region'] = seoul_gdf_exploded['geometry'].apply(find_region_name, latlong_gdf=latlong_gdf)
gyeonggi_gdf_exploded['Region'] = gyeonggi_gdf_exploded['geometry'].apply(find_region_name, latlong_gdf=latlong_gdf)

# Example population movement data
regions = ['종로구', '중구', '용산구', '성동구', '광진구']  # Example regions
population_movement = [3355.476160, 752.529007, 310.364264, 578.803541, 69.811532]  # Example population movement data

# Create a DataFrame with regions and population movement
hwaseong_migration_final = pd.DataFrame({
    'Region': regions,
    'Population Movement': population_movement
})

# Function to match population movement data based on region names
def assign_population_movement(region_name):
    result = hwaseong_migration_final[hwaseong_migration_final['Region'] == region_name]
    return result['Population Movement'].values[0] if not result.empty else 0

# Add population movement to each GeoJSON region based on its assigned region name
seoul_gdf_exploded['Population Movement'] = seoul_gdf_exploded['Region'].apply(assign_population_movement)
gyeonggi_gdf_exploded['Population Movement'] = gyeonggi_gdf_exploded['Region'].apply(assign_population_movement)

# Plot the Seoul and Gyeonggi region maps with color based on population movement
fig, ax = plt.subplots(figsize=(10, 10))

# Plot Seoul and Gyeonggi with population movement data as color
seoul_gdf_exploded.plot(column='Population Movement', ax=ax, cmap='OrRd', legend=True, edgecolor='black')
gyeonggi_gdf_exploded.plot(column='Population Movement', ax=ax, cmap='OrRd', legend=True, edgecolor='black')

plt.title('Hwaseong City Population Movements to Seoul and Gyeonggi Regions')

# Show the plot
plt.show()
