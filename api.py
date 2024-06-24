from fastapi import FastAPI
import requests
import env
from fastapi.responses import RedirectResponse
from role_mapping import hash_to_role_map


app = FastAPI()

API_ENDPOINT = 'link_api_discord'

CLIENT_ID = env.CLIENT_ID
CLIENT_SECRET = env.SECRET
REDIRECT_URI = env.REDIRECT_URI
BOT_TOKEN = env.BOT_TOKEN
GUILD_ID = env.GUILD_ID

def get_token(code: str, starter_id: int):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI.format(starter_id),
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(f'{API_ENDPOINT}/oauth2/token', data=data, headers=headers)
    if r.status_code != 200:
        return False

    response = r.json()
    return response.get('access_token', False)

def join_server(token: str, user_id: str, role_id: str):
    data = {
        'access_token': token,
        'roles': [role_id,],
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bot {BOT_TOKEN}',
    }
    req = requests.put(f'{API_ENDPOINT}/guilds/{GUILD_ID}/members/{user_id}', json=data, headers=headers)
    return req.status_code in (201, 204)

def get_member(token: str):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    req = requests.get(f'{API_ENDPOINT}/users/@me', headers=headers)
    if req.status_code != 200:
        return False
    # return req.json().get('id', False)
    return req.json()

def error_response():
    return {"error": f"entre em contato com o suporte"}

def save_to_csv(member):
    csv = open('result.csv', 'a+')

    id = member.get('id')
    email = member.get('email')
    username = member.get('username')
    csv.write(f'{id},{email},{username}\n')

    csv.close()

def join_and_asign_role(starter_id: str, code: int):
    token = get_token(code, starter_id)
    if not token:
        return False

    role_id = hash_to_role_map.get(str(starter_id), False)
    if not role_id:
        return False
    
    member = get_member(token)
    if not member:
        return False
    id = member.get('id', False)
    username = member.get('username', False)

    print("user: ", username)
    print("id: ", id)
    print("entrando no servidor...")

    result = join_server(token, member.get('id', False), role_id)
    if not result:
        return False

    save_to_csv(member)

    return True

@app.get("/join/{starter_id}")
def join(starter_id: int, code: str):
    result = join_and_asign_role(starter_id, code)
    if not result:
        return error_response()

    return RedirectResponse(f"https://discord.com/channels/{GUILD_ID}")
