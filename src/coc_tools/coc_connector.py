import requests
import json
from os import getenv
import jmespath as jq

BASE_URL = "https://www.codingame.com/services"


class CoC:
    def __init__(self):
        self.session = requests.Session()
        self.uid = self.login()

    def login(self):
        uri = f"{BASE_URL}/Codingamer/loginSiteV2"

        email = getenv("COC_EMAIL")
        password = getenv("COC_PASSWORD")
        payload = [email, password, True]

        response = self._post(uri, payload)
        uid = jq.search('codinGamer.userId', response)

        return uid

    def create_match(self):
        raise NotImplemented

    def start_match(self):
        raise NotImplemented

    def get_game_stats(self, match_id):
        uri = f"{BASE_URL}/ClashOfCode/findClashReportInfoByHandle"
        payload = [match_id]

        response = self._post(uri, payload)
        query = """
        {
            started: started,
            test_id: players[0].testSessionHandle,
            finished: finished,
            mode: mode,
            start_time: startTime,
            players: players[].{
                id: codingamerId, 
                name: codingamerNickname, 
                avatar: codingamerAvatarId,
                status: testSessionStatus,
                language: languageId,
                score: score,
                rank: rank,
                duration: duration, 
                chars: criterion
            }
        }
        """
        payload = jq.search(query, response)
        return {"_id": match_id, **payload}

    def get_test(self, match_id):
        uri = f"{BASE_URL}/TestSession/startTestSession"
        payload = [match_id]
        response = self._post(uri, payload)
        print(response)
        return response

    def _post(self, uri, payload=[]):
        response = self.session.post(uri, json=payload)

        if response.status_code != 200:
            raise CocError(response.json())

        return response.json()


class CocError(Exception):
    def __init__(self, *args):
        if args:
            resp = args[0]
            self.message = resp.get("message", json.dumps(resp))
        else:
            self.message = "Could not connect to COC"

    def __message__(self):
        if self.message:
            return f"CoC Error: {self.message}"
        else:
            return "CoC Error"
