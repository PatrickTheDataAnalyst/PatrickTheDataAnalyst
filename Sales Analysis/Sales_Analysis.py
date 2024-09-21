import streamlit as st       # For creating the dashboard interface
import pandas as pd          # For handling data (reading, manipulating)
import matplotlib.pyplot as plt  # For creating plots
from itertools import combinations
from collections import Counter

# Load dataset from the local path
file_path = r'C:\Users\Patri\Documents\Data Analysis\Python\Sales Analysis\Combined sales data\exported_data.csv'

# Load the dataset
df = pd.read_csv(file_path)

# Display the dataset in the Streamlit app
st.title("Sales Analysis Dashboard")

# Create the plot for Monthly Sales
results = df.groupby('Month')['Sales'].sum()
months = range(1, 13)

# Define font properties for the title
font_dict = {
    'family': 'Times New Roman',
    'fontsize': 12,
    'weight': 'bold'
}

# Sidebar Filters
st.sidebar.header("Filters")

# Hour of the Day Filter
hour_filter = st.sidebar.slider(
    "Select Hour of the Day",
    min_value=1,
    max_value=24,
    value=(1, 24)
)

# Month Filter (Multi-select dropdown)
month_filter = st.sidebar.multiselect(
    "Select Months",
    options=df['Month'].unique(),  # Get unique months from the dataset
    default=df['Month'].unique()    # Default to selecting all months
)


# City Filter
city_filter = st.sidebar.multiselect(
    "Select Cities",
    options=df['City'].unique(),
    default=df['City'].unique()
)

# Product Filter
product_filter = st.sidebar.multiselect(
    "Select Products",
    options=df['Product'].unique(),
    default=df['Product'].unique()
)


# Create the filtered dataset based on the selected filters, including the month filter
df_filtered = df[
    (df['City'].isin(city_filter)) &  # City filter
    (df['Product'].isin(product_filter)) &  # Product filter
    (df['Hour'] >= hour_filter[0]) & (df['Hour'] <= hour_filter[1]) &  # Hour filter
    (df['Month'].isin(month_filter))  # Month filter
]

#FIGURE 1

# Group by 'Month' and sum the 'Sales' column from the filtered data
results_filtered = df_filtered.groupby('Month')['Sales'].sum()

# Create the bar chart with the filtered data
fig1, ax = plt.subplots(figsize=(8, 6))  # Smaller figure size

# Set the background color for the plot area
fig1.patch.set_facecolor('#012a4a')  # Plot area color (dark blue)

# Set bar color and plot the data using the filtered results
ax.bar(results_filtered.index, results_filtered.values, color='#a9d6e5')  # Bar color (light teal)

# Set the title and axis labels with white font color
ax.set_title('Monthly Sales', fontdict={'fontsize': 14, 'weight': 'bold', 'color': 'white'})
ax.set_xlabel('Months', fontsize=12, color='white')
ax.set_ylabel('Sales (USD in Millions)', fontsize=12, color='white')

# Set the axis background color
ax.set_facecolor('#012a4a')  # Axis area background color

# Set the tick parameters (both x and y axis) to have white labels
ax.tick_params(colors='white')  # Color of the tick labels


#FIGURE 2

# Group by 'City' and sum the 'Sales' column from the filtered data
result1_filtered = df_filtered.groupby('City')['Sales'].sum().sort_values(ascending=False)

# Create the bar chart for City Sales with the filtered data
fig2, ax = plt.subplots(figsize=(8, 5))  # Same figure size

# Set the background color for the plot area
fig2.patch.set_facecolor('#012a4a')  # Plot area color (dark blue)

# Set bar color and plot the data using the filtered results
ax.bar(result1_filtered.index, result1_filtered.values, color='#a9d6e5')  # Bar color (light teal)

# Set the title and axis labels with white font color
ax.set_title('Total Sales on Each City', fontdict={'fontsize': 14, 'weight': 'bold', 'color': 'white'})
ax.set_xlabel('City', fontsize=12, color='white')
ax.set_ylabel('Sales (USD in Millions)', fontsize=12, color='white')

# Set the axis background color
ax.set_facecolor('#012a4a')  # Axis area background color

# Set the tick parameters (both x and y axis) to have white labels
ax.tick_params(colors='white')  # Color of the tick labels

# Rotate the x-axis labels to avoid overlap
plt.xticks(rotation=45, ha='right', color='white')


#FIGURE 3

# Updated function to count orders by hour using the filtered data
def count_orders_by_hour(filtered_df):
    # Group by the 'Hour' column and count the number of occurrences
    hour_count = filtered_df.groupby('Hour').size().reindex(range(1, 25), fill_value=0)
    return hour_count

# Call the function with df_filtered to get the count of orders by hour
hour_counts_filtered = count_orders_by_hour(df_filtered)

# Create the line plot for Number of Orders by Hour with consistent colors and figure size
fig3, ax = plt.subplots(figsize=(8, 5))  # Same figure size

# Set the background color for the plot area
fig3.patch.set_facecolor('#012a4a')  # Plot area color (dark blue)

# Plot the line with the desired color using the filtered data
ax.plot(hour_counts_filtered.index, hour_counts_filtered.values, color='#a9d6e5')  # Line color (light teal)

# Set grid, title, and axis labels with white font color
ax.grid(True)
ax.set_xlabel('Hour of the Day (1 to 24)', fontsize=12, color='white')
ax.set_ylabel('Number of Orders', fontsize=12, color='white')
ax.set_title('Number of Orders by Hour', fontdict={'fontsize': 14, 'weight': 'bold', 'color': 'white'})

# Set the x-axis to show all hours from 1 to 24
ax.set_xticks(range(1, 25))

# Set the axis background color
ax.set_facecolor('#012a4a')  # Axis area background color

