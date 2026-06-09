# pip install -U diffusers transformers accelerate sentencepiece torch safetensors python-dotenv torchvision

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from dotenv import load_dotenv
from diffusers import FluxPipeline
import torch
import time

load_dotenv()

MODEL_ID = "black-forest-labs/FLUX.1-schnell"

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

print("토큰 로드 여부:", hf_token is not None)
print("Loading model...")

pipe = FluxPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
    token=hf_token
)

pipe = pipe.to("cpu")

prompt = """
ultra realistic photo of a korean girl,
cinematic lighting,
highly detailed,
8k,
professional photography
"""

start = time.time()

image = pipe(
    prompt,
    guidance_scale=0.0,
    num_inference_steps=2,
    height=512,
    width=512,
).images[0]

image.save("flux_output.png")

print(f"done : {time.time()-start:.1f} sec")