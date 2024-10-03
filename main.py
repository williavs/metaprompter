import os
import uuid
import json
from typing import Optional, Annotated, TypedDict
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import base64
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolInvocation

# Load environment variables
load_dotenv()



# Initialize ChatAnthropic
llm = ChatAnthropic(
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-5-sonnet-20240620",
    temperature=0.7
)

# Define the meta-prompt template
meta_prompt_template = '''
You are an AI assistant embedded in an IDE. Please help me generate a comprehensive prompt to build my application by following these steps:

1. **List Required Parameters:**

   - First, present the following required parameters enclosed in curly brackets:

     - {{project description}}
     - {{key features}}
     - {{technical requirements}}

2. **Wait for User Input:**

   - Allow me to provide the values for each parameter.

3. **Ask Clarifying Questions:**

   - After I provide the parameters, ask me 2-3 clarifying questions to better understand my requirements.

4. **Wait for User Responses:**

   - Wait for me to answer your questions.

5. **Generate Comprehensive Prompt:**

   - Using all the information gathered, create a comprehensive prompt that I can use to instruct the AI in the IDE to build my application. Ensure that all necessary components are included, and use advanced delimiting for clarity.

<requirements>
<frontend>
Framework: React 3.0.1
Language: TypeScript
Routing: React Router
State Management: Context API or Redux
Styling: CSS Modules or Styled Components
Testing: Jest and React Testing Library
Linting and Formatting: ESLint and Prettier
</frontend>

<backend>
Language: Python 3.x
Framework: Flask
ORM: SQLAlchemy
Serialization: Marshmallow
Testing: Pytest
Linting and Formatting: Flake8 and Black
</backend>

<database>
Type: PostgreSQL
Integration: Use SQLAlchemy for ORM in the backend
</database>

<containerization>
Docker: Write Dockerfile for both frontend and backend
Docker Compose: Create docker-compose.yml to orchestrate services
</containerization>

<infrastructure>
Terraform: Write scripts to provision resources on Linode
Local Development: Use LocalStack to simulate cloud services if needed
</infrastructure>

<environment_management>
Environment Variables: Use .env files managed by dotenv
Secrets Management: Assume the use of git-crypt for handling secrets
</environment_management>

<makefile>
Include a Makefile with the following targets:
- install: Install all dependencies
- build: Build the application
- start: Run the application locally
- test: Run all tests
- deploy: Deploy the application
- help: Display available make commands
</makefile>

<additional_requirements>
- CI/CD Pipeline: Provide configuration for a CI/CD pipeline using GitHub Actions or Jenkins
- Documentation: Generate API documentation using Swagger/OpenAPI
- Logging and Error Handling: Implement comprehensive logging and error handling mechanisms
- Code Quality: Set up linters and formatters for consistent code style
- Testing: Include unit and integration tests for both frontend and backend
- Sample Data: Provide seed scripts or sample data for testing purposes
- Version Control: Initialize Git repositories with appropriate .gitignore files
</additional_requirements>
</requirements>

<advanced_delimiting>
Section Separation: Use triple dashes --- to clearly separate major sections
Subsections: Use headings (##, ###, etc.) for subsections
Code Blocks: Include code blocks with syntax highlighting for folder structures and sample code
</advanced_delimiting>

<formatting>
Emphasis: Use bold and italic text to highlight important information
Lists: Utilize bullet points and numbered lists for clarity
</formatting>

<folder_structure>
<frontend>
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── index.tsx
│   └── App.tsx
├── public/
│   └── index.html
├── package.json
├── tsconfig.json
├── webpack.config.js
├── .eslintrc.js
└── .prettierrc
</frontend>

<backend>
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── utils/
├── tests/
├── config.py
├── requirements.txt
└── wsgi.py
</backend>
</folder_structure>

<assumptions>
- Default Settings: Where specific details are not provided, reasonable defaults are assumed
- Technologies: The latest stable versions of all technologies are to be used
- Permissions: Appropriate file permissions and security measures are implemented
</assumptions>

<summary>
By following these instructions, you will create a comprehensive prompt that effectively guides the AI in the IDE to build a complete full-stack web application. The prompt includes advanced delimiting for clarity and encompasses all critical components, ensuring a robust and production-ready application.
</summary>

<next_steps>
Use this structured approach to draft your comprehensive prompt. Make sure to:
1. Review each section for completeness
2. Customize any parts specific to your application's needs
3. Maintain clear and consistent formatting throughout the prompt
4. Instruct the AI the create a Makefile, dockerfile, docker-compose.yml, and Terraform scripts to provision the resources on Linode, and any other specifications needed to get users project up and running.
</next_steps>

'''

# Define the prompt template
chain = ChatPromptTemplate.from_messages([
    ("system", meta_prompt_template),
    ("human", "{input}")
]) | llm

# Define the State class
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define tools
@tool
def generate_prompt(parameters: str, clarifying_answers: str) -> str:
    """Generate a comprehensive prompt based on user parameters and clarifying answers."""
    final_input = parameters + "\n\n" + clarifying_answers
    return chain.invoke({"input": final_input})

tools = [generate_prompt]

# Initialize ToolExecutor
tool_executor = ToolExecutor(tools)

# Bind tools to the model
llm = llm.bind_tools(tools)

# Update the call_model function
def call_model(state):
    messages = state["messages"]
    if not isinstance(messages, list):
        messages = [messages]
    
    # Extract the content from HumanMessage objects
    human_messages = [msg.content for msg in messages if isinstance(msg, HumanMessage)]
    
    # Join all human messages into a single string
    input_text = "\n\n".join(human_messages)
    
    # Use the chain with the meta-prompt template
    response = chain.invoke({"input": input_text})
    
    return {"messages": [AIMessage(content=response.content)]}

