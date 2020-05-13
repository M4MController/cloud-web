from datetime import datetime

from flask import request

import m4m_sync
from m4m_sync import AesStreamWrapper
from m4m_sync.utils import StreamWrapper

from server.resources.base import BaseResource
from server.resources.utils import provide_db_session, schematic_response

from server.admin.schemas import SensorResponse, CompanyResponse
from server.admin.managers import SensorsManager, CompaniesManager


class SensorsResource(BaseResource):
	@provide_db_session
	@schematic_response(SensorResponse(many=True))
	def get(self):
		rows = SensorsManager(self.db_session).get_rows()

		return [{
			'sensor_id': data.id,
			'email': data.controller.object.user.login,
			'name': '{object} / {controller} / {sensor}'.format(
				object=data.controller.object.name,
				controller=data.controller.name,
				sensor=data.name,
			)
		} for data in rows]


class SensorsDataResource(BaseResource):
	@provide_db_session
	def get(self, sensor_id: str, year: int, month: int, day: int):
		key = request.args.get('key')
		data = SensorsManager(self.db_session).get_sensor(sensor_id)

		if not len(data):
			return 404

		sensor = data[0]
		token = sensor.controller.object.user.social_tokens.yandex_disk
		if not token:
			return 403

		store = m4m_sync.YaDiskStore(token=token)
		data = store.get(
			m4m_sync.stores.Sensor(id=sensor_id, controller=m4m_sync.stores.Controller(mac=sensor.controller.mac)),
			stream_wrapper=AesStreamWrapper(key=key) if key else StreamWrapper(),
			range=m4m_sync.stores.DateTimeRange.day(datetime(year=year, month=month, day=day))
		)

		if not len(data):
			return '', 404
		return data[0], 200


class CompaniesResource(BaseResource):
	@provide_db_session
	@schematic_response(CompanyResponse(many=True))
	def get(self):
		return CompaniesManager(self.db_session).get_all()


class CompanySensorsResource(BaseResource):
	@provide_db_session
	@schematic_response(SensorResponse(many=True))
	def get(self, company_id: int):
		return SensorsManager(self.db_session).get_by_company(company_id)


def register_routes(app):
	app.register_route(SensorsResource, 'admin_sensors', '/admin/sensors')
	app.register_route(SensorsDataResource, 'admin_sensors_data', '/admin/sensors/<string:sensor_id>/<int:year>/<int:month>/<int:day>')
	app.register_route(CompanySensorsResource, 'admin_sensors_for_company', '/admin/sensors/<int:company_id>')
	app.register_route(CompaniesResource, 'admin_companies', '/admin/companies')
