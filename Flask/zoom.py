import os
# from dotenv import load_dotenv
# load_dotenv()

# token = os.environ.get("api-token")

API_KEY = "1EeAHGggTyic4EEBCLMOfA"
API_SEC = "V6vAw22LHuLJdlEVTSBotlOyYL298vjTwIQM"


import http.client

def get_email():
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = {
        'authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjFFZUFIR2dnVHlpYzRFRUJDTE1PZkEiLCJleHAiOjE2NDY4MTM2NDMsImlhdCI6MTY0NjIwODg0MH0.M15RMgia4A5WVtZBYtM9r7dLeTmxvbpiV4M7auiPVhE",
        'content-type': "application/json"
        }
    conn.request("GET", "/v2/users?status=active&page_size=30&page_number=1", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    print(data)

    data = data.replace('\'', '')
    data = data.replace('{', '')
    data = data.replace('\"', '')
    data = data.split(',')

    email = [match for match in data if "email" in match][0].removeprefix('email:')

    return email

get_email()