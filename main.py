from fileinput import filename
import os
import os.path
from os import listdir
from urllib.parse import urlparse
import requests
import dotenv
from pathlib import Path
import random


def get_file_ext(link):
    cut = urlparse(link)
    return os.path.splitext(cut.path)[-1]


def get_xkcd():
    response_last = requests.get(
        "https://xkcd.com/info.0.json")
    response_last.raise_for_status()
    response_json_last = response_last.json()
    last_xkcd = response_json_last['num']
    random_num = random.randint(1, last_xkcd)
    response = requests.get(
        f"https://xkcd.com/{random_num}/info.0.json"
    )
    response.raise_for_status()
    response_json = response.json()
    image_links = response_json.get('img')
    file_ext = get_file_ext(image_links)
    return response_json.get('alt'), f"images/xkcd{response_json.get('num')}{file_ext}", image_links


def save_images(image_links, filename):
    response = requests.get(image_links)
    response.raise_for_status()
    with open(filename, "wb") as file:
        file.write(response.content)


def get_server_vk(token_vk):
    response = requests.get("https://api.vk.com/method/photos.getWallUploadServer", 
    params={ 
        "v":5.131, 
        "access_token":token_vk
        }
        )
    response.raise_for_status()
    return response.json()['response']['upload_url']


def file_upload_vk(token_vk, filename):
    url = get_server_vk(token_vk)
    with open(f"{filename}", "rb") as file:
        files = {
        'file1': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        result = response.json()
        return result['photo'], result['hash'], result['server']


def save_file_vk(token_vk, photo, hash, server, user_id):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        'photo': photo,
        'hash': hash,
        'server': server,
        'user_id': user_id,
        "v":5.131, 
        "access_token":token_vk,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    results = response.json()
    for result in results['response']:
        return result['owner_id'], result['id']


def publish_image_vk(comment, token_vk, photo_id, owner_id, group_id):
    url = "https://api.vk.com/method/wall.post"
    params = {
        "v":5.131, 
        "access_token":token_vk,
        "owner_id":group_id,
        'message': comment,
        "attachments": f"photo{owner_id}_{photo_id}",
        "from_group":1
    }
    response = requests.post(url, params=params)
    response.raise_for_status()


def delete_files():
    filelist = listdir("images")
    for f in filelist:
        os.remove(os.path.join("images", f))


def main():
    Path("images").mkdir(parents=True, exist_ok=True)
    dotenv.load_dotenv()
    token_vk = os.getenv('VK_TOKEN')
    user_id = os.getenv('USER_ID')
    group_id = os.getenv('GROUP_ID')
    comment, filename, image_links = get_xkcd()
    save_images(image_links, filename)
    photo, hash, server = file_upload_vk(token_vk, filename)
    owner_id, photo_id = save_file_vk(token_vk, photo, hash, server, user_id)
    publish_image_vk(comment, token_vk, photo_id, owner_id, group_id)
    delete_files()


if __name__ == "__main__":
    main()