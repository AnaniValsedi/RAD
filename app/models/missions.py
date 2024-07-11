from datetime import datetime
from sqlalchemy import desc
from app import db
from app.utils.mission_utils import MissionUtils

# classe que simula tabela no banco de dados
class Missions(db.Model):
  # metadados da tabela
  __tablename__ = 'mission'
  __table_args__ = {'sqlite_autoincrement': True} 

  # atributos
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  launch_date = db.Column(db.Date)
  destination = db.Column(db.String)
  status = db.Column(db.String)
  crew = db.Column(db.String)
  payload = db.Column(db.String)
  duration = db.Column(db.Interval)
  cost = db.Column(db.DECIMAL)
  status_details = db.Column(db.Text)

  # construtor
  def __init__(self, data):
    self.id = data.get('id')
    self.name = data.get('name')
    self.launch_date = data.get('launch_date')
    self.destination = data.get('destination')
    self.status = data.get('status')
    self.crew = data.get('crew')
    self.payload = data.get('payload')
    self.duration = data.get('return_date') - data.get('launch_date')
    self.cost = data.get('cost')
    self.status_details = data.get('status_details')

  # método estático de buscar todas as missões
  @staticmethod
  def getAll(start_date=None, end_date=None):
    query = Missions.query
    if start_date and end_date:
      query = query.filter(Missions.launch_date.between(start_date, end_date))
    return query.order_by(desc(Missions.launch_date)).all()

  # método estático de buscar missão pelo ID
  @staticmethod
  def get(id):
    mission = Missions.query.get(id)
    if mission == None:
      raise ValueError('Mission not found!')
    return mission
   
  # método estático de salvar missão
  def save(self):
    db.session.add(self) 
    db.session.commit()

  # método estático de atualizar missão
  def update(self, mission):
    db.session.query(Missions).filter(Missions.id==self.id).update(MissionUtils.convert_mission_to_row(mission))
    db.session.commit()

  # método estático de deletar missão
  def delete(self):
    db.session.query(Missions).filter(Missions.id==self.id).delete()
    db.session.commit()
