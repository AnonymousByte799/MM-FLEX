tools = """
{
Function Name: debate
Description: Retrieves opinions from three different stakeholders (residents, businesses, and developers) regarding a specific plot of land. This function provides a diverse set of perspectives, offering insights into the potential social, economic, and environmental impacts of development decisions. By considering these varied viewpoints, decision-makers can better understand the multifaceted implications of their actions on different community segments.
Parameters: None.
Example:
- Usage example: debate
  - This call returns the opinions of three different stakeholders (a resident, a business owner, and a developer) on a specific plot of land. Each opinion reflects the unique interests and concerns of the stakeholder, providing a comprehensive understanding of the potential impacts of land development or changes.
}
{
Function Name: query_info
Description: Retrieves detailed information about a specific location, including the types of surrounding plots and the area of the plot itself.
Parameters:
- query: Int. The Serial Number of the location, which is an integer.
Example:
- Usage example: query_info 25
  - This call returns details about the area at Serial Number 25, including the types of surrounding plots and the area of the plot.
}
{
Function Name: query_area
Description: Calculates the percentage of a specific land type in the entire region, providing insights into the distribution of various area types across the region.
Parameters:
- area_type: String. The type of land (e.g., Residential Area, Green Area, Business Area, etc.) for which the percentage calculation is requested.
Example:
- Usage example: query_area Residential Area
  - This call calculates and returns the percentage of Residential Areas in the region.
}
{
Function Name: query_influ
Description: Retrieves the impact on the entire region when a specific plot (identified by its Serial Number) adopts a certain area type. This function provides insights into how changing the type of a single plot can affect the overall area dynamics and planning considerations.
Parameters:
- Serial Number: Int. The numerical identifier of the plot for which the impact analysis is requested.
- area_type: String. The type of land (e.g., Residential Area, Green Area, Business Area, etc.) that the plot is being considered for conversion to.
Usage Example:
- Example command: query_influ 14 Residential Area
  - This call assesses and returns the impact on the entire region if the plot with Serial Number 14 were to be converted into a Residential Area.
}
"""

mm_tools = """
{
Function Name: debate
Description: Retrieves opinions from three different stakeholders (residents, businesses, and developers) regarding a specific plot of land. This function provides a diverse set of perspectives, offering insights into the potential social, economic, and environmental impacts of development decisions. By considering these varied viewpoints, decision-makers can better understand the multifaceted implications of their actions on different community segments.
Parameters: None.
Example:
- Usage example: debate
  - This call returns the opinions of three different stakeholders (a resident, a business owner, and a developer) on a specific plot of land. Each opinion reflects the unique interests and concerns of the stakeholder, providing a comprehensive understanding of the potential impacts of land development or changes.
}
{
Function Name: query_area
Description: Calculates the percentage of a specific land type in the entire region, providing insights into the distribution of various area types across the region.
Parameters:
- area_type: String. The type of land (e.g., Residential Area, Green Area, Business Area, etc.) for which the percentage calculation is requested.
Example:
- Usage example: query_area Residential Area
  - This call calculates and returns the percentage of Residential Areas in the region.
}
{
Function Name: query_influ
Description: Retrieves the impact on the entire region when a specific plot (identified by its Serial Number) adopts a certain area type. This function provides insights into how changing the type of a single plot can affect the overall area dynamics and planning considerations.
Parameters:
- Serial Number: Int. The numerical identifier of the plot for which the impact analysis is requested.
- area_type: String. The type of land (e.g., Residential Area, Green Area, Business Area, etc.) that the plot is being considered for conversion to.
Usage Example:
- Example command: query_influ 14 Residential Area
  - This call assesses and returns the impact on the entire region if the plot with Serial Number 14 were to be converted into a Residential Area.
}
"""