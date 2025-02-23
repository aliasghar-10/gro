import streamlit as st
import pandas as pd
from io import BytesIO
import random

def apply_theme():
    dark_mode = st.sidebar.checkbox("Enable Dark Mode", value=False)
    if dark_mode:
        st.markdown(
            """
            <style>
            body {
                background-color: #0e1117;
                color: #c9d1d9;
            }
            .stButton>button {
                background-color: #21262d;
                color: #c9d1d9;
                border: 1px solid #30363d;
            }
            .stButton>button:hover {
                background-color: #30363d;
            }
            .stTextInput>div>input {
                background-color: #0e1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
            }
            .stTextArea>div>textarea {
                background-color: #0e1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
            }
            .stSelectbox>div>div>div {
                background-color: #0e1117;
                color: #c9d1d9;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    return dark_mode

def main():
    st.set_page_config(page_title="Growth Mindset App", layout="centered")
    dark_mode = apply_theme()

    st.title("🌱 Growth Mindset App")
    st.write("Welcome! This app helps you develop and embrace a growth mindset through goal tracking, data visualization, and daily reflections.")

    with st.sidebar:
        st.header("App Navigation")
        st.info("Navigate through the app sections from here.")

    st.header("🎯 Set and Track Your Goals")
    goal = st.text_input("What is your growth mindset goal?")
    if st.button("Save Goal"):
        if goal:
            st.session_state['goal'] = goal
            st.success("Your goal has been saved!")
        else:
            st.warning("Please enter a goal before saving.")

    if 'goal' in st.session_state:
        st.write(f"**Your Current Goal:** {st.session_state['goal']}")

    st.header("📂 Upload and Visualize Data")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)
            st.session_state['data'] = data
            st.success("File uploaded successfully!")
            st.write("### Uploaded Data")
            st.dataframe(data)

            numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
            if not numeric_columns.empty:
                st.write("### Data Visualization")
                x_axis = st.selectbox("Select X-axis", numeric_columns, key="x_axis")
                y_axis = st.selectbox("Select Y-axis", numeric_columns, key="y_axis")
                if x_axis and y_axis:
                    st.line_chart(data[[x_axis, y_axis]])
            else:
                st.warning("No numeric columns found for visualization.")
        except Exception as e:
            st.error(f"Error processing file: {e}")

    st.header("📝 Daily Reflections")
    reflection = st.text_area("What did you learn today?")
    if st.button("Save Reflection"):
        if reflection:
            if 'reflections' not in st.session_state:
                st.session_state['reflections'] = []
            st.session_state['reflections'].append(reflection)
            st.success("Reflection saved!")
        else:
            st.warning("Please write something to save.")
    if 'reflections' in st.session_state:
        st.write("### Your Reflections:")
        for i, ref in enumerate(st.session_state['reflections'], 1):
            st.write(f"{i}. {ref}")

    st.header("🏷️ Tag Management")
    tag_input = st.text_input("Add a Tag")
    if st.button("Add Tag"):
        if tag_input:
            if 'tags' not in st.session_state:
                st.session_state['tags'] = []
            st.session_state['tags'].append(tag_input)
            st.success(f"Tag '{tag_input}' added!")
        else:
            st.warning("Please enter a tag to add.")
    if 'tags' in st.session_state:
        st.write("### Current Tags:")
        for tag in st.session_state['tags']:
            col1, col2 = st.columns([4, 1])
            col1.write(tag)
            if col2.button("Remove", key=tag):
                st.session_state['tags'].remove(tag)
                st.experimental_rerun()

    st.header("🔄 File Converter")
    uploaded_conversion_file = st.file_uploader("Upload a file to convert", type=["csv", "xlsx"])
    if uploaded_conversion_file:
        try:
            if uploaded_conversion_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_conversion_file)
                output = BytesIO()
                data.to_excel(output, index=False, engine='openpyxl')
                st.download_button(
                    label="Download Excel File",
                    data=output.getvalue(),
                    file_name="converted_file.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                data = pd.read_excel(uploaded_conversion_file)
                output = BytesIO()
                data.to_csv(output, index=False)
                st.download_button(
                    label="Download CSV File",
                    data=output.getvalue(),
                    file_name="converted_file.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"Error converting file: {e}")

    st.header("💡 Inspiration")
    quotes = [
        "Believe you can and you're halfway there.",
        "Challenges are what make life interesting.",
        "Every day is a chance to get better.",
        "Growth is painful. Change is painful. But nothing is as painful as staying stuck.",
        "Success is the sum of small efforts repeated daily."
    ]
    st.write(random.choice(quotes))

if __name__ == "__main__":
    main()
