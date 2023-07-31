
def upload(image_path):
    """
    Upload an image file to Imgur.

    :param image_path: Local path to the image file.
    :return: URL of the uploaded image.
    """
    # Open the image file
    with Image.open(image_path) as img:
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

    # Convert bytes to base64 encoded string
    image_b64 = base64.b64encode(img_byte_arr).decode('utf-8')

    # Create a dict to hold the data for the POST request
    data = {
        'image': image_b64,
        'type': 'base64'
    }

    # Make the POST request to Imgur's API
    response = requests.post(
        url='https://api.imgur.com/3/image',
        headers=HEADERS,
        data=data
    )

    # Raise an exception if the status code indicates a server error
    response.raise_for_status()

    # Extract the 'link' field from the response JSON, this is the URL of the uploaded image
    url = response.json()['data']['link']

    return url

class Chat:
    def __init__(self, system_prompt=''):
        self.system = system_prompt
        self.messages = []
    
    def response(self, prompt):
        self.messages.append({"role": "user", "content":prompt})
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
        #   model="gpt-4-0314",
        messages = self.messages,
#         max_tokens=200
        )
        response = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content":response})
        return response
    

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    verbose=True, # Print debug messages.
    engine="stable-diffusion-xl-1024-v0-9", # Set the engine to use for generation.
    # Available engines: stable-diffusion-xl-1024-v0-9 stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0
    # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-diffusion-xl-beta-v2-2-2 stable-inpainting-v1-0 stable-inpainting-512-v2-0
)

def generate_description(prompt, system_prompt=''):
    prompt_prefix = """
    You are an artist who comes up with phenomenal descritptions of images, flush with detail.
    When given a description of a podcast, you come up with an image that it would be wonderful to put as the photo shown in the video of the podcast.
    You describe this image, and only this image, in detail.
    The description:
    
    """
    ai_chat = Chat(system_prompt)
    return ai_chat.response(prompt_prefix + prompt)


def generate(user_text, return_val='img'):
    answers = stability_api.generate(
#     prompt="expansive landscape rolling greens with blue daisies and yggdrasil under a blue alien sky, masterful, ghibli",
    prompt=generate_description(user_text),
    seed=992446758, # If a seed is provided, the resulting generated image will be deterministic.
                    # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                    # Note: This isn't quite the case for CLIP Guided generations, which we tackle in the CLIP Guidance documentation.
    steps=50, # Amount of inference steps performed on image generation. Defaults to 30.
    cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                   # Setting this value higher increases the strength in which it tries to match your prompt.
                   # Defaults to 7.0 if not specified.
    width=1024, # Generation width, if not included defaults to 512 or 1024 depending on the engine.
    height=2048, # Generation height, if not included defaults to 512 or 1024 depending on the engine.
    samples=1, # Number of images to generate, defaults to 1 if not included.
    sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
)

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save(prompt[:30] + ".png")
                return img
    