# Define graph functions
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return "end"
    return "continue"

def call_tool(state):
    messages = state["messages"]
    last_message = messages[-1]
    tool_call = last_message.tool_calls[0]
    action = ToolInvocation(
        tool=tool_call.function.name,
        tool_input=json.loads(tool_call.function.arguments),
    )
    response = tool_executor.invoke(action)
    tool_message = ToolMessage(
        content=str(response),
        tool_call_id=tool_call.id,
        name=action.tool,
    )
    return {"messages": [tool_message]}

# Define the graph
workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)
workflow.add_edge("action", "agent")

# Compile the graph without checkpointing
app = workflow.compile()

# Helper functions
def generate_verification_message(message: AIMessage) -> AIMessage:
    serialized_tool_calls = json.dumps(message.tool_calls, indent=2)
    return AIMessage(
        content=(
            "I plan to invoke the following tools, do you approve?\n\n"
            "Type 'y' if you do, anything else to stop.\n\n"
            f"{serialized_tool_calls}"
        ),
        id=message.id,
    )

def stream_app_catch_tool_calls(inputs, thread) -> Optional[AIMessage]:
    tool_call_message = None
    for event in app.stream(inputs, thread):
        if "value" in event and "messages" in event["value"]:
            message = event["value"]["messages"][-1]
            if isinstance(message, AIMessage) and message.tool_calls:
                tool_call_message = message
            else:
                st.write(message.content)
    return tool_call_message

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href

def generate_prompt_page():
    st.markdown("""
    <style>
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
        padding: 1.5rem;
        margin-bottom: 2rem;
        height: 100%;
    }
    .description-card {
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        # Description card on the left
        st.markdown("""
        <div class="card description-card">
            <p>Welcome to <strong>CodePromptPro</strong>! Please fill in the fields on the right to generate a comprehensive prompt for your application. This prompt can then be used to instruct the AI in your IDE to build your application.</p>
            <div class="step-indicator">
                <div class="step {0}">1</div>
                <div class="step {1}">2</div>
                <div class="step {2}">3</div>
            </div>
        </div>
        """.format(
            'active' if st.session_state.get('step', 1) == 1 else '',
            'active' if st.session_state.get('step', 1) == 2 else '',
            'active' if st.session_state.get('step', 1) == 3 else ''
        ), unsafe_allow_html=True)

    with col2:
        # Initialize session state
        if "step" not in st.session_state:
            st.session_state.step = 1
        if "user_parameters" not in st.session_state:
            st.session_state.user_parameters = ""
        if "clarifying_questions" not in st.session_state:
            st.session_state.clarifying_questions = ""
        if "user_answers" not in st.session_state:
            st.session_state.user_answers = ""
        if "final_prompt" not in st.session_state:
            st.session_state.final_prompt = ""

        # Wrap all steps in a single card


        # Step 1: Collect parameters
        if st.session_state.step == 1:
            st.subheader("Step 1: Provide Application Parameters")

            with st.form(key="parameters_form"):
              
                project_description = st.text_area('Project Description', placeholder='Describe the main goal and purpose of your application.')
                key_features = st.text_area('Key Features', placeholder='List the main features and functionalities of your application.')
                technical_requirements = st.text_area('Technical Requirements', placeholder='Specify any technical requirements, APIs, or integrations needed.')
                submit_parameters = st.form_submit_button("Submit Parameters")
                st.markdown('</div>', unsafe_allow_html=True)

            if submit_parameters:
                st.session_state.user_parameters = f'''
                {{project description}}: {project_description}

                {{key features}}: {key_features}

                {{technical requirements}}: {technical_requirements}
                '''
                st.session_state.step = 2
                st.rerun()

        # Step 2: AI asks clarifying questions
        elif st.session_state.step == 2:
            st.subheader("Step 2: Clarifying Questions")
            
            if not st.session_state.clarifying_questions:
                with st.spinner("Generating clarifying questions..."):
                    response = call_model({"messages": [HumanMessage(content=st.session_state.user_parameters)]})
                    ai_message = response["messages"][0]
                    st.session_state.clarifying_questions = ai_message.content

            st.markdown(st.session_state.clarifying_questions)

            with st.form(key="answers_form"):
                user_answers = st.text_area('Your Answers to Clarifying Questions', placeholder='Please answer the AI\'s questions here.')
                submit_answers = st.form_submit_button('Submit Answers')

            if submit_answers:
                st.session_state.user_answers = user_answers
                st.session_state.step = 3
                st.rerun()

        # Step 3: AI generates the comprehensive prompt
        elif st.session_state.step == 3:
            st.subheader("Step 3: Generated Comprehensive Prompt")
            
            if not st.session_state.final_prompt:
                with st.spinner("Generating the comprehensive prompt..."):
                    combined_input = f"""
                    User Parameters:
                    {st.session_state.user_parameters}

                    Clarifying Questions and Answers:
                    {st.session_state.clarifying_questions}

                    User Answers:
                    {st.session_state.user_answers}
                    """
                    response = call_model({"messages": [HumanMessage(content=combined_input)]})
                    ai_message = response["messages"][0]
                    st.session_state.final_prompt = ai_message.content

            st.markdown(st.session_state.final_prompt)

            # Create a markdown file with the final prompt
            with open("final_prompt.md", "w") as f:
                f.write(st.session_state.final_prompt)

            # Add a download button for the markdown file
            st.markdown(get_binary_file_downloader_html("final_prompt.md", "final_prompt.md"), unsafe_allow_html=True)

            if st.button("Start Over"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        # Close the card div
        st.markdown('</div>', unsafe_allow_html=True)