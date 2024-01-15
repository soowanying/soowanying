import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import queries 

# TASK 1: establish connection to MySQL
# You code starts here
conn = mysql.connector.connect(
    host='localhost',
    user='root', # put your username here
    password='', # put your password here
    database='bikestore'
)

# Use this function to get scalar values from MySQL
# To use the function, pass in the query variable and connection object.
def getOne_query(query,conn):
    if query != '':
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return list(result)[0]
    else:
        return '--'

# Use this function to get dataframe from MySQL for ploting OR display of lists
# To use the function, pass in the query variable and connection object.
def getMany_query(query, conn):
    if query != '':
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=cursor.column_names)
        cursor.close()
    else:
        result = pd.DataFrame()
    return result

st. set_page_config(layout="wide")

st.title('Bikestore Data Exploration')
tab_overview, tab_customers, tab_staff, tab_items, tab_orders = st.tabs(['Overview','Customers Dashboard','Staff Dashboard','Item Dashboard','Orders Dashboard'])

# ---------------------------------------------- Tab 1 ----------------------------------------------

with tab_overview:
    st.header('Overview')
    col11, col12, col13, col14 = st.columns(4)
    with col11:
        st.metric('Total Customers',getOne_query(queries.queryT1, conn))
    with col12:
        st.metric('Total Products', getOne_query(queries.queryT2, conn))
    with col13:
        st.metric('Total Stores', getOne_query(queries.queryT3, conn))
    with col14:
        st.metric('Total Orders', getOne_query(queries.queryT4, conn))

    col21, col22 = st.columns(2)
    with col21:
        st.subheader('Total Orders by Year')
        df = getMany_query(queries.queryT5, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='no_of_orders', x='year', height=500)

    with col22:
        st.subheader('Distribution of Orders by Store')
        df = getMany_query(queries.queryT6, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='no_of_orders', x='store', height=500)

# ---------------------------------------------- Tab 2 ----------------------------------------------

