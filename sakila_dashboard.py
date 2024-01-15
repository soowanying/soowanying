import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import sakila_queries 

# TASK 1: establish connection to MySQL
# You code starts here
conn = mysql.connector.connect(
    host='localhost',
    user='root', # put your username here
    password='', # put your password here
    database='sakila'
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

st.title('Sakila Data Exploration')
tab_overview, tab_customers, tab_staff, tab_film, tab_payment = st.tabs(['Overview','Customers Dashboard','Staff Dashboard','Film Dashboard','Payment Dashboard'])

# ---------------------------------------------- Tab 1 ----------------------------------------------
with tab_overview:
    st.header('Overview')
    col11, col12, col13, col14 = st.columns(4)
    with col11:
        st.metric('Total Customers',getOne_query(sakila_queries.queryT1, conn))
    with col12:
        st.metric('Total Rental', getOne_query(sakila_queries.queryT2, conn))
    with col13:
        st.metric('Total Sales', str( float( getOne_query(sakila_queries.queryP2, conn)) ))
    with col14:
        st.metric('Total Films',getOne_query(sakila_queries.queryF1, conn))

    col21, col22= st.columns(2)
    with col21:
        st.subheader('Distribution of Category in Films')
        df1 = getMany_query(sakila_queries.queryF3, conn)
        if df1.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df1, y='film_num', x='name', height=500)
    with col22:
        st.subheader('Total Rentals by Month')
        df1 = getMany_query(sakila_queries.queryT6, conn)
        if df1.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df1, y='rental_count', x='rental_month', height=500)
    
    st.header('Busiest Hours for Movie Rentals')
    df = getMany_query(sakila_queries.queryT7, conn)
    if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
    else:
            st.line_chart(df, y='rental_count', x='rental_hour', height=500)

# ---------------------------------------------- Tab 2 ----------------------------------------------

with tab_customers:
    st.header('Customer Dashboard')
    # your code starts here
    col11, col12, col13, col14 = st.columns(4)
    with col11:
        st.metric('Total Customers', getOne_query(sakila_queries.queryT1, conn))
    with col12:
        st.metric('Total Rentals', getOne_query(sakila_queries.queryT2, conn))
    with col13:
        st.metric('Top Spender', getOne_query(sakila_queries.queryT4, conn))
    with col14:
        st.metric('Top Renter', getOne_query(sakila_queries.queryT5, conn))
    
    st.subheader('Top 10 Customers by Number of Rentals')
    df = getMany_query(sakila_queries.queryC1, conn)
    if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
    else:
            st.bar_chart(df, y='rental_count', x='full_name', height=500)

    st.subheader('Top 5 Country has the Most Number of Customers')
    df = getMany_query(sakila_queries.queryC2, conn)
    if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
    else:
            st.bar_chart(df, y='total_customers', x='country', height=500)

    st.subheader('Customers have Rented More Than 30 Films')
    df = getMany_query(sakila_queries.queryC3, conn)
    if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
    else:
            st.line_chart(df, y='rental_count', x='full_name', height=500)
    
    st.header('Total Amount Spent by Each Customer')
    df = getMany_query(sakila_queries.queryC5, conn)
    if df.empty:
        st.write('No data, please insert query in sakila_queries.py')
    else:
        col21, col22 = st.columns(2)
        with col21:
            st.table(df.head(10))

            show_more = st.button('Show More Rows')
            if show_more:
                st.table(df[10:])

        with col22:
            df_chart = df.copy()
            df_chart['total_amount_spent'] = pd.to_numeric(df_chart['total_amount_spent'], errors='coerce')

            st.bar_chart(df_chart.set_index('full_name'), height=500)

    st.subheader('Customer Genre Preferences')
    df = getMany_query(sakila_queries.queryC4, conn)
    if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
    else:
            st.table(df.head(10))
            show_more = st.checkbox('Show More Rows')
            if show_more:
                st.table(df[10:])

# ---------------------------------------------- Tab 2 ----------------------------------------------

with tab_staff:
    st.header('Staff Dashboard')
    # your code starts here
    
    col11, col12= st.columns(2)
    with col11:
        st.subheader('Staff Payment Summary')
        df = getMany_query(sakila_queries.queryQ1, conn)
        if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
        else:
            st.table(df)

    
    with col12:
        st.subheader('Total Rental By Staff')
        df = getMany_query(sakila_queries.queryQ5, conn)
        if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
        else:
            st.table(df)
    
    
    st.subheader('Top 10 Customer & Staff Interactions')
    df2 = getMany_query(sakila_queries.queryQ2, conn)
    if df.empty:
        st.write('No data, please insert query in sakila_queries.py')
    else:
        st.table(df2.head(10))

    col21, col22= st.columns(2)
    with col21:
        st.subheader('Number of Rentals by Staff')
        df3 = getMany_query(sakila_queries.queryQ4, conn)
        if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
        else:
            st.bar_chart(df3, y='Customer_Count', x='Staff_Name', height=500)
    
    with col22:
        st.subheader('Staff Performance with Films')
        df4 = getMany_query(sakila_queries.queryQ3, conn)
        if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
        else:
            st.table(df4)

