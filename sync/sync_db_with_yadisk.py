import logging
import sys

import m4m_sync

from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, Session

from server.database.models import (
    Object,
    Controller,
    Sensor,
    UserSocialTokens,
)

from config import config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    session = Session(create_engine(config['database']['objects']['uri']))

    user_tokens = session.query(UserSocialTokens).filter(UserSocialTokens.yandex_disk != None).all()

    for user_token in user_tokens:
        if not user_token.yandex_disk:
            continue

        try:
            store = m4m_sync.YaDiskStore(token=user_token.yandex_disk)
            remote_controllers = store.get_controllers()
            local_controllers = session.query(Controller).options(joinedload(Controller.object)).filter(
                Object.user_id == user_token.user_id).all()

            local_controllers_macs = [local_controller.mac for local_controller in local_controllers]

            for remote_controller in remote_controllers:
                if remote_controller.mac in local_controllers_macs:
                    local_controller = next(filter(lambda x: x.mac == remote_controller.mac, local_controllers))
                    if local_controller.name != remote_controller.name:
                        local_controller.name = remote_controller.name
                else:
                    object_id, = session.query(Object.id).filter_by(user_id=user_token.user_id).first()
                    local_controller = Controller(
                        name=remote_controller.name,
                        mac=remote_controller.mac,
                        object_id=object_id,
                    )
                    session.add(local_controller)

                remote_sensors = store.get_sensors(remote_controller)
                local_sensors = session.query(Sensor).filter_by(controller_id=local_controller.id)

                local_sensor_ids = [local_sensor.id for local_sensor in local_sensors]

                for remote_sensor in remote_sensors:
                    if remote_sensor.id in local_sensor_ids:
                        local_sensor = next(filter(lambda x: x.id == remote_sensor.id, local_sensors))
                        if local_sensor.name != remote_sensor.name:
                            local_sensor.name = remote_sensor.name
                    else:
                        local_sensor = Sensor(
                            name=remote_sensor.name,
                            id=remote_sensor.id,
                            controller_id=local_controller.id,
                        )
                        session.add(local_sensor)

            session.commit()

        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    main()
