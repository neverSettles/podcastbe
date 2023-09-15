import os
import requests
import base64
from time import sleep
from generate_audio import generate_podcast
from generate_video import generate_image

def authorize_upload(path):
    print("Authorizing upload...")
    # Get the filename from the path
    filename = os.path.basename(path)
    # Define the API endpoint
    url = "https://api.transistor.fm/v1/episodes/authorize_upload"
    # Get the API key from the environment variables
    api_key = os.getenv("TRANSISTOR_API_KEY")
    # Set the headers for the request
    headers = {"x-api-key": api_key}
    # Define the parameters for the request
    params = {"filename": filename}
    # Send the GET request
    response = requests.get(url, headers=headers, params=params)
    # Print the response
    print("Response:", response.json())
    # Check that the request was successful
    response.raise_for_status()
    # Extract the upload URL
    response_json = response.json()
    data = response_json.get("data", {})
    attributes = data.get("attributes", {})
    upload_url = attributes.get("upload_url")
    audio_url = attributes.get("audio_url")
    content_type = attributes.get("content_type")
    return upload_url, audio_url, content_type


def upload_file(path, upload_url, content_type):
    print("Uploading file...")
    # Read the file data
    with open(path, "rb") as f:
        file_data = f.read()

    # Set the headers for the request
    headers = {
        "Content-Type": content_type,
    }

    # Send the PUT request to upload the file
    response = requests.put(upload_url, headers=headers, data=file_data)

    # Check that the request was successful
    response.raise_for_status()
    print("File uploaded successfully.")


def create_episode(show_id, title, summary, audio_url, image_url):
    api_key = os.getenv("TRANSISTOR_API_KEY")
    url = "https://api.transistor.fm/v1/episodes"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }
    data = {
        "episode": {
            "show_id": show_id,
            "title": title,
            "summary": summary,
            "audio_url": audio_url,
            "image_url": image_url,
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    response.raise_for_status()
    print("Response:", response.json())
    print(f'Episode "{title}" created successfully.')
    response_json = response.json()
    episode_id = response_json.get("data", {}).get("id")
    share_url = response_json.get("data", {}).get("attributes", {}).get("share_url")
    share_url = response_json.get("data", {}).get("attributes", {}).get("embed_html")
    return episode_id, share_url


def publish_episode(episode_id):
    print("Publishing episode...")
    # Define the API endpoint
    url = f"https://api.transistor.fm/v1/episodes/{episode_id}/publish"
    # Get the API key from the environment variables
    api_key = os.getenv("TRANSISTOR_API_KEY")
    # Set the headers for the request
    headers = {"x-api-key": api_key}
    # Define the data for the request
    data = {"episode": {"status": "published"}, "fields": {"episode": ["status"]}}
    # Send the PATCH request
    response = requests.patch(url, headers=headers, json=data)
    # Check that the request was successful
    response.raise_for_status()
    # Print the response
    print("Response:", response.json())
    return response.json()


def upload_image_to_imgur(image_path, client_id):
    print("Uploading image...")
    url = "https://api.imgur.com/3/upload"
    headers = {"Authorization": "Client-ID " + client_id}
    with open(image_path, "rb") as img:
        img_b64 = base64.b64encode(img.read())
    data = {"image": img_b64, "type": "base64"}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    print("Image uploaded successfully.")
    link = response.json().get("data", {}).get("link")
    return link


def generate_episode(prompt, original_prompt, length=60):
    audio_file = generate_podcast(prompt, original_prompt, length)
    upload_url, audio_url, content_type = authorize_upload(audio_file)
    upload_file(audio_file, upload_url, content_type)

    image_file = generate_image(original_prompt)
    image_url = upload_image_to_imgur(image_file, "1b765e0d179f29e")
    print(image_url)

    episode_id, share_url = create_episode(
        "44271",
        title=original_prompt,
        summary=original_prompt,
        audio_url=audio_url,
        image_url=image_url,
    )
    publish_episode(episode_id)
    print(f"Podcast published at {share_url}.")
    print('Sleeping for 2 seconds to allow image to sync...')
    sleep(2)

    return share_url


if __name__ == "__main__":
    # generate_episode("Compare RNNs with Transformers", "Compare RNNs with Transformers", 60)
    original_prompt = "Guatemala recent election"
    audio_file = 'output/speech.mp3'

    upload_url, audio_url, content_type = authorize_upload(audio_file)
    upload_file(audio_file, upload_url, content_type)

    image_file = generate_image(original_prompt)
    image_url = upload_image_to_imgur(image_file, "1b765e0d179f29e")
    print(image_url)

    episode_id, share_url = create_episode(
        "44271",
        title=original_prompt,
        summary=original_prompt,
        audio_url=audio_url,
        image_url=image_url,
    )
    publish_episode(episode_id)

    # original_prompt = "Guatemala recent election"

    # audio_url = "https://transistorupload.s3.amazonaws.com/uploads/api/ba1e0e14-5b47-498d-bded-5ed371e20d4b/guatemala%27s_recent_election.mp3"
    # image_url="https://i.imgur.com/pcBDQIa.png"
    # episode_id, share_url = create_episode(
    #     "your-podcast",
    #     title=original_prompt,
    #     summary=original_prompt,
    #     audio_url=audio_url,
    #     image_url=image_url,
    # )

    # publish_episode(episode_id)