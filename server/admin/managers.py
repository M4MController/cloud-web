import typing

from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from server.database.managers import BaseSqlManager

from server.database.models import Sensor, Controller, Object, User, Company, UserInfo


class UsersManager(BaseSqlManager):
	model = User

	def get_by_company_id(self, company_id) -> typing.List[User]:
		return self.session.query(UserInfo). \
			options(joinedload(UserInfo.user)
					.joinedload(User.objects)
					.joinedload(Object.controllers)
					.joinedload(Controller.sensors)
					.joinedload(Sensor.company)
			).filter(Company.id == company_id).all()


class SensorsManager(BaseSqlManager):
	model = Sensor

	def get_rows(self):
		return self.session.query(Sensor) \
			.options(joinedload(self.model.controller).joinedload(Controller.object).joinedload(Object.user)) \
			.all()

	def get_sensor(self, sensor_id: str):
		return self.session.query(self.model)\
			.options(joinedload(self.model.controller)
					.joinedload(Controller.object)
					.joinedload(Object.user)
					.joinedload(User.social_tokens)).filter(self.model.id == sensor_id).all()

	def get_for_company(self, company_id: int, user_id: int):
		return self.session.query(self.model) \
			.options(joinedload(self.model.controller).joinedload(Controller.object).joinedload(Object.user)) \
			.filter(and_(Company.id == company_id, User.id == user_id)) \
			.all()


class CompaniesManager(BaseSqlManager):
	model = Company

	def get_all(self):
		return self.session.query(self.model).all()
