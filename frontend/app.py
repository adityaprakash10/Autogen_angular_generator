import streamlit as st
import requests
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import autogen
import sys


def rerun_app():
    st.session_state["rerun_counter"] = st.session_state.get("rerun_counter", 0) + 1
    raise Exception("Streamlit rerun")


def safe_rerun():
    try:
        rerun_app()
    except Exception as e:
        if str(e) != "Streamlit rerun":
            raise


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    project_root = Path(__file__).parent.parent
    load_dotenv(dotenv_path=project_root / ".env")
except Exception:
    load_dotenv()

from agents.requirements_agent import get_requirements_analyzer_agent
from agents.api_designer_agent import get_api_designer_agent
from agents.model_development_agent import get_model_developer_agent
from agents.business_logic_agent import get_business_logic_agent
from agents.integration_agent import get_integration_agent
from agents.db_migration_agent import get_db_migration_agent
from agents.component_designer_agent import get_component_designer_agent
from agents.service_development_agent import get_service_developer_agent
from agents.ui_implementation_agent import get_ui_implementation_agent
from agents.state_management_agent import get_state_management_agent
from agents.critic_agent import get_critic_agent


WORKFLOW_STEPS = [
    {"name": "API Designer", "agent_func": get_api_designer_agent, "output_file": "backend/api_routes.py"},
    {"name": "Model Developer", "agent_func": get_model_developer_agent, "output_file": "backend/models.py"},
    {"name": "Business Logic Developer", "agent_func": get_business_logic_agent, "output_file": "backend/business_logic.py"},
    {"name": "Integration Developer", "agent_func": get_integration_agent, "output_file": "backend/integrations.py"},
    {"name": "Database Migrator", "agent_func": get_db_migration_agent, "output_file": "backend/migration.py"},
    {"name": "Component Designer", "agent_func": get_component_designer_agent, "output_file": "frontend/component.ts"},
    {"name": "Service Developer", "agent_func": get_service_developer_agent, "output_file": "frontend/service.ts"},
    {"name": "UI Implementer", "agent_func": get_ui_implementation_agent, "output_file": "frontend/ui.html_scss"},
    {"name": "State Manager", "agent_func": get_state_management_agent, "output_file": "frontend/state.ts"},
]
MAX_RETRIES = 3


