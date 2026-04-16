import torch
from diffusers import StableDiffusionXLAdapterPipeline, T2IAdapter
from PIL import Image
import requests
from io import BytesIO

# -----------------------------
# 1. Load the control image (e.g., depth map, canny edges, sketch)
# -----------------------------
control_image_url = "https://huggingface.co/datasets/hf-internal-testing/diffusers-images/resolve/main/t2i-adapter/canny.png"
response = requests.get(control_image_url)
control_image = Image.open(BytesIO(response.content)).convert("RGB")

# -----------------------------
# 2. Load the T2I Adapter model
# -----------------------------
adapter = T2IAdapter.from_pretrained(
    "TencentARC/t2i-adapter-canny-sdxl-1.0",
    torch_dtype=torch.float16
)

# -----------------------------
# 3. Load the Stable Diffusion XL pipeline with the adapter
# -----------------------------
pipe = StableDiffusionXLAdapterPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    adapter=adapter,
    torch_dtype=torch.float16
).to("cuda")

# -----------------------------
# 4. Generate an image
# -----------------------------
prompt = "A futuristic city skyline at sunset, ultra detailed, cinematic lighting"
negative_prompt = "blurry, low quality, distorted"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    image=control_image,
    num_inference_steps=30,
    guidance_scale=7.5,
    adapter_conditioning_scale=0.8  # How strongly to follow the control image
).images[0]

# -----------------------------
# 5. Save the result
# -----------------------------
image.save("t2i_result.png")
print("Image saved as t2i_result.png")

