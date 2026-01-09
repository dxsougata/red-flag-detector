import streamlit as st
from groq import Groq
import base64

# --- CONFIGURATION ---
# Replace with your actual GroqCloud API Key
# (Best practice: Store this in an environment variable or a .env file)
# Instead of "gsk_...", we look for the key in Streamlit's secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize the Groq Client
client = Groq(api_key=GROQ_API_KEY)

# The model: Llama 3.2 11B Vision is fast. 
# If you need more "smarts", switch to "llama-3.2-90b-vision-preview"
MODEL_ID = "meta-llama/llama-4-scout-17b-16e-instruct"

def encode_image(uploaded_file):
    """Helper to convert the uploaded image to base64"""
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

def analyze_with_groq(image_base64, user_prompt):
    """Sends the image to Groq for analysis"""
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}",
                            },
                        },
                    ],
                }
            ],
            temperature=0.6, 
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- DASHBOARD UI ---
st.set_page_config(page_title="Red Flag Detector (Groq Edition)", layout="wide", page_icon="🚩")

st.title("🚩 Red Flag Detector")
#st.caption(f"Powered by GroqCloud LPU • Model: {MODEL_ID}")

# Sidebar
with st.sidebar:
    st.header("Control Panel")
    mode = st.radio(
        "Analysis Mode",
        ["Red Flag Scanner 🚩", "Rizz Rater ⚡", "The 'Summary' 📝"]
    )
    
    st.markdown("---")
    st.markdown("**How it works:**\n\nUpload a screenshot of a chat/bio. The AI will analyze the text inside the image instantly. But currently it only support English language")

# Main Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Upload Evidence")
    uploaded_file = st.file_uploader("Drop the screenshot here...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Preview", use_container_width=True)

with col2:
    st.subheader("2. The Verdict")
    if uploaded_file is not None:
        analyze_btn = st.button("Scan for Red Flags", type="primary")
        
        if analyze_btn:
            # Spinner text customized for Groq's speed
            with st.spinner("Processing at light speed..."):
                
                # 1. Select the prompt based on mode
                if mode == "Red Flag Scanner 🚩":
                    prompt = "Analyze this chat screenshot. Act like a brutally honest dating coach. Identify toxic traits, manipulation, or 'red flags'. Give a 'Toxic Score' out of 10.Do all of this within 20 words."
                elif mode == "Rizz Rater ⚡":
                    prompt = "Analyze the flirting in this screenshot. Is it smooth or cringe? Rate the 'Rizz' from 1 to 10 and explain why."
                else:
                    prompt = "Summarize this conversation. Who are the people? What is the main conflict or topic?"

                # 2. Encode Image
                base64_img = encode_image(uploaded_file)
                
                # 3. Call Groq
                result = analyze_with_groq(base64_img, prompt)
                
                # 4. Show Output
                st.success("Analysis Complete!")
                st.markdown("### The Verdict:")
                st.write(result)
    else:

        st.info("Waiting for upload...")

