import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Set the Matplotlib backend to TkAgg
import matplotlib
matplotlib.use('TkAgg')


def map_plot(city, city_data, save_path):
    os.environ['SHAPE_RESTORE_SHX'] = 'YES'

    # Read SHP file
    shp_path = city_data + city + '.shp'
    pic = gpd.read_file(shp_path)

    # Read CSV file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)

    # Merge DataFrame into GeoDataFrame
    gdf = pd.merge(pic, df, left_index=True, right_index=True)

    # Select areas with type_id as 6
    unplanned_areas = gdf[gdf['type_id'] == 0]
    business_areas = gdf[gdf['type_id'] == 1]
    green_areas = gdf[gdf['type_id'] == 2]
    hospital_areas = gdf[gdf['type_id'] == 3]
    office_areas = gdf[gdf['type_id'] == 4]
    entertainment_areas = gdf[gdf['type_id'] == 5]
    yellow_areas = gdf[gdf['type_id'] == 6]
    school_areas = gdf[gdf['type_id'] == 7]

    # Create a figure object
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot all blocks with red borders
    # pic.plot(ax=ax, edgecolor='red', facecolor='none')
    try:
        unplanned_areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor='grey')
    except Exception as e:
        pass
    try:
        business_areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor='orangered')
    except Exception as e:
        pass
    try:
        green_areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor='forestgreen')
    except Exception as e:
        pass
    try:
        hospital_areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor='lightblue')
    except Exception as e:
        pass
    try:
        office_areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor='mediumorchid')
    except Exception as e:
        pass
    try:
        yellow_areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor='yellow')
    except Exception as e:
        pass
    try:
        entertainment_areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor='peru')
    except Exception as e:
        pass
    try:
        school_areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor='lightpink')
    except Exception as e:
        pass 

    # Create legend manually
    legend_elements = [
        Patch(facecolor='yellow', label='Residential Areas'),
        Patch(facecolor='grey', label='Planned Area'),
        Patch(facecolor='orangered', label='Business Area'),
        Patch(facecolor='forestgreen', label='Green Area'),
        Patch(facecolor='lightblue', label='Hospital Area'),
        Patch(facecolor='mediumorchid', label='Office Area'),
        Patch(facecolor='peru', label='Entertainment Area'),
        Patch(facecolor='lightpink', label='School Area'),
    ]

    # Add legend
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show the plot
    plt.savefig(save_path)


def map_plot_num(city, city_data, save_path):
    os.environ['SHAPE_RESTORE_SHX'] = 'YES'

    # Read SHP file
    shp_path = city_data + city + '.shp'
    pic = gpd.read_file(shp_path)

    # Read CSV file
    csv_path = city_data + city + '_GEO_INFO_COPY.csv'
    df = pd.read_csv(csv_path)

    # Merge DataFrame into GeoDataFrame
    gdf = pd.merge(pic, df, left_index=True, right_index=True)

    # Select areas with type_id as different categories
    unplanned_areas = gdf[gdf['type_id'] == 0]
    business_areas = gdf[gdf['type_id'] == 1]
    green_areas = gdf[gdf['type_id'] == 2]
    hospital_areas = gdf[gdf['type_id'] == 3]
    office_areas = gdf[gdf['type_id'] == 4]
    entertainment_areas = gdf[gdf['type_id'] == 5]
    yellow_areas = gdf[gdf['type_id'] == 6]
    school_areas = gdf[gdf['type_id'] == 7]

    # Create a figure object
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot all blocks with different colors
    area_types = [
        (unplanned_areas, 'grey', 'Planned Area'),
        (business_areas, 'orangered', 'Business Area'),
        (green_areas, 'forestgreen', 'Green Area'),
        (hospital_areas, 'lightblue', 'Hospital Area'),
        (office_areas, 'mediumorchid', 'Office Area'),
        (yellow_areas, 'yellow', 'Residential Areas'),
        (entertainment_areas, 'peru', 'Entertainment Area'),
        (school_areas, 'lightpink', 'School Area')
    ]

    for areas, color, label in area_types:
        try:
            areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor=color)
            # Add text annotation for each polygon using the 'num' column
            for idx, row in areas.iterrows():
                # Get the centroid of each geometry
                centroid = row.geometry.centroid
                # Plot the 'num' value for each area
                ax.text(centroid.x, centroid.y, str(row['num']), fontsize=10, fontweight='bold', ha='center', va='center', color='black')
        except Exception as e:
            pass

    # Create legend manually
    legend_elements = [
        Patch(facecolor='yellow', label='Residential Areas'),
        Patch(facecolor='grey', label='Planned Area'),
        Patch(facecolor='orangered', label='Business Area'),
        Patch(facecolor='forestgreen', label='Green Area'),
        Patch(facecolor='lightblue', label='Hospital Area'),
        Patch(facecolor='mediumorchid', label='Office Area'),
        Patch(facecolor='peru', label='Entertainment Area'),
        Patch(facecolor='lightpink', label='School Area'),
    ]

    # Add legend
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot
    plt.savefig(save_path)


# def map_plot_with_num(path):
#     import os
#     import geopandas as gpd
#     import pandas as pd
#     import matplotlib.pyplot as plt
#     from matplotlib.patches import Patch

#     os.environ['SHAPE_RESTORE_SHX'] = 'YES'

#     # Read SHP file
#     shp_path = 'data/beijing/BEIJING.shp'
#     pic = gpd.read_file(shp_path)

#     # Read CSV file
#     csv_path = path
#     df = pd.read_csv(csv_path)

#     # Merge DataFrame into GeoDataFrame
#     gdf = pd.merge(pic, df, left_index=True, right_index=True)

#     # Create a figure object
#     fig, ax = plt.subplots(figsize=(12, 6))

#     # Plot all blocks with red borders
#     pic.plot(ax=ax, edgecolor='red', facecolor='none')

#     # Iterate through each type_id and plot the corresponding areas
#     for type_id, color in zip([1, 2, 3, 4, 5, 6, 7],
#                               ['orangered', 'forestgreen', 'lightblue',
#                                'mediumorchid', 'peru', 'yellow', 'lightpink']):
#         areas = gdf[gdf['type_id'] == type_id]
#         areas.plot(ax=ax, edgecolor='white', linewidth=1.9, facecolor=color)

#         # Add labels with 'num' values for each area
#         for x, y, label in zip(areas.geometry.centroid.x,
#                               areas.geometry.centroid.y,
#                               areas['num']):
#             ax.text(x, y, str(label), fontsize=8, ha='center', va='center')

#     # Create legend manually
#     legend_elements = [
#         Patch(facecolor='yellow', label='Residential Areas'),
#         Patch(facecolor='grey', label='Planned Area'),
#         Patch(facecolor='orangered', label='Business Area'),
#         Patch(facecolor='forestgreen', label='Green Area'),
#         Patch(facecolor='lightblue', label='Hospital Area'),
#         Patch(facecolor='mediumorchid', label='Office Area'),
#         Patch(facecolor='peru', label='Entertainment Area'),
#         Patch(facecolor='lightpink', label='School Area'),
#     ]

#     # Add legend
#     ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

#     # Show the plot
#     plt.show()

# map_plot('loc.csv')
