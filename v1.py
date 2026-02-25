import streamlit as st
import pandas as pd
import plotly.express as px
from injesting_data import DataIngest

# Set page layout to wide to fit charts side-by-side
st.set_page_config(page_title="HPC Log Visualizer", layout="wide")

def main():
    st.title("HPC Log Visualizations")
    st.markdown("Direct visual insights from the processed log data.")

    # 1. Load and Transform Data using your class
    ingest = DataIngest()
    try:
        df_raw = pd.read_csv(ingest.csv_path)
        df = ingest.transform_data(df_raw)

        # --- Row 1: Key Metrics ---
        # Quick summary counters at the top
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Logs", len(df))
        m2.metric("Nodes Active", df['node'].nunique())
        m3.metric("Components", df['component'].nunique())
        m4.metric("Avg Events/Day", int(df.set_index('timestamp').resample('D').size().mean()))

        st.divider()

        # --- Row 2: Main Charts ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top 10 Nodes by Activity")
            # Create a bar chart for nodes
            node_data = df['node'].value_counts().head(10).reset_index()
            node_data.columns = ['Node ID', 'Log Count']
            fig_node = px.bar(node_data, x='Node ID', y='Log Count', 
                             color='Log Count', color_continuous_scale='Viridis')
            st.plotly_chart(fig_node, use_container_width=True)
            

        with col2:
            st.subheader("System State Distribution")
            # Create a pie chart for states
            state_data = df['state'].value_counts().reset_index()
            state_data.columns = ['Status', 'Count']
            fig_state = px.pie(state_data, names='Status', values='Count', 
                              hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_state, use_container_width=True)
            

        st.divider()

        # --- Row 3: Timeline ---
        st.subheader("Log Frequency Over Time")
        # Group data by day to see trends
        timeline = df.set_index('timestamp').resample('D').size().reset_index()
        timeline.columns = ['Date', 'Event Count']
        fig_line = px.line(timeline, x='Date', y='Event Count', 
                          title="Daily Event Volume", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        


    except Exception as e:
        st.error(f"Error generating visualizations: {e}")

if __name__ == "__main__":
    main()