import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64


def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'


def main():
    # Load seaborn theme.
    sns.set_theme(style='darkgrid')

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

    report_text = st.text_input('Report Text')

    export_as_pdf = st.button('Export Report')

    if export_as_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, report_text)

        html = create_download_link(pdf.output(dest='S').encode('latin-1'), 'test')

        st.markdown(html, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