# ---------------------------------------------- Tab 3 ----------------------------------------------

with tab_film:
    st.header('Film Dashboard')
    # your code starts here
    col11, col12, col13= st.columns(3)
    with col11:
        st.metric('Total Films',getOne_query(sakila_queries.queryF1, conn))
    with col12:
        st.metric('Total Actors', getOne_query(sakila_queries.queryF2, conn))
    with col13:
        st.metric('Language Medium', getOne_query(sakila_queries.queryF5, conn))

    col21, col22= st.columns(2)
    with col21:
        st.subheader('Distribution of Category in films')
        df1 = getMany_query(sakila_queries.queryF3, conn)
        if df1.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df1, y='film_num', x='name', height=500)
    with col22:
        st.subheader('Top 5 Category for Films')
        df2 = getMany_query(sakila_queries.queryF4, conn)
        if df2.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.table(df2)
    
    col31,col32, col33 = st.columns(3)
    with col31:
        st.subheader('Distribution of Rating in Films')
        df3 = getMany_query(sakila_queries.queryF6, conn)
        if df3.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df3, y='film_no', x='rating', height=500)
    with col32:
        st.subheader('Top 10 Actors Appeared in Films')
        df4 = getMany_query(sakila_queries.queryF7, conn)
        if df4.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.table(df4)
    with col33:
        st.subheader('Distribution of Rental Duration in Films')
        df5 = getMany_query(sakila_queries.queryF8, conn)
        if df5.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.area_chart(df5, y='film_num', x='rental_duration', height=500)
    
    col41, col42 = st.columns(2)
    with col41:
        st.subheader('Category by Length of Films')
        df6 = getMany_query(sakila_queries.queryF9, conn)
        if df6.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df6, y='total_film', x='length_category', height=500)
    with col42:
        st.subheader('Top 20 Longest Length of Films')
        df7 = getMany_query(sakila_queries.queryF10, conn)
        if df7.empty:
            st.write('No data, please insert query in queries.py')
        else:
          st.table(df7)


# ---------------------------------------------- Tab 4 ----------------------------------------------

with tab_payment:
    st.header('Payment Dashboard')
    # your code starts here

    col11 = st.columns(3)
    with col11[0]:
        st.metric('Total Sales', str( float( getOne_query(sakila_queries.queryP2, conn)) ))
    
    with col11[1]:
        df = getMany_query(sakila_queries.queryP3, conn)
        st.metric("Highest Sales Film", df["title"][0])

    with col11[2]:
        df = getMany_query(sakila_queries.queryP3, conn)
        df["total_sales"] = df["total_sales"].astype("float")
        st.metric("Highest Film Sales", df["total_sales"][0])

    col21 = st.columns(2)

    with col21[0]:
        st.subheader('Total Sales by Month', divider='blue')
        df = getMany_query(sakila_queries.queryP1, conn)
        df["total_sales"] = df["total_sales"].astype("float")
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df.head(10), y='total_sales', x='month', height=500, color='year')

    with col21[1]:
        st.subheader('Total Sales by Store', divider='red')
        df = getMany_query(sakila_queries.queryP4, conn)
        df["total_sales"] = df["total_sales"].astype("float")
        if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
        else:
            st.bar_chart(df, y='total_sales', x='store_id', height=500, color='#FFC1EE')

    
    st.subheader('Total Sales by Film', divider='violet')
    df = getMany_query(sakila_queries.queryP3, conn)
    if df.empty:
        st.write('No data, please insert query in sakila_queries.py')
    else:
        col31, col32 = st.columns(2)
        with col31:
            st.table(df.head(10))

            show_more = st.checkbox('Show More Films')
            if show_more:
                st.table(df[10:])
        
        with col32:
            df_chart = df.copy()
            df_chart['total_sales'] = pd.to_numeric(df_chart['total_sales'], errors='coerce')
            st.line_chart(df_chart.head(10).set_index('title'), height=500)

    col41 = st.columns(2)
    with col41[0]:
        st.subheader('Total Sales by Film Category', divider='green')
        df = getMany_query(sakila_queries.queryP5, conn)
        df["total_sales"] = df["total_sales"].astype("float")
        if df.empty:
            st.write('No data, please insert query in sakila_queries.py')
        else:
            st.bar_chart(df, y='total_sales', x='category', height=500, color='#ABF7B1')
    
    with col41[1]:
        st.subheader('Top 10 Rental Duration by Film', divider='orange')
        df = getMany_query(sakila_queries.queryP6, conn)
        st.table(df.head(10).set_index('title'))
