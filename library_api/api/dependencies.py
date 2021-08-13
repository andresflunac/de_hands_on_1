from library_api.db.session import db_session


def get_db_session():
    try:
        print('trying to connect ...')
        session = db_session()
        print('connection established')
        yield session
    finally:
        print('connection closed')
        session.close()
