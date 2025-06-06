from typing import Type

from sqlalchemy import create_engine, func, select, desc
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional

from sqlalchemy import Integer, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import inspect


class Base(DeclarativeBase):
    def to_dict(self):
        inspector = inspect(self.__class__)
        result = {}
        for column in getattr(inspector, "attrs"):
            key = column.key
            value = getattr(self, key)
            # 处理关联对象（如 relationship）
            if hasattr(column, 'property') and column.property.uselist:
                result[key] = [item.to_dict() for item in value]  # 递归处理
            else:
                result[key] = value
        return result

    def model_from_dict(self, data_dict: dict):
        inspector = inspect(self.__class__)
        columns = [c.key for c in inspector.attrs]
        filtered = {k: v for k, v in data_dict.items() if k in columns}

        instance = self.__class__(**filtered)
        return instance


class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False)

    message_id: Mapped[str] = mapped_column(Text, unique=True, index=True)
    message_name: Mapped[Optional[str]] = mapped_column(Text)
    message_type: Mapped[Optional[str]] = mapped_column(Text)
    message_data: Mapped[Optional[str]] = mapped_column(Text)
    message_status: Mapped[Optional[str]] = mapped_column(Text, default='okay')

    event_data: Mapped[Optional[str]] = mapped_column(Text)
    describe: Mapped[Optional[str]] = mapped_column(Text)
    tag: Mapped[Optional[str]] = mapped_column(Text)
    resource_type: Mapped[Optional[str]] = mapped_column(Text, default='mqtt')

    create_time: Mapped[Optional[str]] = mapped_column(Text)
    expire_time: Mapped[Optional[str]] = mapped_column(Text)
    modify_time: Mapped[Optional[str]] = mapped_column(Text)

    create_by: Mapped[Optional[str]] = mapped_column(Text, default='sys')
    create_at: Mapped[Optional[str]] = mapped_column(Text, server_default=text('CURRENT_TIMESTAMP'))
    modify_by: Mapped[Optional[str]] = mapped_column(Text, default='sys')
    modify_at: Mapped[Optional[str]] = mapped_column(Text, server_default=text('CURRENT_TIMESTAMP'))


class Config(Base):
    __tablename__ = 'config'
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, nullable=False)
    config_id: Mapped[str] = mapped_column(Text, unique=True, index=True)
    config_name: Mapped[Optional[str]] = mapped_column(Text)
    config_data: Mapped[Optional[str]] = mapped_column(Text)
    config_status: Mapped[Optional[str]] = mapped_column(Text, default='ok')

    create_by: Mapped[Optional[str]] = mapped_column(Text, default='sys')
    create_at: Mapped[Optional[str]] = mapped_column(Text, server_default=text('CURRENT_TIMESTAMP'))
    modify_by: Mapped[Optional[str]] = mapped_column(Text, default='sys')
    modify_at: Mapped[Optional[str]] = mapped_column(Text, server_default=text('CURRENT_TIMESTAMP'))


class DBBase:
    def __init__(self, db_engine: str = "sqlite:///db/open-day.db", echo: bool = False):
        self.engine = create_engine(db_engine, echo=echo)

    def save_messages(self, ins: Message):
        session: Session = sessionmaker(bind=self.engine)()
        instance = session.query(Message).filter_by(
            message_id=ins.message_id).first()
        if instance:
            instance.tag = ins.tag
        else:
            session.add(ins)

        session.commit()

    def upsert_config(self, data: Config):
        session: Session = sessionmaker(bind=self.engine)()
        instance = session.query(Config).filter_by(
            config_id=data.config_id).first()
        if instance:
            instance.config_name = data.config_name
            instance.config_data = data.config_data
            instance.config_status = data.config_status
        else:
            session.add(data)
        session.commit()

    def filter_by_dict(self, model: Type[Base], filter_dict: dict, limit: int = 10) -> list:
        session: Session = sessionmaker(bind=self.engine)()
        query = select(model)
        if filter_dict:
            for key, value in filter_dict.items():
                query = query.filter(getattr(model, key) == value)
        query = query.order_by(desc(getattr(model, "id")))
        query = query.limit(limit)
        data = [r.to_dict() for r in session.scalars(query).all()]
        return data

    @staticmethod
    def get_max_value(session: Session, table: Type[Base], column):
        stmt = select(func.max(getattr(table, column)))
        result = session.execute(stmt)
        return result.scalar()

    def init_db(self, clear_table: bool = False):
        if clear_table:
            Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)


class DBSqlite3(DBBase):
    def __init__(self, db_path: str = "db/open-day.db"):
        super().__init__(db_engine=f'sqlite:///{db_path}')
