import json

from bson import json_util
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
#from Utils import InitUtil as IU
from bson import json_util




from Server.Database.connection import InitMongo
from Server.Database.dataBase import DataBase
from Server.Simulator.OpenAISimulator import OpenAISimulator
from Server.Utils.Voice import Voice

app = Flask(__name__)
CORS(app)

def get_client_agent_strongs(db):
    agent = db.get_agent("NglT4UH7dzTYD6EEmW64NvzKQZ82")
    agent_skills = agent.skills
    client_skills = db.get_client_skills_yuval()

    client_personals = client_skills[0]
    client_emotions = client_skills[1]
    return agent_skills, client_personals, client_emotions

def load_config_file(config_path):
    # Load the configuration from the JSON file
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


@app.route('/')
def home():
    return jsonify({'message': 'Hello from Flask server!'})

# @app.route('/api/users/<id>', methods=['GET'])
# def login(id):



@app.route('/api/data', methods=['GET'])
def get_data():
    # Perform any necessary operations or retrieve data from a database
    data = {'data': [1, 2, 3, 4, 5]}
    return jsonify(data)


@app.route('/api/skills_fill', methods=['GET'])
def get_skills_to_fill():
    # Perform any necessary operations or retrieve data from a database
    skills = db.get_client_skills()
    # Convert ObjectId to string
    skills = json.loads(json_util.dumps(skills))
    print(skills)
    return jsonify(skills)

 #jsonify(agent)
@app.route('/api/get_agent', methods=['GET'])
def get_agent():
    agent_id = request.args.get('agent_id')  # get agent_id from the query string
    agent = db.get_login(agent_id)
    agent = json.loads(json_util.dumps(agent))
    return jsonify(agent)

@app.route('/api/skills_template', methods=['GET'])
def get_skills_template():
    # Perform any necessary operations or retrieve data from a database
    skills = db.get_template_sim()
    # Convert ObjectId to string
    skills = json.loads(json_util.dumps(skills))
    return jsonify(skills)

@app.route('/api/get_review', methods=['GET'])
def get_review():
    result = simulator.review_simulation(simulation_id)
    return jsonify(result)

@app.route('/api/transcription_exchange', methods=['POST'])
def post_transcription():
    # Retrieve the string from the client request
    string_from_client = request.json.get('transcript')
    # Perform any necessary operations or retrieve data from a database

    #################################
    # if string_from_client == "review":
    #     result = simulator.review_simulation(simulation_id)
    #     return result
    # else:
    result, emotion = simulator.generate_answer(simulation_id, string_from_client)
    if emotion not in emotions_models:
        emotion = "NATURAL"

    voice.generate_emotional_speech(result, emotions_models[emotion], "audio/curr_speech_file.wav")
    print(result)
    return send_file("audio/curr_speech_file.wav", mimetype='audio/x-wav')
    ############################


# company_description, emotions, personality, call_subject
@app.route('/api/situation_description', methods=['POST'])
def get_company_description():
    emotions = request.json.get('emotions')
    personality = request.json.get('personality')
    situation_description = request.json.get('situation_description')
    global simulation_id
    simulation_id = simulator.start_simulation(config["CompanyInfo"], emotions,
                                               personality,
                                               situation_description)
    return ""

if __name__ == '__main__':
    simulation_id = None

    db_connection = InitMongo()
    db = DataBase(db_connection)
    config = load_config_file("configuration.json")
    local_config = load_config_file("local_conf.json")
    voice_config = load_config_file("Utils/config_voice.json")
    emotions_models = voice_config["emotions_models"]

    simulator = OpenAISimulator()

    voice = Voice(local_config)
    #res = IU.InitUtil.matching_customer(simulator.model_engine,db)

    app.run(debug=True)
