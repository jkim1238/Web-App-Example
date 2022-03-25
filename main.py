import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    # Load seaborn theme.
    sns.set_theme(style="darkgrid")

    # Read online JSON API and store into pandas DataFrame.
    df = pd.read_json('https://opendata.maryland.gov/resource/2tuk-rcgi.json')

    # Title for streamlit page.
    # <title>Interactive K-Means Clustering</title>
    st.title('Home Performance Energy Efficiency Projects in Maryland')

    # Description.
    st.write('Through grants and loans, the Maryland Energy Administration has contributed to the growth of energy '
             'efficiency industries, and has helped reduce statewide energy consumption:')

    # Create sidebar.
    sidebar = st.sidebar

    # Add checkbox to sidebar.
    df_display = sidebar.checkbox('Display Raw Data', value=True)

    # Display DataFrame to streamlit page.
    if df_display:
        st.write(df)

    # Count frequency of county.
    df = df.groupby('county').count().reset_index()

    # Drop all columns and keep 'county' and 'program' columns.
    df = df[['county', 'program']]

    # Rename column.
    df = df.rename(columns={'program': 'frequency'})

    # Add checkbox to sidebar.
    freq_display = sidebar.checkbox('Display Frequency Data', value=True)

    if freq_display:
        st.write(df)

    # Create box plot.
    # Create the figure size.
    fig = plt.figure(figsize=(10, 4))

    # Create the count plot.
    sns.barplot(x='frequency', y='county', orient='h', data=df)

    # Display figure on page.
    st.write(fig)


    print(df)


if __name__ == '__main__':
    main()
