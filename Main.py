from openai import OpenAI

import streamlit as st

st.title("Thothica Test Taker App")

client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "Act as Essay Evaluator GPT. Essay Evaluator is designed to assist in grading philosophy essays based on specific rubrics. It focuses on five key areas: introduction content, body paragraph content, conclusion content, organization, and academic writing conventions. Each area has a set of criteria defining Excellent, Competent, and Needs Development grades. The evaluator will analyze the essay to check if it introduces the topic, author, and text effectively, structures the body paragraphs with focus and relevant content, provides a strong conclusion with personal insights, organizes content logically, and adheres to academic writing standards. It will assess each category independently, assign a grade based on the rubric, calculate the final grade considering the weighted percentages, and provide constructive feedback. The evaluator is tailored for essays exploring philosophical schools of thought, requiring critical analysis, argument evaluation, and reflection on philosophical questions and contemporary relevance. It ensures that essays use credible sources, are well-organized, and follow formatting guidelines.",
        },
        {
            "role": "user",
            "content": """Provide detailed scoring and feedback for this essay on the Rubrics defined:

<PDF text>

enclose your detailed assessment and feedback in the following XML tags:

<assessment>
</assessment>

enclose the component-wise score out of 100 in the following XML tags:
<component_grade>
</component_grade>

enclose the overall score out of 100 in the following XML tags:
<grade>
</grade>""",
        },
    ]

if len(st.session_state.messages) == 2:
    response = client.chat.completions.create(
        model="gpt-4-1106-preview", messages=st.session_state.messages
    )
    if "<question>" in response.choices[0].message.content.split():
        response = (
            response.choices[0].message.content.split("<question>")[0]
            + " \n\n ## Question "
            + response.choices[0]
            .message.content.split("<question>")[1]
            .split("</question>")[0]
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
    else:
        st.session_state.messages.append(
            {"role": "assistant",
                "content": response.choices[0].message.content}
        )

for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input()
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = client.chat.completions.create(
            model="gpt-4", messages=st.session_state.messages
        )
        full_response = response.choices[0].message.content
        full_response = "AAAAAAAAA" + full_response

        assessment = full_response.split("<assessment>")[
            1].split("</assessment>")[0]
        score = full_response.split("<grade>")[1].split("</grade>")[0]
        c_score = full_response.split("<component_grade>")[
            1].split("</component_grade>")[0]

        st.markdown("## Assessment - \n\n " + assessment)
        st.markdown("## Component_grade - \n\n " + c_score.replace("\n", "\n\n"))
        st.markdown("## Grade - \n\n " + score)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content":
            "## Assessment - \n\n "
            + assessment
            + " \n\n "
            + "## Component_grade - \n\n"
            + c_score
            + "## Grade - \n\n "
            + score,
        }
    )