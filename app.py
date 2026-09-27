import streamlit as st
import json
import os

from utils.async_runner import get_async_runner

from team import run_team

from linkedin.auth import (
    build_authorization_url,
    exchange_code_for_token,
)

from linkedin.member import get_member_urn
from linkedin.publisher import publish_post


# ============================================================
# CONFIGURATION
# ============================================================

TOKEN_FILE = ".linkedin_token.json"
STATE_FILE = ".linkedin_oauth_state"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI LinkedIn Content Agent",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "generated" not in st.session_state:
    st.session_state.generated = False

if "approved" not in st.session_state:
    st.session_state.approved = False

if "published" not in st.session_state:
    st.session_state.published = False

if "linkedin_post_id" not in st.session_state:
    st.session_state.linkedin_post_id = None

if "linkedin_connected" not in st.session_state:
    st.session_state.linkedin_connected = False


# ============================================================
# LINKEDIN TOKEN HELPERS
# ============================================================

def linkedin_connected():

    try:

        with open(
            TOKEN_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            token_data = json.load(file)

        return bool(
            token_data.get("access_token")
        )

    except (
        FileNotFoundError,
        json.JSONDecodeError,
    ):

        return False


def save_linkedin_token(token_data):

    with open(
        TOKEN_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            token_data,
            file,
            indent=2,
        )


# ============================================================
# OAUTH STATE HELPERS
# ============================================================

def save_oauth_state(state):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(state)


def load_oauth_state():

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            return file.read().strip()

    except FileNotFoundError:

        return None


def delete_oauth_state():

    try:

        os.remove(STATE_FILE)

    except FileNotFoundError:

        pass


# ============================================================
# LINKEDIN OAUTH CALLBACK
# ============================================================

def handle_linkedin_callback():

    params = st.query_params

    code = params.get("code")
    state = params.get("state")
    error = params.get("error")

    # --------------------------------------------------------
    # Normal Streamlit page load
    # --------------------------------------------------------

    if not code and not error:

        return False


    # --------------------------------------------------------
    # LinkedIn authorization error
    # --------------------------------------------------------

    if error:

        st.error(
            f"❌ LinkedIn authorization failed: {error}"
        )

        return True


    # --------------------------------------------------------
    # Authorization code validation
    # --------------------------------------------------------

    if not code:

        st.error(
            "❌ No LinkedIn authorization code received."
        )

        return True


    # --------------------------------------------------------
    # OAuth state validation
    # --------------------------------------------------------

    expected_state = load_oauth_state()

    if not expected_state:

        st.error(
            "❌ OAuth state was not found."
        )

        st.info(
            "Please click Connect LinkedIn again."
        )

        return True


    if state != expected_state:

        st.error(
            "❌ OAuth security validation failed."
        )

        st.info(
            "The OAuth state does not match. "
            "Please start the LinkedIn connection again."
        )

        delete_oauth_state()

        return True


    # --------------------------------------------------------
    # Exchange authorization code
    # --------------------------------------------------------

    try:

        with st.spinner(
            "🔗 Connecting to LinkedIn..."
        ):

            token_data = exchange_code_for_token(
                code
            )

            save_linkedin_token(
                token_data
            )

            delete_oauth_state()


        st.session_state.linkedin_connected = True

        st.success(
            "✅ LinkedIn connected successfully!"
        )

        st.info(
            "You can now use the LinkedIn Content Agent."
        )


        # Remove OAuth parameters from URL

        st.query_params.clear()

        return True


    except Exception as exc:

        st.error(
            "❌ LinkedIn token exchange failed."
        )

        st.code(
            str(exc)
        )

        return True


# ============================================================
# PROCESS OAUTH CALLBACK
# ============================================================

handle_linkedin_callback()


# ============================================================
# CHECK EXISTING LINKEDIN CONNECTION
# ============================================================

if linkedin_connected():

    st.session_state.linkedin_connected = True


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 AI LinkedIn Content Agent"
)

st.markdown(
    """
Generate professional LinkedIn content using a multi-agent
AutoGen workflow with research, writing, SEO optimization,
guardrails, DeepEval, human approval and direct LinkedIn
publishing.
"""
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "⚙️ Workflow"
    )

    st.success(
        "1. Research Agent"
    )

    st.success(
        "2. Content Writer Agent"
    )

    st.success(
        "3. SEO / LinkedIn Agent"
    )

    st.success(
        "4. Guardrails"
    )

    st.success(
        "5. DeepEval"
    )

    st.success(
        "6. Human Approval"
    )

    if st.session_state.linkedin_connected:

        st.success(
            "7. LinkedIn Connected"
        )

    else:

        st.warning(
            "7. LinkedIn Not Connected"
        )

    st.divider()

    st.caption(
        "AutoGen • Guardrails • DeepEval • LinkedIn API"
    )


# ============================================================
# LINKEDIN CONNECTION
# ============================================================

st.subheader(
    "🔗 LinkedIn Connection"
)


if st.session_state.linkedin_connected:

    st.success(
        "✅ LinkedIn account connected"
    )

else:

    st.info(
        "Connect your LinkedIn account before publishing."
    )

    if st.button(
        "🔐 Connect LinkedIn",
        type="primary",
        use_container_width=True,
    ):

        authorization_url, state = (
            build_authorization_url()
        )

        save_oauth_state(
            state
        )

        st.link_button(
            "➡️ Continue with LinkedIn",
            authorization_url,
            use_container_width=True,
        )


st.divider()


# ============================================================
# CONTENT GENERATION
# ============================================================

st.subheader(
    "📝 Create LinkedIn Content"
)


