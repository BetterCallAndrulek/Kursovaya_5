from Database.db_manager import DBManager
from Database.getting_data_hh import HH_api_db


def main():
    # Get info about employers
    response = HH_api_db()

    employers_dict = response.employers_dict
    employers_all_vacancies = response.get_vacancies()

    # Create database
    database = DBManager()
    database.create_database('parser')

    # Create tables
    database.create_tables('parser')

    # Save info to database
    database.save_info_to_database('parser', employers_dict, employers_all_vacancies)

    print("Список компаний и количество вакансий в компаниях:")
    for row in database.get_companies_and_vacancies_count('parser'):
        print(f"{row[0]} - {row[1]}")

    print("Список всех вакансий с указанием названия компании:")
    for row in database.get_all_vacancies('parser'):
        print(f"{row[0]} - {row[1]}")

    print("Получает среднюю зарплату по вакансиям:")
    for row in database.get_avg_salary('parser'):
        print(f"{row[0]}")

    print("Список всех вакансий, у которых зарплата выше средней по всем вакансиям:")
    for row in database.get_vacancies_with_higher_salary('parser'):
        print(f"{row[0]}")

    keyword = 'Оператор'

    print("Список всех вакансий, в названии которых содержатся переданные в метод слова:")
    for row in database.get_vacancies_with_keyword('parser', keyword):
        print(f"{row[0]} ")


if __name__ == '__main__':
    main()