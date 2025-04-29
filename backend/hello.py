import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objs as go

# --- Background with 3D effect ---
def add_animated_background():
    st.markdown(
        """
        <style>
        @keyframes gradientAnimation {
          0% {background-position: 0% 50%;}
          50% {background-position: 100% 50%;}
          100% {background-position: 0% 50%;}
        }
        .stApp {
            background: linear-gradient(-45deg, #FF6F61, #6F86D6, #FF6F61, #6F86D6);
            background-size: 400% 400%;
            animation: gradientAnimation 20s ease infinite;
            color: white;
            font-family: 'Arial Rounded MT Bold', sans-serif;
            backdrop-filter: blur(10px);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .stTitle, .stText {
            text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }
        .stButton {
            background-color: #6F86D6;
            border: none;
            padding: 12px 20px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        .stButton:hover {
            background-color: #FF6F61;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Data Cleaning ---
def clean_data(df):
    df_cleaned = df.copy()
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].str.strip()
    df_cleaned = df_cleaned.drop_duplicates()
    for col in df_cleaned.select_dtypes(include=['float64', 'int64']).columns:
        df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        if df_cleaned[col].mode().size > 0:
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
    return df_cleaned

# --- Main App ---
def main():
    add_animated_background()

    st.title("🚀 AI-Powered Business Analytics Dashboard....!")
    st.write("Upload your dataset ➡️ Clean ➡️ Visualize ➡️ Predict ➡️ Download!")

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            df_cleaned = clean_data(df)

            # --- Data View Section with Buttons ---
            st.subheader("📄 View Data")
            col1, col2 = st.columns(2)

            if col1.button("📄 Show Original Data"):
                st.success("Showing Original Uploaded Data 📄")
                st.dataframe(df)

            if col2.button("🧹 Show Cleaned Data"):
                st.success("Showing Cleaned Data After Processing 🧹")
                st.dataframe(df_cleaned)

            # --- Visualization Section ---
            st.subheader("📊 Create Visualization (on Cleaned Data)")
            all_columns = df_cleaned.columns.tolist()
            numeric_columns = df_cleaned.select_dtypes(include=['float64', 'int64']).columns.tolist()

            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Pie Chart"])

            if chart_type == "Bar Chart":
                x_column = st.selectbox("Select X-axis", all_columns)
                y_column = st.selectbox("Select Y-axis", numeric_columns)

                fig = px.bar(df_cleaned, x=x_column, y=y_column, title=f"Bar Chart of {y_column} vs {x_column}")
                st.plotly_chart(fig)

            elif chart_type == "Line Chart":
                x_column = st.selectbox("Select X-axis", all_columns)
                y_columns = st.multiselect("Select Y-axis columns", numeric_columns)

                if y_columns:
                    fig = go.Figure()
                    for y_col in y_columns:
                        fig.add_trace(go.Scatter(x=df_cleaned[x_column], y=df_cleaned[y_col], mode='lines+markers', name=y_col))
                    fig.update_layout(title=f"Line Chart of {', '.join(y_columns)} vs {x_column}")
                    st.plotly_chart(fig)

            elif chart_type == "Scatter Plot":
                x_column = st.selectbox("Select X-axis", numeric_columns)
                y_column = st.selectbox("Select Y-axis", numeric_columns)
                hue_column = st.selectbox("Select Hue (optional)", ["None"] + all_columns)

                if hue_column != "None":
                    fig = px.scatter(df_cleaned, x=x_column, y=y_column, color=df_cleaned[hue_column], title=f"Scatter Plot")
                else:
                    fig = px.scatter(df_cleaned, x=x_column, y=y_column, title=f"Scatter Plot")
                st.plotly_chart(fig)

            elif chart_type == "Histogram":
                selected_column = st.selectbox("Select column for Histogram", numeric_columns)
                fig = px.histogram(df_cleaned, x=selected_column, title=f"Histogram of {selected_column}")
                st.plotly_chart(fig)

            elif chart_type == "Pie Chart":
                label_column = st.selectbox("Select label column for Pie Chart", all_columns)
                value_column = st.selectbox("Select value column for Pie Chart", numeric_columns)

                fig = px.pie(df_cleaned, names=label_column, values=value_column, title=f"Pie Chart of {label_column}")
                st.plotly_chart(fig)

            # --- Prediction Section ---
            st.subheader("🔮 Predict Future Based on Numeric Columns")
            st.info("Select X (input) and Y (target) numeric columns to build prediction model!")

            input_column = st.selectbox("Select Independent (Input) Column (X)", numeric_columns)
            target_column = st.selectbox("Select Target (Output) Column (Y)", numeric_columns)

            prediction_mode = st.selectbox("Prediction Type:", ["Single Value Prediction", "Date Wise Prediction"])

            if prediction_mode == "Single Value Prediction":
                future_input = st.number_input(f"Enter Future Value for {input_column} to Predict {target_column}", format="%.6f")

                if st.button("Predict"):
                    X = df_cleaned[[input_column]].values
                    y = df_cleaned[target_column].values
                    model = LinearRegression()
                    model.fit(X, y)

                    predicted_value = model.predict(np.array([[future_input]]))

                    st.success(f"🚀 Predicted {target_column} when {input_column} = {future_input}: {predicted_value[0]:.2f}")

                    # Plot prediction
                    fig2 = px.scatter(df_cleaned, x=input_column, y=target_column, title="Prediction Result")
                    fig2.add_trace(go.Scatter(x=[future_input], y=[predicted_value[0]], mode='markers', marker=dict(color='red', size=12), name='Future Prediction'))
                    st.plotly_chart(fig2)

            elif prediction_mode == "Date Wise Prediction":
                date_unit = st.selectbox("Predict for:", ["Days", "Months", "Years"])
                periods = st.number_input(f"How many {date_unit} to predict?", min_value=1, step=1)

                if st.button("Predict Future Dates"):
                    X = np.arange(len(df_cleaned)).reshape(-1, 1)
                    y = df_cleaned[target_column].values

                    model = LinearRegression()
                    model.fit(X, y)

                    future_indexes = np.arange(len(df_cleaned), len(df_cleaned) + int(periods)).reshape(-1, 1)
                    future_predictions = model.predict(future_indexes)

                    # Display prediction
                    future_dates = []
                    if date_unit == "Days":
                        future_dates = pd.date_range(start=pd.Timestamp.today(), periods=periods).date
                    elif date_unit == "Months":
                        future_dates = pd.date_range(start=pd.Timestamp.today(), periods=periods, freq='M').date
                    elif date_unit == "Years":
                        future_dates = pd.date_range(start=pd.Timestamp.today(), periods=periods, freq='Y').date

                    prediction_df = pd.DataFrame({
                        'Date': future_dates,
                        'Predicted ' + target_column: future_predictions
                    })

                    st.subheader("📅 Future Predictions")
                    st.write(prediction_df)

                    # Plot future predictions
                    fig3 = px.line(prediction_df, x='Date', y='Predicted ' + target_column, title=f"Future {target_column} Predictions over {periods} {date_unit}")
                    st.plotly_chart(fig3)

            # --- Download Section ---
            st.subheader("💾 Download Cleaned Data & Predictions")
            if st.button("Download Cleaned Data as CSV"):
                csv = df_cleaned.to_csv(index=False)
                st.download_button(label="Download Cleaned Data", data=csv, file_name="cleaned_data.csv", mime="text/csv")

            if prediction_mode == "Date Wise Prediction" and 'prediction_df' in locals():
                csv_pred = prediction_df.to_csv(index=False)
                st.download_button(label="Download Future Predictions", data=csv_pred, file_name="future_predictions.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Error processing the file: {e}")
    else:
        st.info("Please upload a CSV or Excel file to get started!")

if __name__ == "__main__":
    main()