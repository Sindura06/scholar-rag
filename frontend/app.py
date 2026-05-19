import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="ScholarRAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 ScholarRAG")
st.subheader("Local Research Paper Assistant for AI and Data Science Papers")

st.write(
    "Ask questions over your local arXiv research paper knowledge base. "
    "Answers are generated using retrieved paper chunks and shown with sources."
)

question = st.text_area(
    "Enter your research question:",
    placeholder="Example: What is retrieval augmented generation?",
    height=100
)

top_k = st.slider(
    "Number of retrieved chunks",
    min_value=3,
    max_value=10,
    value=5
)

ask_button = st.button("Ask ScholarRAG")

if ask_button:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving papers and generating answer..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": question,
                        "top_k": top_k
                    },
                    timeout=180
                )

                response.raise_for_status()
                data = response.json()

                st.markdown("## Answer")
                st.write(data["answer"])

                st.markdown("## Sources")

                for source in data["sources"]:
                    with st.expander(
                        f"Source [{source['source_id']}] | "
                        f"Topic: {source['topic']} | "
                        f"Score: {source['score']:.4f}"
                    ):
                        st.write(f"**PDF:** {source['source_pdf']}")
                        st.write(f"**Chunk Index:** {source['chunk_index']}")
                        st.markdown("**Text Preview:**")
                        st.write(source["text_preview"])

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the FastAPI backend. "
                    "Make sure the backend is running on http://127.0.0.1:8000"
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")