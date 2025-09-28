import streamlit as st
import requests
from datetime import datetime, date, time
import pandas as pd # Adicionado para melhor manipulação de dados

# Configuração da URL da API (Ajuste o prefixo conforme seu backend)
API_URL = "http://backend:8000/api" 

# --- Funções de Ajuda ---

@st.cache_data(ttl=5)
def get_reference_data(endpoint):
    """Fetches reference data (users or projects) from FastAPI."""
    try:
        response = requests.get(f"{API_URL}/{endpoint}/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.ConnectionError:
        return []

def format_datetime_for_api(selected_date: date, selected_time: time):
    """Combines date and time inputs into a timezone-aware ISO 8601 string."""
    combined_dt = datetime.combine(selected_date, selected_time)
    return combined_dt.isoformat() + 'Z'


# --- Função Principal da Página ---

def task_management_section():
    st.header("📋 Task Management")
    
    # Busca dados de referência (Chaves Estrangeiras)
    users = get_reference_data('user')
    projects = get_reference_data('project')
    
    # Mapeamento de Opções (CRÍTICO: Usamos 'project_name' conforme seu schema)
    user_options = {f"{u['user_id']} - {u['name']}": u['user_id'] for u in users}
    project_options = {f"{p['project_id']} - {p['project_name']}": p['project_id'] for p in projects}
    
    # STATUS_CHOICES alinhado com o StatusBase do seu schema
    STATUS_CHOICES = ["To-do", "Doing", "Finished"]
    
    # --- Abas CRUD ---
    tab1, tab2, tab3, tab4 = st.tabs(["➕ CREATE", "👀 KANBAN/LIST", "✍️ UPDATE", "🗑️ DELETE"])

    # --- TAB 1: CREATE ---
    with tab1:
        st.subheader("Add New Task")
        if not user_options or not project_options:
            st.warning("⚠️ Please create at least one **User** and one **Project** before creating tasks.")
        else:
            with st.form("create_task_form", clear_on_submit=True):
                # Campos de Input
                new_title = st.text_input("Task Name (task_name)")
                new_description = st.text_area("Description (task_description)")
                new_status = st.selectbox("Initial Status", STATUS_CHOICES)
                
                new_deadline_date = st.date_input("Deadline Date", value=date.today(), key="create_date")
                new_deadline_time = st.time_input("Deadline Time", value=time(23, 59), key="create_time")
                
                selected_user = st.selectbox("Responsible", list(user_options.keys()), key="task_user_select")
                selected_project = st.selectbox("Project", list(project_options.keys()), key="task_project_select")

                submitted = st.form_submit_button("Create Task")
                
                if submitted:
                    deadline_iso = format_datetime_for_api(new_deadline_date, new_deadline_time)
                    user_id = user_options[selected_user]
                    project_id = project_options[selected_project]
                    
                    response = requests.post(
                        f"{API_URL}/task/",
                        json={
                            # CRÍTICO: Chaves alinhadas com o schema TaskCreate
                            "task_name": new_title, 
                            "task_description": new_description, 
                            "status": new_status,
                            "deadline": deadline_iso, 
                            "project_id": project_id,
                            "user_id": user_id
                        }
                    )
                    
                    if response.status_code == 200:
                        st.success("Task created successfully!")
                        st.cache_data.clear() # Limpa o cache após sucesso
                    elif response.status_code == 400:
                        st.error(f"Validation Error: {response.json().get('detail')}")
                    else:
                        st.error(f"Error creating task: {response.json()}")


    # --- ABA 2: KANBAN / LIST (Read) ---
    with tab2:
        st.subheader("Kanban View")
        
        # Botão de atualização manual
        if st.button("🔄 Refresh Task List", key="refresh_tasks"):
            st.cache_data.clear()
            st.rerun() 
            
        @st.cache_data(ttl=2) 
        def get_all_tasks():
            try:
                response = requests.get(f"{API_URL}/task/")
                return response.json() if response.status_code == 200 else []
            except requests.exceptions.ConnectionError:
                return []

        tasks_data = get_all_tasks()
        
        if tasks_data:
            # Kanban implementation with columns
            cols = st.columns(len(STATUS_CHOICES))
            
            for i, status in enumerate(STATUS_CHOICES):
                with cols[i]:
                    st.markdown(f"**{status} ({len([t for t in tasks_data if t['status'] == status])})**")
                    st.divider()
                    
                    for task in [t for t in tasks_data if t['status'] == status]:
                        deadline_str = task.get('deadline', 'N/A')
                        try:
                            # Tenta parsear para mostrar em formato mais amigável
                            friendly_deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")
                        except ValueError:
                            friendly_deadline = deadline_str
                        
                        # CRÍTICO: Usa as chaves corretas para exibição
                        st.info(f"**#{task['task_id']} - {task['task_name']}**") 
                        st.caption(f"Responsible: {task['user_id']} | Project: {task['project_id']}")
                        st.error(f"Deadline: {friendly_deadline}")
                        st.write(task['task_description'][:50] + "...") # Chave corrigida
                        st.markdown("---")
        else:
            st.info("No tasks registered.")


    # --- TAB 3: UPDATE ---
    with tab3:
        st.subheader("Update Existing Task")
        
        latest_tasks = get_all_tasks()
        # CRÍTICO: Mapeia o nome de exibição para a chave correta
        task_map = {f"{t['task_id']} - {t['task_name']}": t['task_id'] for t in latest_tasks}
        
        selected_task_label = st.selectbox("Select Task to Update", list(task_map.keys()), key="update_task_select")
        
        if selected_task_label:
            task_id_to_update = task_map[selected_task_label]
            current_task = next((t for t in latest_tasks if t['task_id'] == task_id_to_update), None)

            if current_task:
                # CRÍTICO: Pre-populando Data e Hora do Deadline
                deadline_dt = datetime.fromisoformat(current_task.get('deadline', datetime.now().isoformat()).replace('Z', '+00:00'))
                current_date = deadline_dt.date()
                current_time = deadline_dt.time()
                
                with st.form("update_task_form", clear_on_submit=False):
                    # CRÍTICO: Chaves de valor e rótulos corrigidos
                    upd_title = st.text_input("Task Name", value=current_task.get('task_name', ''))
                    upd_description = st.text_area("Description", value=current_task.get('task_description', ''))
                    
                    upd_deadline_date = st.date_input("Deadline Date", value=current_date, key="update_date")
                    upd_deadline_time = st.time_input("Deadline Time", value=current_time, key="update_time")
                    
                    upd_status = st.selectbox("Status", STATUS_CHOICES, index=STATUS_CHOICES.index(current_task.get('status')), key="upd_status")
                    
                    # Lógica de preenchimento para Chaves Estrangeiras
                    default_user_key = f"{current_task.get('user_id')} - {next((u['name'] for u in users if u['user_id'] == current_task.get('user_id')), 'Unknown')}"
                    default_project_key = f"{current_task.get('project_id')} - {next((p['project_name'] for p in projects if p['project_id'] == current_task.get('project_id')), 'Unknown')}"
                    
                    upd_user = st.selectbox("Responsible", list(user_options.keys()), index=list(user_options.keys()).index(default_user_key), key="upd_user")
                    upd_project = st.selectbox("Project", list(project_options.keys()), index=list(project_options.keys()).index(default_project_key), key="upd_project")

                    update_submitted = st.form_submit_button("Update Task")
                    
                    if update_submitted:
                        deadline_iso = format_datetime_for_api(upd_deadline_date, upd_deadline_time)

                        update_data = {
                            # CRÍTICO: Chaves alinhadas com o schema TaskUpdate
                            "task_name": upd_title, 
                            "task_description": upd_description, 
                            "status": upd_status,
                            "deadline": deadline_iso,
                            "user_id": user_options[upd_user],
                            "project_id": project_options[upd_project]
                        }
                        
                        response = requests.put(
                            f"{API_URL}/task/{task_id_to_update}",
                            json=update_data
                        )
                        
                        if response.status_code == 200:
                            st.success("Task updated successfully!")
                            st.cache_data.clear()
                        else:
                            st.error(f"Error updating task: {response.json()}")


    with tab4:
        st.subheader("Delete Task")
        
        # Garante que a lista de tarefas está fresca
        latest_tasks = get_all_tasks() 
        
        # Mapeamento para o Selectbox
        delete_task_map = {f"{t['task_id']} - {t['task_name']}": t['task_id'] for t in latest_tasks}
        
        selected_delete_label = st.selectbox("Select Task to Delete", list(delete_task_map.keys()), key="delete_task_select")
        
        if selected_delete_label:
            task_id_to_delete = delete_task_map[selected_delete_label]
            st.warning(f"Confirm deletion of Task ID: **{task_id_to_delete}**")
            
            if st.button("Confirm Deletion"):
                response = requests.delete(f"{API_URL}/task/{task_id_to_delete}")
                
                if response.status_code == 200:
                    try:
                        # Tenta ler o JSON para obter a mensagem personalizada
                        success_data = response.json()
                        deleted_id = success_data.get("deleted_id", task_id_to_delete)
                        message = success_data.get("message", f"Task ID {deleted_id} deleted successfully!")
                        
                        st.success(message)
                        st.cache_data.clear() 
                    except Exception:
                         # Fallback: Se o backend retornar 200, mas sem JSON (como se fosse um 204)
                         st.success(f"Task ID {task_id_to_delete} deleted successfully! (Backend did not return full JSON)")

                # TRATAMENTO DE ERRO 404 (Task not found)
                elif response.status_code == 404:
                    st.error("Task not found.")
                
                # TRATAMENTO DE OUTROS ERROS (400, 500)
                else:
                    # Tenta ler o JSON do erro (o que causa o JSONDecodeError se o corpo estiver vazio)
                    try:
                        error_detail = response.json().get('detail', f"Status {response.status_code}. No JSON detail found.")
                    except requests.exceptions.JSONDecodeError:
                        # Captura o erro se o corpo da resposta for vazio (e.g., 500 sem corpo)
                        error_detail = f"Server returned Status {response.status_code}, but the response body was empty or invalid."
                        
                    st.error(f"Error deleting task: {error_detail}")