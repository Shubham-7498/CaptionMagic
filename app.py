from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain_ollama import OllamaLLM
import torch
from PIL import Image

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path:str) -> str:
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0],skip_special_tokens= True)

    return caption

caption = generate_caption("./images/Sample1.jpg")
print(caption)

llm = OllamaLLM(model="llama2", temperature=0.7)

enhanced_prompt = f"Make this caption more creative, catchy and engaging for social media: {caption}, Don't print the prompts and other additional response text."
enhanced_caption = llm.invoke(enhanced_prompt)
print(enhanced_caption)

