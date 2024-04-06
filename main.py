from database.database_manager import DBManager
from utils.utils import create_database, create_tables, insert_data_into_tables


def user_interaction():

    list_employers = [3127, 3776, 4934, 3529, 4181, 78638, 54979, 64174, 3388, 2180]
    dbm = DBManager()
    create_database('db_name')
    create_tables('db_name')
    insert_data_into_tables(list_employers)

    while True:

        new = input(
            '1 - список всех компаний и кол-во вакансий у каждой компании\n'
            '2 - список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию\n'
            '3 - средняя зарплата по вакансиям\n'
            '4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
            '5 - список вакансий, в названии которых содержится ключевое слово\n'
            'Выход - закончить\n'
        )

        if new == '1':
            print(dbm.get_companies_and_vacancies_count())
        elif new == '2':
            print(dbm.get_all_vacancies())
        elif new == '3':
            print(dbm.get_avg_salary())
        elif new == '4':
            print(dbm.get_vacancies_with_higher_salary())
        elif new == '5':
            keyword = str(input('Найти: '))
            print(dbm.get_vacancies_with_keyword(keyword))
        elif new == 'Выход':
            break

if __name__ == "__main__":
    user_interaction()
