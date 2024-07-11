from datetime import datetime
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request
from app.models.missions import Missions
from app.utils.mission_utils import MissionUtils

# 'mapeador' de dados no corpo da requisição
mission_args = RequestParser()
mission_args.add_argument('name', type=str)
mission_args.add_argument('launch_date', type=str)
mission_args.add_argument('return_date', type=str)
mission_args.add_argument('destination', type=str)
mission_args.add_argument('status', type=str)
mission_args.add_argument('crew', type=str)
mission_args.add_argument('payload', type=str)
mission_args.add_argument('cost', type=float)
mission_args.add_argument('status_details', type=str)

# endpoint para obter todas as missões
class GetAllMissions(Resource):
  def get(self):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
      try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
      except:
        return { 'message': 'The start date and end date must be in the format yyyy-mm-dd' }, 400
      if start_date > end_date:
        return { 'message': 'The end date must be greater than the start date' }, 400
    missions = Missions.getAll(start_date, end_date)
    return [MissionUtils.convert_mission_to_resumed_dict(mission) for mission in missions]

# endpoint para obter missão
class GetMission(Resource):
  def get(self, id):
    try:
      mission = Missions.get(id)
    except:
      return { 'message': 'Mission not found!' }, 404
    return MissionUtils.convert_mission_to_dict(mission)

# endpoint para criar missão
class CreateMission(Resource):
  def post(self):
    try:
      data = MissionUtils.validate_mission(mission_args.parse_args())
    except Exception:
      return { 'message': 'Mission invalid!' }, 400
    mission = Missions(data)
    try:
      mission.save()
    except:
      return { 'message': 'The mission could not be saved'}, 500
    return MissionUtils.convert_mission_to_dict(mission), 200

# endpoint para atualizar missão
class UpdateMission(Resource):
  def put(self, id):
    try:
      data = MissionUtils.validate_mission(mission_args.parse_args())
    except:
      return { 'message': 'Mission invalid!' }, 400
    try:
      mission = Missions.get(id)
    except:
      return { 'message': 'Mission not found!' }, 404
    data = Missions(data)
    try:
      mission.update(data)
    except:
      return { 'message': 'The mission could not be updated' }, 500
    return MissionUtils.convert_mission_to_dict(mission), 200  

# endpoint para deletar missão
class DeleteMission(Resource):
  def delete(self, id):
    try:
      mission = Missions.get(id)
    except:
      return { 'message': 'Mission not found!' }, 404
    try:
      mission.delete()
    except:
      return { 'message': 'The mission could not be deleted' }, 500
    return { 'message': 'Mission deleted successfully!' }, 200  
