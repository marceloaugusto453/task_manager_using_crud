import streamlit as st
import requests

# URL base do seu backend FastAPI
API_URL = "http://backend:8000/api" 


def user_management_section():
    st.header("👤 User Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Create", "📋 List user", "✍️ Update", "🗑️ Delete"])

    # --- ABA 1: Create ---
    with tab1:
        st.subheader("Create new user")
        with st.form("create_user_form", clear_on_submit=True):
            new_name = st.text_input("Name", key="create_name")
            new_email = st.text_input("Email", key="create_email")
            new_area = st.text_input("Area", key="create_area")
            submitted = st.form_submit_button("Create user")
            
            if submitted:
                response = requests.post(
                    f"{API_URL}/user/",
                    json={"name": new_name, "email": new_email, "area": new_area}
                )
                
                if response.status_code == 200:
                    st.success("Sucess! You created a new user")
                elif response.status_code == 400:
                    st.error(f"Error: {response.json().get('detail')}")
                else:
                    st.error(f"Unknown error ({response.status_code}): {response.json()}")

    # --- ABA 2: LISTAR (Read - All) ---
    with tab2:
        st.subheader("List all users")
            
        if st.button("🔄 Refresh", key="refresh_users"):
            st.cache_data.clear()
            st.rerun() 
        
        @st.cache_data(ttl=5)
        def get_all_users():
            try:
                response = requests.get(f"{API_URL}/user/")
                if response.status_code == 200:
                    return response.json()
                else:
                    st.error(f"Error loading users: {response.status_code}")
                    return []
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ Connection error")
                return []

        users_data = get_all_users()
        
        if users_data:
            st.dataframe(users_data, use_container_width=True)
        else:
            st.info("No registered user or connection error")


    # --- ABA 3: ATUALIZAR (Update) ---
    with tab3:
        st.subheader("Update Existing User")
        
        latest_users = get_all_users() 
        user_map = {f"{u['user_id']} - {u['name']} ({u['email']})": u['user_id'] for u in latest_users}
        
        selected_user_label = st.selectbox("Select user to Update", list(user_map.keys()))
        
        if selected_user_label:
            user_id_to_update = user_map[selected_user_label]
            
            current_user = next((u for u in latest_users if u['user_id'] == user_id_to_update), None)

            if current_user:
                with st.form("update_user_form", clear_on_submit=False):
                    st.write(f"Updating User ID: **{user_id_to_update}**")
                    
                    upd_name = st.text_input("New name", value=current_user.get('name', ''), key="update_name")
                    upd_email = st.text_input("New email", value=current_user.get('email', ''), key="update_email")
                    upd_area = st.text_input("New area", value=current_user.get('area', ''), key="update_area")
                    
                    update_submitted = st.form_submit_button("Atualizar Usuário")
                    
                    if update_submitted:
                        update_data = {
                            "name": upd_name, 
                            "email": upd_email, 
                            "area": upd_area
                        }
                        
                        response = requests.put(
                            f"{API_URL}/user/{user_id_to_update}",
                            json=update_data
                        )
                        
                        if response.status_code == 200:
                            st.success("User updated successfully!")
                            st.cache_data.clear() # Limpa o cache para forçar a atualização da lista
                        elif response.status_code == 404:
                            st.error("User not found.")
                        elif response.status_code == 400:
                            st.error(f"Validation error: {response.json().get('detail')}")
                        else:
                            st.error(f"Error loading: {response.json()}")


    # --- ABA 4: DELETAR (Delete) ---
    with tab4:
        st.subheader("Delete user")
        
        latest_users = get_all_users() 
        delete_user_map = {f"{u['user_id']} - {u['name']}": u['user_id'] for u in latest_users}
        

        selected_delete_label = st.selectbox("Select User to Delete", list(delete_user_map.keys()))
        
        if selected_delete_label:
            user_id_to_delete = delete_user_map[selected_delete_label]
            st.warning(f"Confirm deletion of user ID: **{user_id_to_delete}**")
            
            if st.button("Confirm Deletion"):
                response = requests.delete(f"{API_URL}/user/{user_id_to_delete}")
                
                if response.status_code == 200:
                    st.success("User deleted successfully!")
                    st.cache_data.clear() # Limpa o cache
                elif response.status_code == 404:
                    st.error("User not found!")
                else:
                    st.error(f"Error deleting: {response.json()}")
