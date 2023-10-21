import streamlit as st
import pandas as pd
import json
from database import create_task, insert_task, get_all_data, get_all_defined_task, update_task, delete_task, get_task_data, get_status
from chat import chat_openai

#Display the task data from the database
def display_table(table_empty):
    data = get_all_data()
    column_names = ["Task", "Status", "Start Date", "End Date"]
    data = [(task, status, pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()) for task, status, start_date, end_date in data]
    table_empty.dataframe(pd.DataFrame(data, columns=column_names), hide_index=True)

# Main function
def main():
    # st.markdown("<h1 style='text-align:center;'>ToDo</h1>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .css-cio0dv.ea3mdgi1
    {
        visibility:hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar option
    option = st.sidebar.radio("Choose operation:", options=("Create", "Update", "Delete", "Display","Chat"))

    if option == "Create":
        create_task()
        with st.form("Create", clear_on_submit=True):
            defined_task = st.text_area("Define Task")
            status = st.selectbox("Status", options=("ToDo", "In Progress", "Completed"))
            startdate, enddate = st.columns(2)
            start_date = startdate.date_input("Start Date")
            end_date = enddate.date_input("End Date")
            submit_btn = st.form_submit_button("Add")
            if submit_btn and defined_task != "":
                insert_task(defined_task, status, start_date, end_date)
                st.success(f"{defined_task} task is added successfully")

    elif option == "Display":
        table_empty = st.empty()
        display_table(table_empty)

    elif option == "Update":
        table_empty = st.empty()
        display_table(table_empty)
        defined_task = st.selectbox("Please choose the task you want to update",options=get_all_defined_task())
        Status_options = ["ToDo", "Completed", "In Progress"]

        if defined_task:
            with st.form("Update",clear_on_submit=True):
                st.text_area("Task",defined_task)
                result = get_task_data(defined_task)
                if result:
                    status = st.selectbox("Status",options=("ToDo","Completed","In Progress"),index=Status_options.index(get_status(defined_task)))
                    startdate,enddate = st.columns(2)
                    start_date = startdate.date_input("Start Date",result[0][1])
                    end_date = enddate.date_input("End Date",result[0][2])
                    submit_btn = st.form_submit_button("Update")
                    if  submit_btn:
                        update_task(defined_task,status,start_date,end_date)
                        st.success(f"{defined_task} task is updated successfully")
            display_table(table_empty)

                        
    elif option == "Delete":
        table_empty = st.empty()
        display_table(table_empty)
        with st.form("Delete",clear_on_submit=True):
            defined_task = st.selectbox("Please choose the task you want to delete",options=get_all_defined_task())    
            submit_btn = st.form_submit_button("Delete")
            if submit_btn:
                delete_task(defined_task)
                st.success(f"{defined_task} task is deleted successfully")

        display_table(table_empty)

    elif option == "Chat":
        question=st.text_area("Ask a question")
        btn=st.button("Submit")
        if btn:
            data=get_all_data()
            data_json = json.dumps(data, default=str) 
            generated_text = chat_openai(data_json, question )
            print(generated_text['choices'][0]['message']['content'])
            st.write(generated_text['choices'][0]['message']['content'])    
            
if __name__ == "__main__":
    main()
