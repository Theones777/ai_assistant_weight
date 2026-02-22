from sqlalchemy import (
    Column, BigInteger, Integer, String, Text,
    ForeignKey, TIMESTAMP, func, Index
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    requests = relationship(
        "UserRequest",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class UserRequest(Base):
    __tablename__ = "user_requests"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    request_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="requests")

    __table_args__ = (
        Index(
            "idx_user_requests_user_id_timestamp_desc",
            "user_id",
            timestamp.desc()
        ),
    )
