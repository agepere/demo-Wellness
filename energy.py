from flask import Blueprint, make_response, request, jsonify
from models import EnergyData
import datetime
from database import setup_mysql_engine_default
from sqlalchemy.orm import sessionmaker

energy_api = Blueprint('energy', __name__)

ERROR_MESSAGE = 'There was an unexpected error, please try again later'


@energy_api.route('/')
def energy():
    engine_db = None
    s = None
    response = None

    try:
        engine_db = setup_mysql_engine_default()
        session = sessionmaker(bind=engine_db)
        s = session()

        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')

        if startDate is None or endDate is None:
            response = make_response(
                {'message': 'Params startDate and endDate are required. The format they have match is dd/MM/yyyy'}, 400)
        else:
            startDate = datetime.datetime.strptime(startDate + ' 00:00:00', '%d/%m/%Y %H:%M:%S')
            endDate = datetime.datetime.strptime(endDate + ' 23:59:59', '%d/%m/%Y %H:%M:%S')

            energies = s.query(EnergyData).filter(EnergyData.date >= startDate).filter(EnergyData.date <= endDate).all()

            response = make_response(jsonify(energies), 200)

    except ValueError:
        response = make_response(
            {'message': 'Params startDate and endDate are required. The format they must match is dd/MM/yyyy'}, 400)
    except:
        response = make_response({'message': ERROR_MESSAGE}, 500)
    finally:
        # Clean resources and return the response
        if s is not None:
            s.close()
        if engine_db is not None:
            engine_db.dispose()

        if response is not None:
            return response
        else:
            return make_response({'message': ERROR_MESSAGE}, 500)


@energy_api.route('/<startDate>/<endDate>')
def energyGroupByDate(startDate, endDate):
    engine_db = None
    response = None
    conn = None

    try:
        datetime.datetime.strptime(startDate + ' 00:00:00', '%d-%m-%Y %H:%M:%S')
        datetime.datetime.strptime(endDate + ' 23:59:59', '%d-%m-%Y %H:%M:%S')

        engine_db = setup_mysql_engine_default()
        conn = engine_db.connect()

        query = conn.execute("""
        SELECT CAST(DATE as DATE) date, sum(energy) as energy, sum(reactive_energy) as reactive_energy
        FROM energy_data
        WHERE 
            DATE BETWEEN  STR_TO_DATE(%s, %s) AND STR_TO_DATE(%s, %s) 
        GROUP BY CAST(DATE as DATE);""", startDate + ' 00:00:00', '%d-%m-%Y %H:%i:%s', endDate + ' 23:59:59',
                             '%d-%m-%Y %H:%i:%s')

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        response = make_response(jsonify(result), 200)

    except ValueError as e:
        print(e)
        response = make_response(
            {'message': 'The format date must match is dd-MM-yyyy'}, 400)
    except Exception as e:
        print(e)
        response = make_response({'message': ERROR_MESSAGE}, 500)
    finally:
        # Clean resources and return the response
        if conn is not None:
            conn.close()
        if engine_db is not None:
            engine_db.dispose()

        if response is not None:
            return response
        else:
            return make_response({'message': ERROR_MESSAGE}, 500)
