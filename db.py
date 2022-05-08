from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_NAME = 'bot.sqlite'

engine = create_engine(f"sqlite:///{DATABASE_NAME}")
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Button(Base):
    __tablename__ = 'Кнопки'
    id = Column(Integer, primary_key=True)
    button_text = Column(String(50))
    button_link = Column(String(50))


class Admins(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    client_id = Column(String, ForeignKey('clients.id'))


class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    first_name = Column(String(100), nullable=True)
    username = Column(String(50), nullable=True)
    admin = relationship('Admins', backref='clients')


def create_db():
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()


def check_existing(id):
    session = Session()
    result = session.query(Clients.chat_id).filter(Clients.chat_id == id).all()
    return result


def check_existing_admin(id):
    session = Session()
    result = session.query(Admins.client_id).filter(Admins.client_id == id).all()
    return result


def add_user(id, first_name, username, ):
    session = Session()
    exist = check_existing(id)
    if not exist:
        user = Clients(chat_id=id,
                       first_name=first_name,
                       username=username, )
        session.add(user)
    session.commit()
    session.close()


def add_admin(id):
    session = Session()
    exist = check_existing_admin(id)
    if not exist:
        admin = Admins(client_id=id)
        session.add(admin)
    session.commit()
    session.close()


def add_button(text, link):
    session = Session()
    add_btn = Button(button_text=text, button_link=link)
    session.add(add_btn)
    session.commit()
    session.close()


def get_buttons():
    session = Session()
    return session.query(Button).all()


if __name__ == '__main__':
    create_db()
