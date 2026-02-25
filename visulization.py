import streamlit as st
import pandas as pd
import plotly.express as px  # Using Plotly for interactive charts
from injesting_data import DataIngest

# Set page config
st.set_page_config(page_title="HPC Log Analyzer", layout="wide")

def main():
    st.title(" HPC Log Analytics Dashboard")
    st.markdown("Analyze node performance and component states from structured logs.")

    # 1. Load and Transform Data
    ingest = DataIngest()
    
    try:
        df_raw = pd.read_csv(ingest.csv_path)
        df = ingest.transform_data(df_raw)
        
        # Sidebar Filters
        st.sidebar.header("Filters")
        selected_node = st.sidebar.multiselect("Select Node", options=df['node'].unique())
        selected_state = st.sidebar.multiselect("Select State", options=df['state'].unique())

        # Apply Filters
        filtered_df = df.copy()
        if selected_node:
            filtered_df = filtered_df[filtered_df['node'].isin(selected_node)]
        if selected_state:
            filtered_df = filtered_df[filtered_df['state'].isin(selected_state)]

        # --- Metric Row ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Logs", len(filtered_df))
        col2.metric("Unique Nodes", filtered_df['node'].nunique())
        col3.metric("Critical Events", len(filtered_df[filtered_df['state'].str.contains('unavailable', case=False)]))

        # --- Data Display Section ---
        st.subheader(" Log Data Preview")
        st.dataframe(filtered_df, use_container_width=True)

        # --- Visualizations Section ---
        st.divider()
        st.subheader("📈 Visual Analytics")
        
        viz_col1, viz_col2 = st.columns(2)

        with viz_col1:
            st.write("**Top Nodes by Frequency**")
            node_counts = filtered_df['node'].value_counts().head(10).reset_index()
            fig_node = px.bar(node_counts, x='node', y='count', color='count',
                             labels={'node': 'Node ID', 'count': 'Log Count'})
            st.plotly_chart(fig_node, use_container_width=True)

        with viz_col2:
            st.write("**Component State Distribution**")
            state_counts = filtered_df['state'].value_counts().reset_index()
            fig_state = px.pie(state_counts, names='state', values='count', hole=0.4)
            st.plotly_chart(fig_state, use_container_width=True)

        # --- Timeline Section ---
        st.write("**Event Timeline**")
        timeline_df = filtered_df.set_index('timestamp').resample('D').size().reset_index(name='event_count')
        fig_time = px.line(timeline_df, x='timestamp', y='event_count', title="Daily Event Frequency")
        st.plotly_chart(fig_time, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure 'HPC_2k.log_structured.csv' and 'injesting_data.py' are in the same folder.")

if __name__ == "__main__":
    main()