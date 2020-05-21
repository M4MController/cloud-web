import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from server.database.managers import UserSocialTokensManager
from server.database.models import (
    UserSocialTokens,
)

from config import config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    session = Session(create_engine(config['database']['objects']['uri']))
    user_social_tokens_manager = UserSocialTokensManager(session)

    user_tokens = session.query(UserSocialTokens).all()

    for user_token in user_tokens:
        try:
            user_social_tokens_manager.sync_user(user_token)
            session.commit()
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    main()
