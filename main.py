import streamlit as st
import os
from dotenv import load_dotenv
from utils.perplexity import fetch_structured_data_from_perplexity
from utils.gsheets import append_to_google_sheet
from utils.email_agent import send_email

# Load environment variables
load_dotenv()
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

st.title("AI Outreach Agent")

# Input for the search query
query = st.text_input("Query (e.g., AI student organizations)", placeholder="Enter search query")

if st.button("Fetch Organizations"):
    if not perplexity_api_key:
        st.error("Perplexity API Key is not set. Please configure it in the environment.")
    elif not query.strip():
        st.error("Query cannot be empty. Please enter a valid query.")
    else:
        try:
            organizations = fetch_structured_data_from_perplexity(query)
            st.session_state["organizations"] = organizations
            st.write("Found Organizations:")
            if organizations:
                for org in organizations:
                    st.write(f"{org['name']} - {org['email']}")
            else:
                st.warning("No organizations found. Try a different query.")
        except Exception as e:
            st.error(f"Error fetching organizations: {str(e)}")

if st.button("Save to Google Sheets"):
    if "organizations" in st.session_state and st.session_state["organizations"]:
        try:
            # Prepare data for appending
            data = [[org["name"], org["email"]] for org in st.session_state["organizations"]]
            updated_cells = append_to_google_sheet(data)
            st.success(f"Successfully saved to Google Sheets! {updated_cells} cells updated.")
        except RuntimeError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
    else:
        st.warning("No data to save. Please fetch organizations first.")

if st.button("Send Outreach Emails"):
    email_subject = st.text_input("Email Subject", placeholder="Enter email subject")
    email_body = st.text_area("Email Body", placeholder="Compose your email body here")
    smtp_server = st.text_input("SMTP Server", placeholder="e.g., smtp.gmail.com", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=465)
    sender_email = st.text_input("Your Email", placeholder="Enter your email address")
    sender_password = st.text_input("Your Email Password", type="password", placeholder="Enter your email password")

    if not email_subject.strip():
        st.error("Email subject cannot be empty.")
    elif not email_body.strip():
        st.error("Email body cannot be empty.")
    elif not sender_email.strip() or not sender_password.strip():
        st.error("Email credentials are required.")
    elif "organizations" in st.session_state and st.session_state["organizations"]:
        try:
            for org in st.session_state["organizations"]:
                send_email(smtp_server, smtp_port, sender_email, sender_password, org["email"], email_subject, email_body)
            st.success("Emails Sent!")
        except Exception as e:
            st.error(f"Error sending emails: {str(e)}")
    else:
        st.warning("No recipients available. Please fetch organizations first.")