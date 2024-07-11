from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_restful import Api 
from flask_cors import CORS

# instancia app, api e habilita CORS
app = Flask(__name__)
api = Api(app)
CORS(app)

# configura banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)

from app.models.missions import Missions

# cria tabelas
with app.app_context():
  db.create_all()

from app.controllers.mission_controller import GetAllMissions, GetMission, CreateMission, UpdateMission, DeleteMission

# prepara rotas da API
api.add_resource(GetAllMissions, '/api/missions')
api.add_resource(GetMission, '/api/missions/<int:id>')
api.add_resource(CreateMission, '/api/missions')
api.add_resource(UpdateMission, '/api/missions/<int:id>')
api.add_resource(DeleteMission, '/api/missions/<int:id>')
