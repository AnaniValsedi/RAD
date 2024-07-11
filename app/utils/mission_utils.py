from marshmallow import Schema, fields, validate, ValidationError

# classe que possui métodos de ajuda para manipular as missões
class MissionUtils:
  # método estático que converte classe para dicionário
  @staticmethod
  def convert_mission_to_dict(mission):
    return {
      'id': mission.id,
      'name': mission.name,
      'launch_date': mission.launch_date.strftime('%Y-%m-%d'),
      'destination': mission.destination,
      'status': mission.status,
      'crew': mission.crew,
      'payload': mission.payload,
      'duration': f'{mission.duration.days} days',
      'cost': float(mission.cost),
      'status_details': mission.status_details
    }

  # método estático que converte classe para dicionário com menos informações
  @staticmethod
  def convert_mission_to_resumed_dict(mission):
    return {
      'id': mission.id,
      'name': mission.name,
      'launch_date': mission.launch_date.strftime('%Y-%m-%d'),
      'destination': mission.destination,
      'status': mission.status
    }

  # método estático que converte classe para linha do banco de dados
  @staticmethod
  def convert_mission_to_row(mission):
    return {
      'name': mission.name,
      'launch_date': mission.launch_date,
      'destination': mission.destination,
      'status': mission.status,
      'crew': mission.crew,
      'payload': mission.payload,
      'duration': mission.duration,
      'cost': mission.cost,
      'status_details': mission.status_details
    }

  # método estático que valida missão
  @staticmethod
  def validate_mission(mission):
    string_field = fields.String(validate=validate.Length(min=1))
    MissionSchema = Schema.from_dict({
      'name': string_field,
      'launch_date': fields.Date('%Y-%m-%d'),
      'return_date': fields.Date('%Y-%m-%d'),
      'destination': string_field,
      'status': string_field,
      'crew': string_field,
      'payload': string_field,
      'cost': fields.Decimal(2),
      'status_details': string_field,
    })()
    mission = MissionSchema.load(mission)
    if mission['launch_date'] > mission['return_date']:
      raise ValidationError('The return date must be greater than the launch date')
    if mission['status'] not in { 'ACTIVE', 'COMPLETED', 'ABORTED' }:
      raise ValidationError('The status must be ACTIVE, COMPLETED or ABORTED')
    if mission['cost'] <= 0:
      raise ValidationError('The cost must be greater than 0')
    return mission