with tab_customers:
    st.header('Customer Dashboard')
    # your code starts here
    col11, col12 = st.columns(2)
    with col11:
        st.metric('Total Customers', getOne_query(queries.queryT23, conn))
    
    with col12:
        st.metric('Total Orders', getOne_query(queries.queryT4, conn))
        
    col21, col22 = st.columns(2)
    with col21:
        st.subheader('Type of Customers', divider='violet')
        df = getMany_query(queries.queryT27, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='no_of_customers', x='status', height=500, color = '#7F00FF')
    
    with col22:
        st.subheader('Top 10 customers that spend the most', divider='violet')
        df = getMany_query(queries.queryT24, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.table(df)

        
    col31, col32 = st.columns(2)
    with col31:
        st.subheader('List of Recurring Customers', divider='violet')
        with st.expander('See whole table'):
            
            df2 = getMany_query(queries.queryT26, conn)
            if df2.empty:
                st.write('No data, please insert query in queries.py')
            else:
                st.table(df2)
    with col32:
        st.subheader('Products and Their Price Category', divider='violet')
        with st.expander('See whole table'):
            
            df3 = getMany_query(queries.queryT25, conn)
            if df3.empty:
                st.write('No data, please insert query in queries.py')
            else:
                st.table(df3)

# ---------------------------------------------- Tab 3 ----------------------------------------------

with tab_staff:
   st.header('Staff Dashboard')

   col11, col12, col13 = st.columns(3)
   with col11:
    st.metric('Total Customers', getOne_query(queries.queryT1, conn))
   with col12:
    st.metric('Total Stores', getOne_query(queries.queryT3, conn))
   with col13:
    st.metric('Total Staffs', getOne_query(queries.queryT8, conn))


   col21, col22 = st.columns(2)
   with col21:
    st.subheader('Total Staffs Available in Each Store')
    df = getMany_query(queries.queryS1, conn)
    if df.empty:
            st.write('No data, please insert query in queries.py')
    else:
            st.bar_chart(df, y='no_of_staffs', x='store', height=500)

   with col22:
    st.subheader('Ratio Between Customer vs Staff')
    df = getMany_query(queries.queryS2, conn)
    if df.empty:
            st.write('No data, please insert query in queries.py')
    else:
            df['ratio'] = df['ratio'].astype(float)
            st.bar_chart(df, y='ratio', x='store', height=500)

   st.header('Ratio of Customer with Staff by Year')
   df = getMany_query(queries.queryS5, conn)
   if df.empty:
            st.write('No data, please insert query in queries.py')
   else:
            df['ratio'] = df['ratio'].astype(float)
            df = getMany_query(queries.queryS5, conn).astype({"ratio":"float"}).pivot(index = 'order_year', columns = 'store', values = 'ratio')
            st.line_chart(df)

   st.header('Staff Performance Based on Sales')
   df = getMany_query(queries.queryS3, conn)
   if df.empty:
        st.write('No data, please insert query in queries.py')
   else:
        col31, col32 = st.columns(2)
        with col31:
            st.subheader('Sales Data Table')
            st.table(df)
        with col32:
            df_chart = df.copy()
            df_chart['total_sales'] = pd.to_numeric(df_chart['total_sales'], errors='coerce')

            st.subheader('Sales Chart')
            st.bar_chart(df_chart.set_index('staff_id'), height=500)

   st.header('Average Sales per Transaction')
   df = getMany_query(queries.queryS4, conn)
   if df.empty:
        st.write('No data, please insert query in queries.py')
   else:
        col31, col32 = st.columns(2)
        with col31:
            st.subheader('Average Sales Data Table')
            st.table(df)

        with col32:
            df_chart = df.copy()
            df_chart['avg_sales_per_transaction'] = pd.to_numeric(df_chart['avg_sales_per_transaction'], errors='coerce')

            st.subheader('Average Sales Chart')
            st.bar_chart(df_chart.set_index('staff_id'), height=500)

# ---------------------------------------------- Tab 4 ----------------------------------------------

with tab_items:
    st.header('Item Dashboard')
    # your code starts here
    col11, col12= st.columns(2)
    with col11:
        st.metric('Total Products',getOne_query(queries.queryI7, conn))
    with col12:
        st.metric('Total Brand', getOne_query(queries.queryI8, conn))

    col21, col22 = st.columns(2)
    with col21:
        st.subheader('Brands Available')
        df2 = getMany_query(queries.queryI10, conn)
        st.table(df2)
    with col22:
        st.subheader('Total Products by Brands')
        df1 = getMany_query(queries.queryI9, conn)
        if df1.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df1, y='total_product', x='brand_name', height=500)

    col31, col32= st.columns(2)
    with col31:
        st.metric('Brand that has most sales',getOne_query(queries.queryI11, conn))
    with col32:
        st.metric('Number of sales', getOne_query(queries.queryI11b, conn))

    col41, col42= st.columns(2)
    with col41:
        st.metric('Product that has most sales',getOne_query(queries.queryI12, conn))
    with col42:
        st.metric('Number of sales', getOne_query(queries.queryI12b, conn))

    col51, col52 =st.columns(2)
    with col51:
        with st.expander('See whole table'):
            st.subheader('Products and Their Price Category')
            df3 = getMany_query(queries.queryI13, conn)
            if df3.empty:
                st.write('No data, please insert query in queries.py')
            else:
                st.table(df3)
    with col52:
        with st.expander('See whole table'):
            st.subheader('Sales by Price Category of Items')
            df4 = getMany_query(queries.queryI14, conn)
            if df4.empty:
                st.write('No data, please insert query in queries.py')
            else:
                st.table(df4)

    col61, col62, col63= st.columns(3)
    with col61:
        st.subheader('Top 5 Highest Sales of Low-Priced Items')
        df5 = getMany_query(queries.queryI15, conn)
        st.table(df5)
    with col62:
        st.subheader('Top 5 Highest Sales of Medium-Priced Items')
        df6 = getMany_query(queries.queryI16, conn)
        st.table(df6)
    with col63:
        st.subheader('Top 5 Highest Sales of High-Priced Items')
        df7 = getMany_query(queries.queryI17, conn)
        st.table(df7)


# ---------------------------------------------- Tab 5 ----------------------------------------------

with tab_orders:
    st.header('Orders Dashboard')
    # your code starts here
    cols11, cols12, cols13 = st.columns(3)
    with cols11:
        st.metric('Total Orders', getOne_query(queries.queryT4, conn))
    with cols12:
        st.metric('Total Sales', str( int( getOne_query(queries.queryT28, conn) ) // 1000 ) + " K" )
    with cols13:
        df = getMany_query(queries.queryT21, conn)
        st.metric("Highest Sales Product", df["product_name"][0])

    col21, col22 = st.columns(2)
    with col21:
        st.subheader('Total Orders by Year', divider='blue')
        df = getMany_query(queries.queryT5, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='no_of_orders', x='year', height=500)

    with col22:
        st.subheader('Total Sales by Year', divider='violet')
        df = getMany_query(queries.queryT29, conn)
        df["total_sales"] = df["total_sales"].astype("float")
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='total_sales', x='order_year', height=500, color = '#BC4EC2')
    
    col31 = st.columns(1)
    # with col31:
    st.subheader('Top 10 Products by Sales', divider='red')
    df = getMany_query(queries.queryT20, conn)
    df["total_sales"] = df["total_sales"].astype("float")
    if df.empty:
        st.write('No data, please insert query in queries.py')
    else:
        st.line_chart(df.head(10), y='total_sales', x='product_name', height=500, color='#FFC1EE')
        show_more = st.button('Show More Rows')
        if show_more:
            st.table(df[10:])

    col41 = st.columns(1)
    st.subheader('Total Orders by Month', divider='green')
    df = getMany_query(queries.queryT22, conn)
    if df.empty:
        st.write('No data, please insert query in queries.py')
    else:
        st.bar_chart(df, y='no_of_orders', x='month', height=500, color='year')
