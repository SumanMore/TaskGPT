import os
import openai
from promptflow import tool
from dotenv import load_dotenv

load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("azure_openai_endpoint")
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("azure_openai_key")
deployment_id = "Suman"  

@tool
def chat_openai(contextMsg: str ,quesMsg: str) -> str :
# Make an API call to generate tex
    print(contextMsg)
    print(quesMsg)
    response = openai.ChatCompletion.create(
        engine = deployment_id,
        messages=[ {  
                "role": "system",
                "content": """You are a helpful assistant.Output the answer in a tabular format.Do not give the answer in a tuple format and list format.Be very careful and accurate while answering queries related to startdates, enddates, dates between ranges and so on.
                
                Refer to these examples to understand better:
                Example starts here:
                ###########################################
                user: ["('Upskill on python', 'ToDo', datetime.date(2023, 10, 3), datetime.date(2023, 10, 15))", "('upskill on streamlit', 'ToDo', datetime.date(2023, 10, 3), datetime.date(2023, 10, 25))", "('abc', 'In Progress', datetime.date(2023, 10, 3), datetime.date(2023, 11, 15))", "('test', 'Completed', datetime.date(2023, 10, 3), datetime.date(2023, 11, 29))"]
                user: give me the list of task whose end date is in october
                assistant: Here is the list of tasks whose end date is in October:

                | Task Name | Status | Start Date | End Date |
                | --- | --- | --- | --- |
                | Upskill on python | ToDo | 2023-10-03 | 2023-10-15 |
                | upskill on streamlit | ToDo | 2023-10-03 | 2023-10-25 |
                ###########################################

                user: ["('Upskill on python', 'ToDo', datetime.date(2023, 10, 3), datetime.date(2023, 10, 15))", "('upskill on streamlit', 'ToDo', datetime.date(2023, 10, 3), datetime.date(2023, 10, 25))", "('abc', 'In Progress', datetime.date(2023, 10, 3), datetime.date(2023, 11, 15))", "('test', 'Completed', datetime.date(2023, 10, 3), datetime.date(2023, 11, 29))"]
                user: give me all tasks that ends after 16th october and before 16th november
                assistant: Here is the list of tasks that end after 16th October and before 16th November:
                | Task Name | Status | Start Date | End Date |
                | --- | --- | --- | --- |
                | upskill on streamlit | ToDo | 2023-10-03 | 2023-10-25 |
                | abc | In Progress | 2023-10-03 | 2023-11-15 |
                ###########################################
                Example ends here
                """
            },
            {
                "role": "user",
                "content": contextMsg

            },
            {
            "role": "user",
            "content": quesMsg

            },
        ],
        temperature = 0,
    )
    return response

