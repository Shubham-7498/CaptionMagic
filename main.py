from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain_ollama import OllamaLLM
from PIL import Image
import streamlit as st
import torch

@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

def generate_caption(image:Image.Image, processor, model) -> str:
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0],skip_special_tokens= True)

    return caption

def load_llm(caption: str) -> str:
    llm = OllamaLLM(model="llama2", temperature=0.7)
    prompt = f"Make this caption more creative, catchy and attractive for social media: {caption} list only the captions without any additional text."
    return llm.invoke(prompt)

st.set_page_config(
    page_title="CaptionMagic",
    page_icon="📷",
    layout="wide"
)

st.markdown("""
<style>
    .title {
        font-size: 2.5rem !important;
        margin-bottom: 20px;
    }
    .title i {
        font-style: italic;
        font-weight: normal;
    }
</style>

<h1 class="title">CaptionMagic – <i> An AI Powered Image Caption Generator</i></h1>
""", unsafe_allow_html=True)
st.write("Upload an image and get a creative captions!")

with st.sidebar:
    st.header("CaptionMagic")
    upload_option = st.radio("Image Source", ("Upload Image", "Use Sample Image"))
    if upload_option == "Use Sample Image":
        sample_image= {"Sample 1":"./images/Sample1.jpg",
                       "Sample 2":"./images/Sample2.jpg",
                       "Sample 3":"./images/Sample3.jpg"}
        selected_sample = st.selectbox("Select sample image", list(sample_image.keys()))
    else:
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    generate_Button=st.button("Generate")

col1, col2 = st.columns(2)

with col1:
    if upload_option == "Upload Image" and uploaded_file is not None:
        st.subheader("Uploaded Image")
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)
    elif upload_option == "Use Sample Image":
        st.subheader("Uploaded Image")
        image = Image.open(sample_image[selected_sample]).convert("RGB")
        st.image(image, caption=f"Sample Image: {selected_sample}", use_container_width=True)

with col2:
    if generate_Button:
        st.subheader("Generated Caption")
        with st.spinner("Generating caption..."):
            processor, model = load_model()
            caption = generate_caption(image, processor, model)
            enhanced = load_llm(caption)
        st.write(enhanced)


