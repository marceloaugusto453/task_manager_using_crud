import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import altair as alt      

API_BASE = "http://backend:8000/api"

def dashboard_management_section():
    st.title("📊 Dashboard - Task Manager")
    
    # --- Puxa dados da API (Mantido) ---
    @st.cache_data(ttl=600) # Mantive o cache de 10 minutos
    def load_data():
        try:
            # Requisitando todas as tarefas para a análise
            tasks_response = requests.get(f"{API_BASE}/task/")
            users_response = requests.get(f"{API_BASE}/user/")
            projects_response = requests.get(f"{API_BASE}/project/")
            
            # Garante que todas as requisições foram bem-sucedidas
            tasks_response.raise_for_status() 
            users_response.raise_for_status() 
            projects_response.raise_for_status()
            
            return users_response.json(), projects_response.json(), tasks_response.json()
        except Exception as e:
            st.error(f"Error loading API data: Check the backend. Details: {e}")
            return [], [], []

    users, projects, tasks = load_data()

    # Cria DataFrames
    df_users = pd.DataFrame(users)
    df_tasks = pd.DataFrame(tasks)
    
    if df_tasks.empty:
        st.warning("No tasks found. Unable to generate dashboard. 🚨")
        st.stop()

    df = df_tasks.copy()
    df = df.merge(df_users, left_on="user_id", right_on="user_id", suffixes=("", "_user")) 
    
    
    df_projects = pd.DataFrame(projects).rename(columns={'project_name': 'project_name_full'}) 
    df = df.merge(df_projects, left_on="project_id", right_on="project_id", suffixes=("", "_project"))

    st.sidebar.subheader("Filtros")

    user_options = ["All"] + sorted(df["name"].unique().tolist())
    project_options = ["All"] + sorted(df["project_name_full"].unique().tolist())

    selected_user = st.sidebar.selectbox("User", user_options)
    selected_project = st.sidebar.selectbox("Project", project_options)

    filtered_df = df.copy()
    if selected_user != "All":
        filtered_df = filtered_df[filtered_df["name"] == selected_user]
    if selected_project != "All":
        filtered_df = filtered_df[filtered_df["project_name_full"] == selected_project]

    if filtered_df.empty:
        st.warning("No tasks found with selected filters.")
    

    st.subheader("📌 Overview")
    col1, col2, col3 = st.columns(3)
    
    total_tarefas = len(filtered_df)
    perc_concluidas = (filtered_df['status'].eq('Finished').mean() * 100) if total_tarefas > 0 else 0
    usuario_top = filtered_df["name"].mode()[0] if not filtered_df.empty else "—"

    col1.metric("Total Tasks", total_tarefas, delta_color="off")
    col2.metric("% Finished", f"{perc_concluidas:.1f}%", delta_color="off")
    col3.metric("Top User", usuario_top, delta_color="off")

    st.markdown("---")

    col_pie, col_bar = st.columns([1, 2]) 

    with col_pie:
        st.markdown("#### 🎯 Tasks by Status")
        
        status_counts = filtered_df["status"].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig_pie = px.pie(
            status_counts, 
            values='Count', 
            names='Status', 
            title='Percentage by Status',
            hole=0.3,
            height=350
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(showlegend=False)

        st.plotly_chart(fig_pie, use_container_width=True)


    with col_bar:
        st.markdown("#### 👤 Tasks by User and Status")
        
        fig_bar = px.histogram(
            filtered_df, 
            x="name", 
            color="status", 
            title="Task Distribution by User",
            barmode='group', # Barras agrupadas
            height=350,
            labels={'name': 'User', 'status': 'Status'}
        )
        
        fig_bar.update_layout(xaxis={'categoryorder':'total descending'}) 
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")