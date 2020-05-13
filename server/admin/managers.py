from sqlalchemy.orm import joinedload

from server.database.managers import BaseSqlManager

from server.database.models import Sensor, Controller, Object, User, Company


class SensorsManager(BaseSqlManager):
	model = Sensor

	def get_rows(self):
		self.session.query(Sensor) \
			.options(joinedload(self.model.controller).joinedload(Controller.object).joinedload(Object.user)) \
			.all()

	def get_sensor(self, sensor_id: str):
		return self.session.query(self.model)\
			.options(joinedload(self.model.controller)
					.joinedload(Controller.object)
					.joinedload(Object.user)
					.joinedload(User.social_tokens)).filter(self.model.id == sensor_id).all()

	def get_by_company(self, company_id: int):
		return self.session.query(self.model)\
			.filter_by(company_id=company_id)\
			.all()


class CompaniesManager(BaseSqlManager):
	model = Company

	def get_all(self):
		return self.session.query(self.model).all()
