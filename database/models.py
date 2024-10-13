from sqlalchemy import BigInteger, ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    house: Mapped[int] = mapped_column(Integer)
    doorway: Mapped[int] = mapped_column(Integer)
    stage: Mapped[int] = mapped_column(Integer)
    flat: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String, default='')
    phone: Mapped[str] = mapped_column(String, default='')
    auto1: Mapped[str] = mapped_column(String, default='')
    auto2: Mapped[str] = mapped_column(String, default='')


class GuideNews(Base):
    __tablename__='guide_news'
    id: Mapped[int] = mapped_column(primary_key=True) # может быть только две строки: "1" и "2"
    name_line: Mapped[str] = mapped_column(String) # может быть только две строки: "guide" и "news"
    text: Mapped[str] = mapped_column(String)
    photo: Mapped[str] = mapped_column(String)

class IdGroup(Base):
    __tablename__='id_group'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_group: Mapped[int] = mapped_column(Integer)



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
