
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# replace with stuff you need
project_id = "{your gcp project id}"
output_file = "my-output.png"
prompt = "Generate a cover image that can go along with this poem 'Deaths touch, a fleeting, painless sting, But living shadowed, soul wont sing. Defeat may linger, steal your fire, But rise, ignite a new desire. Though faltered steps may mark the way, Undying spirit lights the day. Embrace the fight, each trial faced, For victorys song is hard-won, graced. So let not slumbering shadows reign, Choose glorys path, defy the pain. Live bold, live bright, with purpose strong, Death holds no fear, where you belong.'" # The text prompt describing what you want to see.

# This uses Google Imagen2. You must have access to it in order to use this generation. 
vertexai.init(project=project_id, location="us-central1")
model = ImageGenerationModel.from_pretrained("imagegeneration@006")

images = model.generate_images(
    prompt=prompt,
    # Optional parameters
    number_of_images=1,
    language="en",
    # You can't use a seed value and watermark at the same time.
    # add_watermark=False,
    seed=100,
    aspect_ratio="1:2",
    safety_filter_level="block_some",
    person_generation="dont_allow",
)

images[0].save(location=output_file, include_generation_parameters=False)

# Optional. View the generated image in a notebook.
# images[0].show()

print(f"Created output image using {len(images[0]._image_bytes)} bytes")