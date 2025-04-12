import os
from dotenv import load_dotenv
import base64
import hashlib
import secrets
import webbrowser
from urllib.parse import urlencode
import requests

load_dotenv()


# 認証情報
client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")
redirect_uri = "http://localhost:8080/callback"
authorize_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
api_url = "https://api.twitter.com/2/tweets"
scope = "users.read tweet.read offline.access tweet.write"

# PKCE用コードを生成
code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b"=").decode("utf-8")
print("PKCE用コード")
print(f"- challenge: {code_challenge}")
print(f"- verifier : {code_verifier}")

# Authorizationヘッダ用コードを生成
auth_value = f"{client_id}:{client_secret}"
auth_header = base64.b64encode(auth_value.encode()).decode()
auth_header_text = f"Basic {auth_header}"
print("Authorizationヘッダ用コード")
print(f"- Authorization: {auth_header_text}")



def authorize():
    # 認可URL作成
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "scope": scope,
        "state": "1234567890"
    }
    url = f"{authorize_url}?{urlencode(params)}"

    # ブラウザで開く
    webbrowser.open(url)
    print("このURLをブラウザで開き、リダイレクト先のURLからcodeをコピーしてください")



def get_token(auth_code):

    # ヘッダ
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": auth_header_text
    }
    print(headers)

    # トークン取得
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": code_verifier
    }

    response = requests.post(token_url, data=data, headers=headers)
    tokens = response.json()

    print(tokens)
    print("Access Token:", tokens.get("access_token"))
    return tokens


def get_refreshed_token(refresh_token):
    # ヘッダ
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": auth_header_text
    }
    print(headers)

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        #"client_id": client_id,
        "code_verifier": code_verifier,
        #"client_secret": client_secret
    }

    response = requests.post(token_url, data=data, headers=headers)
    tokens = response.json()

    print(tokens)
    print("Access Token:", tokens.get("access_token"))
    return tokens



# サンプル呼び出し
def call_api(access_token, tweet_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    cur_url = f"{api_url}/{tweet_id}?tweet.fields=public_metrics"
    response = requests.get(cur_url, headers=headers)
    print(response.json())

    return response.json()



def main():
    access_token = None
    refresh_token = None

    if access_token is None:
        # 認証
        print("--------------------------------")
        print("認証")
        authorize()

        # 手動でブラウザでログインした後、リダイレクトURLからcodeを取得
        auth_code = input("Enter the authorization code: ")
        
        tokens = get_token(auth_code)
        #print("INFO: access_token:", tokens.get("access_token"))
        if tokens.get("access_token") is None:
            print("ERROR: access_token is None")
            exit()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        print("--------------------------------")

    # API呼び出し(サンプル)
    print("--------------------------------")
    print("API呼び出し(サンプル)") 
    tweet_id = "1866319451081306620"    # sample tweet id
    response_json = call_api(tokens.get("access_token"), tweet_id)

    # responseで、tokenがexpiredだった場合は、refresh_tokenを使用して新しいtokenを取得する
    if response_json.get("errors") is not None and response_json.get("errors")[0].get("code") == 89:
        print("ERROR: token is expired")
        
        # トークン更新
        print("--------------------------------")
        print("トークン更新")
        tokens = get_refreshed_token(refresh_token)
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        print("--------------------------------")

        # 再実行
        print("--------------------------------")
        print("再実行")
        response_json = call_api(access_token, tweet_id)



if __name__ == "__main__":
    main()

    ## リフレッシュトークンの発行のみ
    #refresh_token = "(latest refresh token)"
    #tokens = get_refreshed_token(refresh_token)
    #print(tokens)

    pass