# Set the tick parameters to white
ax.tick_params(colors='white')


#TABLE PLOT

# Initialize a Counter object to keep track of pair frequencies
count = Counter()

# Loop through each row in the 'Grouped' column of df_filtered
for row in df_filtered['Grouped']:
    row_list = row.split(',')  # Split the grouped product string into a list of individual products
    count.update(Counter(combinations(row_list, 2)))  # Create all possible pairs of two products, count them, and update the Counter

# Get the 10 most common product pairs along with their counts
common_pairs = count.most_common(10)

# Convert the result into a dataframe for better display in Streamlit
pair_data = pd.DataFrame(common_pairs, columns=['Product Pair', 'Count'])

# Format the 'Product Pair' column (replace commas with '&')
pair_data['Product Pair'] = pair_data['Product Pair'].apply(lambda x: ' & '.join(x))

# Set index to start from 1
pair_data.index = pair_data.index + 1


#FIGURE 4 

# Ensure 'Quantity Ordered' is numeric (handling non-numeric values) in the filtered dataset
df_filtered['Quantity Ordered'] = pd.to_numeric(df_filtered['Quantity Ordered'], errors='coerce')

# Group by 'Product' and sum the 'Quantity Ordered' column from the filtered data
product_group_filtered = df_filtered.groupby('Product')['Quantity Ordered'].sum()

# Sort the products by 'Quantity Ordered' in descending order
product_group_sorted_filtered = product_group_filtered.sort_values(ascending=False)

# Create the bar chart for Sales by Product with the filtered data
fig4, ax = plt.subplots(figsize=(8, 5))  # Same figure size

# Set the background color for the plot area
fig4.patch.set_facecolor('#012a4a')  # Plot area color (dark blue)

# Set bar color and plot the data using the filtered results
ax.bar(product_group_sorted_filtered.index, product_group_sorted_filtered.values, color='#a9d6e5')  # Bar color (light teal)

# Set the title and axis labels with white font color
ax.set_title('Sales by Product', fontdict={'fontsize': 14, 'weight': 'bold', 'color': 'white'})
ax.set_xlabel('Product', fontsize=12, color='white')
ax.set_ylabel('Quantity Ordered', fontsize=12, color='white')

# Rotate the x-axis labels vertically to avoid overlap
ax.set_xticklabels(product_group_sorted_filtered.index, rotation='vertical', color='white')

# Set the axis background color
ax.set_facecolor('#012a4a')  # Axis area background color

# Set the tick parameters (both x and y axis) to have white labels
ax.tick_params(colors='white')


## FIGURE 5

# Ensure 'Quantity Ordered' and 'Price Each' are numeric in the filtered dataset
df_filtered['Quantity Ordered'] = pd.to_numeric(df_filtered['Quantity Ordered'], errors='coerce')
df_filtered['Price Each'] = pd.to_numeric(df_filtered['Price Each'], errors='coerce')

# Drop rows with missing or invalid data from the filtered data
cleaned_data_filtered = df_filtered.dropna(subset=['Quantity Ordered', 'Price Each'])

# Create the scatter plot for Price vs Quantity Ordered with consistent colors and figure size
fig5, ax = plt.subplots(figsize=(8, 5))  # Adjusted figure size for consistency

# Set the background color for the plot area
fig5.patch.set_facecolor('#012a4a')  # Plot area color (dark blue)

# Plot the scatter plot with light teal color for markers
ax.scatter(cleaned_data_filtered['Price Each'], cleaned_data_filtered['Quantity Ordered'], alpha=0.5, color='#affc41')  # Marker color

# Set the title and axis labels with white font color
ax.set_title('Price vs Quantity Ordered', fontdict={'fontsize': 14, 'weight': 'bold', 'color': 'white'})
ax.set_xlabel('Price Each', fontsize=12, color='white')
ax.set_ylabel('Quantity Ordered', fontsize=12, color='white')

# Add grid lines and set the axis background color
ax.grid(True)
ax.set_facecolor('#012a4a')  # Axis area background color

# Set the tick parameters to white
ax.tick_params(colors='white')


# Calculate and display the correlation coefficient in Streamlit
correlation_coefficient_filtered = cleaned_data_filtered[['Price Each', 'Quantity Ordered']].corr().iloc[0, 1]
st.write(f"**Correlation coefficient between Price and Quantity Ordered:** {correlation_coefficient_filtered:.2f}")


# Create tabs for each analysis plot
# Create the layout with two columns
col1, col2 = st.columns(2)

# First plot (Monthly Sales) in the first column
with col1:
    st.write("### Monthly Sales")
    st.pyplot(fig1)  # Display Monthly Sales plot

# Second plot (Total Sales per City) in the second column
with col2:
    st.write("### Total Sales per City")
    st.pyplot(fig2)  # Display Total Sales per City plot

# Another pair of columns for the next two plots
col3, col4 = st.columns(2)

# Swap: Display Price vs Quantity Ordered in the third column
with col3:
    st.write("### Price vs Quantity Ordered")
    st.pyplot(fig5)  # Display Price vs Quantity Ordered plot in col3

# Fourth plot (Sales by Product) in the fourth column
with col4:
    st.write("### Sales by Product")
    st.pyplot(fig4)  # Display Sales by Product plot

# Swap: Display Number of Orders by Hour below the columns
st.write("### Number of Orders by Hour")
st.pyplot(fig3)  # Display Number of Orders by Hour below the columns

# Display the correlation coefficient below the Price vs Quantity Ordered scatter plot
st.write(f"**Correlation coefficient between Price and Quantity Ordered:** {correlation_coefficient_filtered:.2f}")

# Display the table for the Top 10 Most Common Product Pairs
st.write("### Top 10 Most Common Product Pairs")
st.table(pair_data)  # Display the table
