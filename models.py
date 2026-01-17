from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Service(Base):
    __tablename__ = "services"

    name = Column(String, primary_key=True, index=True)
    url = Column(String, nullable=False)
    version = Column(String, nullable=False)
    health_endpoint = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return{
            "name": self.name,
            "url": self.url,
            "version": self.version,
            "health_endpoint": self.health_endpoint,
            "registered_at": self.registered_at.isoformat() \
            if self.registered_at else None

        }