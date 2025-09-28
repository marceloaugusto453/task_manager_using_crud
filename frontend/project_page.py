import streamlit as st
import requests


API_URL = "http://backend:8000/api" 


def project_management_section():
    st.header("👤 Project Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Create", "📋 List project", "✍️ Update", "🗑️ Delete"])

    with tab1:
        st.subheader("Create project")
        with st.form("create_project_form", clear_on_submit=True):
            new_project_name = st.text_input("Project Name", key="create_project_name")
            new_project_description = st.text_input("Description", key="create_project_description")
            submitted = st.form_submit_button("Create project")
            
            if submitted:
                response = requests.post(
                    f"{API_URL}/project/",
                    json={"project_name": new_project_name, "project_description": new_project_description}
                )
                
                if response.status_code == 200:
                    st.success("Sucess! You created a new project")
                elif response.status_code == 400:
                    st.error(f"Error: {response.json().get('detail')}")
                else:
                    st.error(f"Unknown error ({response.status_code}): {response.json()}")

    with tab2:
        st.subheader("List all projects")
        
        @st.cache_data(ttl=5)
        def get_all_projects():
            try:
                response = requests.get(f"{API_URL}/project/")
                if response.status_code == 200:
                    return response.json()
                else:
                    st.error(f"Error loading projects: {response.status_code}")
                    return []
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ Connection error")
                return []

        projects_data = get_all_projects()
        
        if projects_data:
            st.dataframe(projects_data, use_container_width=True)
        else:
            st.info("No registered user or connection error")


    with tab3:
        st.subheader("Update Existing Project")
        
        latest_users = get_all_projects() 
        project_map = {f"{u['project_id']} - {u['project_name']} ({u['project_description']})": u['project_id'] for u in latest_users}
        
        selected_project_label = st.selectbox("Select project to Update", list(project_map.keys()))
        
        if selected_project_label:
            project_id_to_update = project_map[selected_project_label]
            
            current_project = next((u for u in latest_users if u['project_id'] == project_id_to_update), None)

            if current_project:
                with st.form("update_project_form", clear_on_submit=False):
                    st.write(f"Updating Project ID: **{project_id_to_update}**")
                    
                    upd_project_name = st.text_input("New project name", value=current_project.get('project_name', ''), key="update_project_name")
                    upd_project_description = st.text_input("New project description", value=current_project.get('project_description', ''), key="update_project_description")
                    
                    update_submitted = st.form_submit_button("Atualizar Usuário")
                    
                    if update_submitted:
                        update_data = {
                            "project_name": upd_project_name, 
                            "project_description": upd_project_description
                        }
                        
                        response = requests.put(
                            f"{API_URL}/project/{project_id_to_update}",
                            json=update_data
                        )
                        
                        if response.status_code == 200:
                            st.success("Project updated successfully!")
                            st.cache_data.clear() 
                        elif response.status_code == 404:
                            st.error("Project not found.")
                        elif response.status_code == 400:
                            st.error(f"Validation error: {response.json().get('detail')}")
                        else:
                            st.error(f"Error loading: {response.json()}")


    with tab4:
        st.subheader("Delete project")
        
        latest_projects = get_all_projects() 
        delete_projects_map = {f"{u['project_id']} - {u['project_name']}": u['project_id'] for u in latest_users}
        
        selected_delete_label = st.selectbox("Select Project to Delete", list(delete_projects_map.keys()))
        
        if selected_delete_label:
            project_id_to_delete = delete_projects_map[selected_delete_label]
            st.warning(f"Confirm deletion of project ID: **{project_id_to_delete}**")
            
            if st.button("Confirm Deletion"):
                response = requests.delete(f"{API_URL}/project/{project_id_to_delete}")
                
                if response.status_code == 200:
                    st.success("Project deleted!")
                    st.cache_data.clear()
                elif response.status_code == 404:
                    st.error("Project not found.")
                else:
                    st.error(f"Error deleting the project: {response.json()}")
