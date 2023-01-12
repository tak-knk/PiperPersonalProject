import requests

def main():
    send_notify('トイレできたよ！！！')

def send_notify(message):
    token = 'AAAAAAAAAAAAAAAAAA0'
    api_url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': message}
    requests.post(api_url, headers = headers, data = data)

if __name__ == '__main__':
    main()
