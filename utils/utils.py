import psycopg2
from utils.config import config
from classes.HHParser import HHParser


def get_hh_employers() -> list:
    url = "https://api.hh.ru/employers"
    params = {'only_with_vacancies': True,
              'per_page': 10}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        return response_data['items']
    raise ConnectionError


def get_hh_data(employers: list) -> list:
    url = "https://api.hh.ru/vacancies"
    vacancies_data = []
    for employer in employers:
        params = {'employer_id': employer['id']}
        response = requests.get(url, params)
        response_data = json.loads(response.text)
        vacancies_data.extend(response_data['items'])
    return vacancies_data


def create_database(params: dict, db_name: str) -> None:
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql.SQL('CREATE DATABASE {};').format(
        sql.Identifier(db_name)))
    conn.close()


def create_employers_table(cur) -> None:
    cur.execute('''
        CREATE TABLE employers (
            id INTEGER PRIMARY KEY,
            name varchar(100) NOT NULL,
            open_vacancies int
    )
    ''')


def create_vacancies_table(cur) -> None:
    cur.execute('''
        CREATE TABLE vacancies (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(10),
            url VARCHAR(100) NOT NULL,
            employer_id INTEGER NOT NULL,
            FOREIGN KEY (employer_id) REFERENCES employers (id)
    )
    ''')


def insert_employers_data(cur, employers: list) -> None:
    for employer in employers:
        query = "INSERT INTO employers VALUES (%s, %s, %s)"
        employer_data = (int(employer['id']),
                         employer['name'],
                         employer['open_vacancies'])
        cur.execute(query, employer_data)


def insert_vacancies_data(cur, vacancies: list) -> None:
    for vacancy in vacancies:
        query = "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            vacancy_data = (int(vacancy['id']),
                            vacancy['name'],
                            vacancy['salary']['from'],
                            vacancy['salary']['to'],
                            vacancy['salary']['currency'],
                            vacancy['alternate_url'],
                            int(vacancy['employer']['id']))
        except TypeError:
            vacancy_data = (int(vacancy['id']),
                            vacancy['name'],
                            None, None, None,
                            vacancy['alternate_url'],
                            int(vacancy['employer']['id']))

        cur.execute(query, vacancy_data)
