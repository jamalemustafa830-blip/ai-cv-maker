import streamlit as st
from groq import Groq
from fpdf import FPDF

st.set_page_config(page_title="Free AI CV Maker", layout="centered")

st.title("📄 Free AI CV Builder")
st.write("Apni details Urdu, Roman Urdu ya English me likhein, AI aap ko English CV bana kar de ga!")

# Groq API Key Input
api_key = st.text_input("Apni Groq API Key yahan paste karein:", type="password")

# User Form
user_input = st.text_area(
    "Apni details likhein (Name, Contact, Education, Experience, Skills):",
    height=200,
    placeholder="Mera naam Ali hai. Phone: 03001234567. Maine BA kiya hai. Sales me 2 saal ka experience hai..."
)

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    lines = text.split('\n')
    for line in lines:
        clean_line = line.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, clean_line)
        
    return pdf.output(dest='S').encode('latin-1')

if st.button("CV Banayein ✨"):
    if not api_key:
        st.error("Pehle apni Groq API Key darj karein!")
    elif not user_input:
        st.warning("Baraye mehrbani apni details likhein!")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are a professional resume writer.
            Convert the following user information into a well-formatted, complete professional English CV.
            Translate and refine any Urdu or Roman Urdu input into accurate, formal English.

            CV Sections:
            - Full Name
            - Contact Information
            - Professional Summary
            - Work Experience
            - Education
            - Key Skills

            User Info:
            {user_input}
            """

            with st.spinner("AI aap ki CV bana raha hai..."):
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                
                cv_result = response.choices[0].message.content
                
                st.success("CV Tayar Hai!")
                st.markdown("### CV Preview:")
                st.text_area("Aap ki Resulting CV:", cv_result, height=300)
                
                pdf_bytes = generate_pdf(cv_result)
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name="Professional_CV.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Ghalti aa gayi: {e}")
