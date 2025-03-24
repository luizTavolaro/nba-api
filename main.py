from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
# CORS(app, origins=["http://localhost:3000"])

API_HOST = "api-nba-v1.p.rapidapi.com"
API_KEY = "f1cd865500msh13db90aff14e6ecp138027jsn5a456d9d09fc"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

def getTeams():
    url = f"https://{API_HOST}/teams"
    response = requests.get(url, headers=HEADERS)
    return response.json().get('response', [])

@app.route('/teams', methods=['GET'])
def teams():
    return jsonify(getTeams())

def getStandingsByTeamId(teamId):
    url = f"https://{API_HOST}/standings"
    params = {"league": "standard", "season": "2021", "team": teamId}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json().get('response', [])

    if not data:
        return {"error": "Time não encontrado"}

    return {
        'teamId': data[0]['team']['id'],
        'teamName': data[0]['team']['name'],
        'teamLogo': data[0]['team']['logo'],
        'teamWins': data[0]['win']['total'],
        'teamLosses': data[0]['loss']['total'],
        'teamGames': data[0]['win']['total'] + data[0]['loss']['total']
    }


@app.route('/standings/<int:team_id>', methods=['GET'])
def standings(team_id):
    return jsonify(getStandingsByTeamId(team_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
