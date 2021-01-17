import csv
from dataclasses import dataclass
import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, Float
from database import create_db, create_tables, setup_mysql_engine_default
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()


@dataclass
class User(Base):
    __tablename__ = 'users'

    # Serialize object to JSON
    id: int
    username: str
    password: str

    # Database properties
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)


@dataclass
class EnergyData(Base):
    __tablename__ = 'energy_data'

    # Serialize object to JSON
    id: int
    date: str
    energy: float
    reactive_energy: float
    power: float
    maximeter: float
    reactive_power: float
    voltage: float
    intensity: float
    power_factor: float

    # Database properties
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    energy = Column(Float)
    reactive_energy = Column(Float)
    power = Column(Float)
    maximeter = Column(Float)
    reactive_power = Column(Float)
    voltage = Column(Float)
    intensity = Column(Float)
    power_factor = Column(Float)


def populate():
    """
    Populate the database with the data in csv: ./docs/Monitoring report.csv
    """
    def check_no_empty(data):
        if data.strip() == '':
            return None
        else:
            return data

    with open('./docs/Monitoring report.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line = 0

        engine_db = setup_mysql_engine_default()
        session = sessionmaker(bind=engine_db)
        s = session()

        for row in csv_reader:
            if line == 0:
                line += 1
            else:
                s.add(EnergyData(date=datetime.datetime.strptime(row[0], '%d %b %Y %H:%M:%S'),
                                 energy=check_no_empty(row[1]),
                                 reactive_energy=check_no_empty(row[2]), power=check_no_empty(row[3]),
                                 maximeter=check_no_empty(row[4]), reactive_power=check_no_empty(row[5]),
                                 voltage=check_no_empty(row[6]), intensity=check_no_empty(row[7]),
                                 power_factor=check_no_empty(row[8])))
                line += 1

                if line % 500 == 0:
                    s.commit()
                    print(f'{line} rows inserted')

        print(f'{line} rows inserted')
        s.commit()
        s.close()
        engine_db.dispose()


if __name__ == '__main__':
    print('Creating database...')
    create_db()
    print('Creating models...')
    create_tables(Base)
    print('Populating database...')
    populate()
    print('OK')
