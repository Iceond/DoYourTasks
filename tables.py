from sqlalchemy import create_engine,INTEGER,VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, sessionmaker
import datetime
Base = declarative_base()
DATABASE_URL = "sqlite:///identifier.sqlite"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Tasks(Base):
    __tablename__ = 'tasks'
    Id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    taskname: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    description: Mapped[str] = mapped_column(VARCHAR(200))
    user_id: Mapped[int] = mapped_column(INTEGER,ForeignKey('users.ID'))
    category_id: Mapped[int] = mapped_column(INTEGER, ForeignKey('categories.id'))
    priority_id: Mapped[int] = mapped_column(INTEGER,ForeignKey("priorities.id"))
    due_date: Mapped[datetime.datetime] = mapped_column(VARCHAR(50), nullable=False)

    def __repr__(self):
        return f"{self.taskname} | {self.description} | {self.category_id} | {self.priority_id} | {self.due_date}"

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Category: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

class Priority(Base):
    __tablename__ = 'priorities'
    id : Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Priority: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

def Create_Task(name,description,category,priority,due_date):
    try:
        order =  1 if len(session.query(Tasks).all()) +1 < 2 else len(session.query(Tasks).all()) + 1
        new_task = Tasks(Id=order,taskname=name,description=description,category_id=category ,priority_id=priority,due_date=due_date,user_id=1)
        session.add(new_task)
        session.commit()
    except Exception as exc:
        print(f"Error:{exc} has occured")
        session.rollback()

class User(Base):
    __tablename__ = 'users'
    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Username: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

def Drop_Task(id:int):
    try:
        session.query(Tasks).get(int(id))
        session.query(Tasks).delete(synchronize_session=False)
        session.commit()
    except Exception as exc:
        print(f"Error:{exc} has occured")


def Get_Category():
    try:
        categ =  session.query(Category).all()
        categories = []
        for e in categ:
            categories.append(e.Category)
        return categories
    except Exception as exc:
        print(f"Error:{exc} has occured")
        return ["Unavailable"]
def getcategorybyid(id):
    try:
        categ = session.query(Category).get(id)
        return categ
    except Exception as exc:
        print(exc)
def get_Priority():
    try:

        val = session.query(Priority).all()
        priorities = []
        for i in val:
            priorities.append(i.Priority)
        return priorities
    except Exception as exc:
        print(exc)
        return ["Unavailable"]