topic = st.text_input(
    "Enter your topic",
    placeholder=(
        "Example: Agentic AI Testing in Enterprise Applications"
    ),
)


if st.button(
    "🚀 Generate LinkedIn Content",
    type="primary",
    use_container_width=True,
):

    if not topic.strip():

        st.warning(
            "Please enter a topic."
        )

    else:

        with st.spinner(
            "🤖 AutoGen agents are researching, "
            "writing and optimizing..."
        ):

            try:

                # Use persistent async event loop
                runner = get_async_runner()

                result = runner.run(
                    run_team(
                        topic.strip()
                    )
                )


                # Store result
                st.session_state.result = result

                st.session_state.generated = True

                # Reset approval/publishing
                st.session_state.approved = False

                st.session_state.published = False

                st.session_state.linkedin_post_id = None


                st.success(
                    "✅ Content generated and validated successfully."
                )


            except Exception as exc:

                st.session_state.result = None

                st.session_state.generated = False

                st.session_state.approved = False

                st.session_state.published = False

                st.error(
                    f"❌ Content generation failed:\n\n{exc}"
                )


# ============================================================
# GENERATED CONTENT
# ============================================================

if (
    st.session_state.generated
    and st.session_state.result
):

    result = st.session_state.result

    st.divider()


    # ========================================================
    # GENERATION SUMMARY
    # ========================================================

    st.subheader(
        "📊 Generation Summary"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Topic",
            result["topic"],
        )


    with col2:

        st.metric(
            "Research",
            "Completed",
        )


    with col3:

        st.metric(
            "Validation",
            "Passed",
        )


    # ========================================================
    # RESEARCH OUTPUT
    # ========================================================

    with st.expander(
        "🔎 Research Output"
    ):

        st.write(
            result.get(
                "research",
                "No research output available.",
            )
        )


    # ========================================================
    # ARTICLE DRAFT
    # ========================================================

    with st.expander(
        "✍️ Article Draft"
    ):

        st.write(
            result.get(
                "article",
                "No article available.",
            )
        )


    # ========================================================
    # FINAL LINKEDIN POST
    # ========================================================

    st.subheader(
        "📢 Final LinkedIn Post"
    )


    final_content = result.get(
        "final_content",
        "",
    )


    edited_content = st.text_area(
        "Review / Edit Content",
        value=final_content,
        height=500,
        key="linkedin_content",
    )


    # ========================================================
    # HUMAN APPROVAL
    # ========================================================

    st.divider()

    st.subheader(
        "👤 Human Approval"
    )

    st.warning(
        "Review the content above before publishing."
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # APPROVE
    # --------------------------------------------------------

    with col1:

        if st.button(
            "✅ Approve Content",
            key="approve_content",
            use_container_width=True,
        ):

            st.session_state.approved = True

            st.session_state.published = False

            st.success(
                "✅ Content approved by human."
            )

            # Force Streamlit to immediately
            # render the publishing section

            st.rerun()


    # --------------------------------------------------------
    # REJECT
    # --------------------------------------------------------

    with col2:

        if st.button(
            "❌ Reject Content",
            key="reject_content",
            use_container_width=True,
        ):

            st.session_state.approved = False

            st.session_state.published = False

            st.session_state.linkedin_post_id = None

            st.error(
                "❌ Content rejected. Publishing stopped."
            )


    # ========================================================
    # LINKEDIN PUBLISHING
    # ========================================================

    if st.session_state.get(
        "approved",
        False,
    ):

        st.divider()

        st.subheader(
            "🚀 LinkedIn Publishing"
        )


        # ----------------------------------------------------
        # LINKEDIN NOT CONNECTED
        # ----------------------------------------------------

        if not st.session_state.linkedin_connected:

            st.error(
                "❌ LinkedIn account is not connected."
            )

            st.info(
                "Please connect LinkedIn before publishing."
            )


        # ----------------------------------------------------
        # ALREADY PUBLISHED
        # ----------------------------------------------------

        elif st.session_state.get(
            "published",
            False,
        ):

            st.success(
                "🎉 LinkedIn post has already been published."
            )


            if st.session_state.get(
                "linkedin_post_id"
            ):

                st.write(
                    "LinkedIn Post ID:"
                )

                st.code(
                    st.session_state.linkedin_post_id
                )


        # ----------------------------------------------------
        # READY TO PUBLISH
        # ----------------------------------------------------

        else:

            st.success(
                "✅ Content approved and LinkedIn is connected."
            )

            st.write(
                "Your content is ready to publish."
            )


            if st.button(
                "🚀 Publish to LinkedIn",
                key="publish_to_linkedin",
                type="primary",
                use_container_width=True,
            ):

                try:

                    with st.spinner(
                        "Publishing to LinkedIn..."
                    ):

                        # ------------------------------------
                        # Get LinkedIn member URN
                        # ------------------------------------

                        author_urn = get_member_urn()


                        # ------------------------------------
                        # Publish approved content
                        # ------------------------------------

                        post_id = publish_post(
                            author_urn=author_urn,
                            post_text=edited_content,
                        )


                    # ----------------------------------------
                    # Store publishing result
                    # ----------------------------------------

                    st.session_state.published = True

                    st.session_state.linkedin_post_id = (
                        post_id
                    )


                    st.success(
                        "🎉 LinkedIn post published successfully!"
                    )


                    st.write(
                        "LinkedIn Post ID:"
                    )


                    st.code(
                        post_id
                        or "Post ID unavailable"
                    )


                except Exception as exc:

                    st.error(
                        "❌ LinkedIn publishing failed:"
                    )

                    st.code(
                        str(exc)
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Powered by AutoGen • Guardrails • DeepEval • LinkedIn API"
)