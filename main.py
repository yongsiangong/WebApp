import pandas as pd
import streamlit as st
import plotly.express as px

st.title("WebApp Project")

# Upload file
st.subheader("File upload")
st.write("Upload your csv file for analysis.")
file_path = st.file_uploader("Upload csv file")

if file_path:
    # Checking file file is in csv format
    if file_path.name.split('.')[-1] != "csv":
        st.write("Please upload csv file")
    else:
        # Read the csv file
        df = pd.read_csv(file_path)

        # Expected columns and file types
        expected_dtypes = {
            'Date': 'object',
            'Category': 'object',
            'Amount': 'float64'
        }

        # Variable to control the display of the visual
        display = True


        for col_name, expected_dtype in expected_dtypes.items():
            # Check if the column names are correct
            if col_name not in df.columns:
                st.write(f"'{col_name}' not found as header in the uploaded csv file.")
                display = False
            else:
                # Check if the dtype of the file is correct
                if df.dtypes[col_name] != expected_dtype:
                    st.write(f"Data type for column '{col_name}' does not match. Expected {expected_dtype}, got {df.dtypes[col_name]}")
                    display = False

        # Display visual if the columns and dytpe checks passed
        if display:
            # Create Month and Year columns
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
            df['Month'] = df['Date'].dt.strftime('%B')
            df['Year'] = df['Date'].dt.strftime('%Y')

            # Bar chart
            st.subheader("Distribution of Amount Spent")
            st.write("Select the month and year below to see the distribution of expenses for the selected time period.")

            # Setting up select box for the barchart
            col1, col2 = st.columns(2)
            with col1:
                month_selected = st.selectbox("Select Month", df['Month'].unique())
            with col2:
                year_selected = st.selectbox("Select Year", df['Year'].unique())

            # Filter and display the barchart
            df_filtered = df[(df['Month'] == month_selected) & (df['Year'] == year_selected)]
            st.plotly_chart(px.bar(df_filtered, x = 'Category', y ='Amount', color = 'Category', title = f"Amount Spent on Each Category in {month_selected} {year_selected}"))

            # Line graph
            st.subheader("Trend of Amount Spent")
            st.write("Select the year and category below to see the distribution of expenses for the selected time period and category.")
            # Setting up selectbox for the line graph
            line_graph_col1, line_graph_col2 = st.columns(2)
            with line_graph_col1:
                year_selected_line = st.selectbox("Select Year for Line Graph", df['Year'].unique())
            with line_graph_col2:
                category_selected_line = st.selectbox("Select Category for Line Graph", ["All"] + list(df['Category'].unique()))
                if category_selected_line == "All":
                    category_selected_line = df['Category'].unique()
                else:
                    category_selected_line = [category_selected_line]

            # Filter and display the line chart
            df_filtered_line = df[(df["Year"] == year_selected_line) & (df["Category"].isin(category_selected_line))]
            time_series = df_filtered_line.groupby(["Month", "Category"], as_index= False)['Amount'].sum()
            st.plotly_chart(px.line(time_series, x = "Month", y = 'Amount', color = "Category", title = f"Line Graph for Expenses in {year_selected_line}"))