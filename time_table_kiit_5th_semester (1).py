# -*- coding: utf-8 -*-
"""TIME_TABLE_KIIT_5TH_SEMESTER.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AaaesoPDM5TciD4zZeN5_6D2MWNHierQ
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load the section, professional elective, and core section files from GitHub
section_url = 'https://raw.githubusercontent.com/satyam26en/TIME_TABLE_KIIT/main/SECTION.csv'
elective_url = 'https://raw.githubusercontent.com/satyam26en/TIME_TABLE_KIIT/main/Elective_TIME_TABLE.csv'
core_url = 'https://raw.githubusercontent.com/satyam26en/TIME_TABLE_KIIT/main/core%20-%20Sheet1.csv'

section_df = pd.read_csv(section_url)
elective_df = pd.read_csv(elective_url)
core_df = pd.read_csv(core_url)

# Normalize the 'Roll No.' column to ensure there are no leading/trailing spaces and consistent data type
section_df['Roll No.'] = section_df['Roll No.'].astype(str).str.strip()

# Define the order of days and times in 12-hour format
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
times = ['8-9 AM', '9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM', '1-2 PM', '2-3 PM', '3-4 PM', '4-5 PM']

# Function to take roll number input and create the timetable DataFrame
def create_timetable_df(roll_number):
    # Find the section details for the given roll number
    student_section = section_df[section_df['Roll No.'] == roll_number]

    if student_section.empty:
        st.error("Roll number not found.")
        return pd.DataFrame(columns=days, index=times)

    # Extract the core section and elective sections
    core_section = student_section['Core Section'].values[0]
    elective_1_section = student_section['Professional Elective 1'].values[0]
    elective_2_section = student_section['Professional Elective 2'].values[0]

    # Retrieve the weekly timetable for Professional Electives 1 and 2
    elective_1_timetable = elective_df[elective_df['Section(DE)'] == elective_1_section]
    elective_2_timetable = elective_df[elective_df['Section(DE)'] == elective_2_section]
    core_timetable = core_df[core_df['Section'] == core_section]

    # Define the order of days and a mapping from abbreviated to full day names
    day_mapping = {
        'MON': 'Monday',
        'TUE': 'Tuesday',
        'WED': 'Wednesday',
        'THU': 'Thursday',
        'FRI': 'Friday',
        'SAT': 'Saturday'
    }

    # Convert time to 12-hour format
    time_mapping = {
        '8 TO 9': '8-9 AM',
        '9 TO 10': '9-10 AM',
        '10 TO 11': '10-11 AM',
        '11 TO 12': '11-12 PM',
        '12 TO 1': '12-1 PM',
        '1 TO 2': '1-2 PM',
        '2 TO 3': '2-3 PM',
        '3 TO 4': '3-4 PM',
        '4 TO 5': '4-5 PM'
    }

    # Initialize the combined timetable dictionary
    combined_timetable_dict = {day: {time: "" for time in times} for day in days}

    # Helper function to update the timetable dictionary
    def update_timetable(timetable_df, timetable_dict):
        room_columns = [col for col in timetable_df.columns if 'ROOM' in col]
        for index, row in timetable_df.iterrows():
            for col in room_columns:
                if row[col] != '---' and row[col] != 'x':
                    day = day_mapping.get(row['DAY'], 'Unknown')
                    time_col = timetable_df.columns[timetable_df.columns.get_loc(col) + 1]
                    time_slot = time_mapping.get(time_col, time_col)
                    subject = row[time_col]
                    room_number = row[col]
                    if subject.lower() != 'x':
                        timetable_dict[day][time_slot] = f"{subject} ({room_number})"
        return timetable_dict

    # Update the combined timetable with core, elective 1, and elective 2 timetables
    combined_timetable_dict = update_timetable(core_timetable, combined_timetable_dict)
    combined_timetable_dict = update_timetable(elective_1_timetable, combined_timetable_dict)
    combined_timetable_dict = update_timetable(elective_2_timetable, combined_timetable_dict)

    # Create a DataFrame from the combined timetable dictionary
    combined_timetable_df = pd.DataFrame(combined_timetable_dict)

    return combined_timetable_df

# Streamlit app
st.title('Timetable Maestro')
roll_number = st.text_input("Enter Roll Number:")

if roll_number:
    timetable_df = create_timetable_df(roll_number)

    # Remove empty rows
    timetable_df = timetable_df.replace("", "x")

    # Display the combined timetable DataFrame
    st.write("\nCombined Timetable DataFrame:")
    st.dataframe(timetable_df)

    # Function to plot the timetable
    def plot_timetable(timetable_df):
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Time'] + list(timetable_df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[timetable_df.index] + [timetable_df[col] for col in timetable_df.columns],
                       fill_color='lavender',
                       align='left'))
        ])

        fig.update_layout(title_text='Timetable')
        fig.show()

    # Plot the timetable DataFrame
    plot_timetable(timetable_df)