import psycopg2
from utils.config import config


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query) -> list:
        conn = psycopg2.connect(dbname='db_name', **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        ''' Метод, получающий список всех компаний и вакансий у каждой компании. '''


        result = self.execute_query('SELECT employers.name, COUNT(vacancies.employer_id) AS vacancies_count FROM employers LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id GROUP BY employers.name')
        return result


    def get_all_vacancies(self):
        ''' Метод, получающий список всех вакансий. '''

        result = self.execute_query('SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url FROM employers JOIN vacancies using (employer_id)')
        return result


    def get_avg_salary(self):
        ''' Метод, получающий среднюю зарплату по вакансиям. '''

        result = self.execute_query('SELECT AVG(salary_from) AS payment_avg FROM vacancies')
        return result


    def get_vacancies_with_higher_salary(self):
        ''' Метод, получающий список всех вакансий, у которых зарплата выше средней по всем вакансиям. '''

        result = self.execute_query('SELECT * FROM vacancies WHERE salary_from > (select AVG(salary_from) FROM vacancies)')
        return result


    def get_vacancies_with_keyword(self, keywords):
        ''' Метод, поиска всех вакансий по ключевому слову. '''

        result = self.execute_query(f'SELECT * FROM vacancies WHERE name LIKE \'%{keywords}%\'')
        return result
