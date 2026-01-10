import streamlit as st
from groq import Groq
import base64

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Red Flag Detector", layout="wide", page_icon="🚩")

# --- 2. CSS STYLING ---
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #0E1117; }
    
    /* Neon Red Buttons */
    div.stButton > button:first-child {
        background-color: #FF4B4B; color: white; border-radius: 20px;
        border: 2px solid #FF4B4B; font-weight: bold; font-size: 20px;
        padding: 10px 24px; width: 100%;
    }
    div.stButton > button:hover {
        background-color: #FF0000; border-color: #FF0000;
        transform: scale(1.02); transition: all 0.3s;
    }
    img { border-radius: 15px; box-shadow: 0 0 15px rgba(255, 75, 75, 0.5); }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- 3. API SETUP ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = "gsk_..." # PUT KEY HERE FOR LOCAL TESTING

client = Groq(api_key=GROQ_API_KEY)

# We use two different models now!
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # For Images
TEXT_MODEL = "llama-3.3-70b-versatile"         # For Text Files (Smarter)

# --- 4. HELPER FUNCTIONS ---
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

def analyze_image(image_base64, prompt):
    """Function for Screenshot Analysis"""
    try:
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
                    ],
                }
            ],
            temperature=0.6,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_text_file(chat_content, prompt):
    """Function for Text File Analysis"""
    # We combine the prompt and the chat logs
    full_message = f"{prompt}\n\n--- START OF CHAT LOG ---\n{chat_content}\n--- END OF CHAT LOG ---"
    
    try:
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": "You are a relationship expert AI."},
                {"role": "user", "content": full_message}
            ],
            temperature=0.6,
            max_tokens=2000, # Text files can be long, so we allow more tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- 5. MAIN UI LAYOUT ---
st.title("🚩 Red Flag Detector")
st.caption("Powered by GroqCloud • Supports Screenshots & WhatsApp Exports")

# Sidebar
with st.sidebar:
    st.header("Control Panel")
    mode = st.radio("Analysis Mode", ["Red Flag Scanner 🚩", "Rizz Rater ⚡", "The 'Summary' 📝"])
    st.markdown("---")
    st.info("💡 Tip: For WhatsApp exports, choose the '.txt' tab.")

# Main Tabs
tab1, tab2 = st.tabs([" **Upload Screenshot**", " **Upload Text File (.txt)**"])

# --- TAB 1: IMAGE LOGIC (Existing) ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        img_file = st.file_uploader("Upload Chat Screenshot", type=['png', 'jpg', 'jpeg'], key="img_upload")
        if img_file:
            st.image(img_file, caption="Preview", use_container_width=True)

    with col2:
        if img_file:
            if st.button("SCAN IMAGE", type="primary", key="btn_img"):
                with st.spinner("🕵️‍♂️ Analyzing Screenshot..."):
                    
                    # Language Context
                    lang_ctx = "Note: Text may be Hinglish/Benglish. Understand the slang."
                    
                    if mode == "Red Flag Scanner 🚩":
                        prompt = f"{lang_ctx} Analyze this chat image. Identify toxic traits. Be brutally honest. Give a 'Toxic Score' (0-100%). Do it within 20 sentence with 3 bullet points 1st one include score in percentage."
                    elif mode == "Rizz Rater ⚡":
                        prompt = f"{lang_ctx} Rate the Rizz (0-100%). Is it cringe or smooth?Do it within 20 sentence with 3 bullet points 1st one include score in percentage."
                    else:
                        prompt = f"{lang_ctx} Summarize this conversation."

                    base64_img = encode_image(img_file)
                    result = analyze_image(base64_img, prompt)
                    
                    st.markdown("---")
                    if "toxic" in result.lower() or "red flag" in result.lower():
                        st.error(result)
                    else:
                        st.success(result)
                        st.balloons()

# --- TAB 2: TEXT FILE LOGIC (New!) ---
# --- TAB 2: TEXT FILE LOGIC (FIXED) ---
with tab2:
    st.markdown("### How to get your WhatsApp Chat:")
    st.caption("Open WhatsApp Chat > 3 dots > More > Export Chat > Without Media.")
    
    txt_file = st.file_uploader("Upload WhatsApp .txt file", type=['txt'], key="txt_upload")
    
    if txt_file:
        # FIX 1: Reset the file pointer to the beginning before reading
        txt_file.seek(0)
        
        # FIX 2: robust decoding (Try UTF-8, if fails, try Latin-1)
        try:
            chat_content = txt_file.read().decode("utf-8")
        except UnicodeDecodeError:
            txt_file.seek(0) # Reset again before retry
            chat_content = txt_file.read().decode("latin-1")
            
        # Show a snippet of the chat
        with st.expander("👁️ Preview Chat Log"):
            st.text(chat_content[:1000] + "...") 
        
        # We store the content in session state so it doesn't disappear on button click
        st.session_state['chat_content'] = chat_content
        
        if st.button("ANALYZE FULL CHAT", type="primary", key="btn_txt"):
            if 'chat_content' in st.session_state:
                with st.spinner("📖 Reading the whole history (Hinglish/Benglish supported)..."):
                    
                    lang_ctx = "The following is a raw WhatsApp chat export. It may contain Hinglish (Hindi-English) or Benglish. Ignore timestamps."
                    
                    if mode == "Red Flag Scanner 🚩":
                        prompt = f"{lang_ctx} Analyze the relationship dynamic in this chat log. Who is putting in more effort? Are there signs of manipulation? Give a Toxic Score between 0 to 100 %. Do it within 20 sentence with 3 bullet points 1st one include score in percentage."
                    elif mode == "Rizz Rater ⚡":
                        prompt = f"{lang_ctx} Read this chat history. Rate the flirting skills. Who has better 'game'? Quote specific lines.Do it within 20 sentence with 3 bullet points 1st one include score in percentage."
                    else:
                        prompt = f"{lang_ctx} Summarize the timeline of this conversation. How did the mood change from start to finish?"

                    # Use the text stored in variable
                    result = analyze_text_file(st.session_state['chat_content'], prompt)
                    
                    st.markdown("---")
                    st.subheader("📝 Chat Analysis")
                    st.write(result)
                    
        ##except Exception as e:
            ##st.error("Error reading file. Make sure it's a valid UTF-8 text file.")