def initialize_state():
    defaults = {
        "initial_srd_text": "",
        "srd_generation_complete": False,
        "workflow_started": False,
        "current_step": 0,
        "generated_code": {},
        "current_code_to_review": "",
        "critic_feedback": "",
        "retry_count": 0,
        "current_agent": None,
        "agent_feedback_messages": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


initialize_state()


def run_async(async_func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(async_func(*args))


st.title("Task Tracker - Requirements and Code Generation Workflow")

# Phase 1: Requirements Upload and Review
if not st.session_state.srd_generation_complete:
    st.header("Phase 1: Upload and Review Requirements Document")

    uploaded_file = st.file_uploader(
        "Upload your requirements document (PDF, DOCX, or Markdown)",
        type=["pdf", "docx", "md"],
        disabled=bool(st.session_state.initial_srd_text),
    )

    if uploaded_file and not st.session_state.initial_srd_text:
        with st.spinner("Parsing requirements document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post("http://127.0.0.1:8000/upload/", files=files)
                response.raise_for_status()
                raw_text = response.json().get("raw_text", "")

                if not raw_text.strip():
                    st.warning("The uploaded file contains no extractable text.")
                else:
                    st.session_state.initial_srd_text = raw_text
            except Exception as e:
                st.error(f"Failed to upload and parse file: {e}")

    if st.session_state.initial_srd_text:
        st.markdown("### Extracted Requirements Document (Review Below)")
        st.text_area("Requirements Text", st.session_state.initial_srd_text, height=400)

        if st.button("Approve Requirements and Proceed to Code Generation"):
            st.session_state.srd_generation_complete = True
            safe_rerun()

# Phase 2: Multi-Agent Code Generation
else:
    st.header("Phase 2: Multi-Agent Code Generation (Stepwise Workflow)")

    with st.expander("View Approved Requirements Document", expanded=False):
        st.markdown(st.session_state.initial_srd_text)

    user_proxy = autogen.UserProxyAgent(name="CodeGenerationProxy", code_execution_config=False)

    if not st.session_state.workflow_started:
        if st.button("Start Code Generation Workflow ▶️"):
            st.session_state.workflow_started = True
            safe_rerun()

    if st.session_state.workflow_started and st.session_state.current_step < len(WORKFLOW_STEPS):
        step = WORKFLOW_STEPS[st.session_state.current_step]
        st.subheader(f"Step {st.session_state.current_step + 1}: {step['name']} (Attempt {st.session_state.retry_count + 1}/{MAX_RETRIES + 1})")

        if st.session_state.retry_count > MAX_RETRIES:
            st.error(f"Maximum retries ({MAX_RETRIES}) exceeded for this step.")
        else:
            # Generate code if not present
            if not st.session_state.current_code_to_review:
                with st.spinner(f"{step['name']} is generating code..."):
                    agent = step["agent_func"]()
                    st.session_state.current_agent = agent

                    context = (
                        st.session_state.initial_srd_text +
                        "\n\n--- PREVIOUSLY GENERATED CODE ---\n" +
                        "\n".join(st.session_state.generated_code.values())
                    )
                    history = [{"role": "user", "content": context}]
                    response = run_async(agent.a_generate_reply, history, user_proxy)
                    st.session_state.current_code_to_review = response

                safe_rerun()

            # Critic feedback
            if st.session_state.current_code_to_review and not st.session_state.critic_feedback:
                with st.spinner("Critic Agent is reviewing the code..."):
                    critic = get_critic_agent()
                    review_prompt = (
                        f"Please review the following generated code for quality, correctness, readability, and functionality:\n\n"
                        f"--- GENERATED CODE ---\n{st.session_state.current_code_to_review}"
                    )
                    history = [{"role": "user", "content": review_prompt}]
                    feedback = run_async(critic.a_generate_reply, history, user_proxy)
                    st.session_state.critic_feedback = feedback

                safe_rerun()

            # Show generated code and feedback
            if st.session_state.current_code_to_review and st.session_state.critic_feedback:
                st.text("Generated Code:")
                st.code(st.session_state.current_code_to_review, language="python")

                st.text("Critic Agent’s Feedback:")
                st.info(st.session_state.critic_feedback)

                prompt = st.chat_input("Type 'approve' to accept this code, or enter feedback to retry.")
                if prompt:
                    if prompt.strip().lower() == "approve":
                        # Save and advance step
                        st.session_state.generated_code[step["output_file"]] = st.session_state.current_code_to_review
                        output_path = Path("output") / step["output_file"]
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(st.session_state.current_code_to_review)
                        st.success(f"Code approved and saved to {output_path}")

                        st.session_state.current_step += 1
                        st.session_state.retry_count = 0
                        st.session_state.current_code_to_review = ""
                        st.session_state.critic_feedback = ""
                        st.session_state.agent_feedback_messages = []

                        safe_rerun()
                    else:
                        # Retry with feedback
                        st.session_state.retry_count += 1
                        st.session_state.current_code_to_review = ""
                        st.session_state.critic_feedback = ""
                        if "agent_feedback_messages" not in st.session_state:
                            st.session_state.agent_feedback_messages = []
                        st.session_state.agent_feedback_messages.append({"role": "user", "content": prompt})
                        ai_resp = run_async(
                            st.session_state.current_agent.a_generate_reply,
                            st.session_state.agent_feedback_messages,
                            user_proxy,
                        )
                        st.session_state.agent_feedback_messages.append(ai_resp)

                        safe_rerun()
    elif st.session_state.workflow_started:
        st.header("✅ Code Generation Workflow Complete!")
        st.success("All code artifacts have been generated and saved to the 'output' directory.")
        if st.button("Start a New Project"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            safe_rerun()
