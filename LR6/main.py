from auth import login_user, login_employee
from unauthorized_menu import unauthorized_menu
from client_menu import client_menu
from employee_menu import employee_menu

def main_menu():
    while True:
        print("\n" + "="*40)
        print("                Главное меню")
        print("="*40)
        print("1. Войти как неавторизованный пользователь")
        print("2. Войти как клиент")
        print("3. Войти как сотрудник")
        print("4. Выйти")
        print("="*40)

        choice = input("Выберите опцию (1-4): ")

        if choice == '1':
            print("\nВы вошли как **Неавторизованный пользователь**.")
            print("-" * 40)
            unauthorized_menu()

        elif choice == '2':
            print("\nВы выбрали вход как **Клиент**.")
            print("-" * 40)
            email = input("Введите ваш email: ")
            password = input("Введите ваш пароль: ")
            user_id = login_user(email, password)  # Получаем client_id
            if user_id:
                print("\n✅ Авторизация прошла успешно.")
                print("-" * 40)
                client_menu(user_id)  # Передаем client_id в client_menu
            else:
                print("\n❌ Неверный email или пароль. Пожалуйста, попробуйте снова.")
                print("-" * 40)

        elif choice == '3':
            print("\nВы выбрали вход как **Сотрудник**.")
            print("-" * 40)
            email = input("Введите ваш email: ")
            password = input("Введите ваш пароль: ")
            user = login_employee(email, password)
            if user:
                print("\n✅ Авторизация прошла успешно.")
                print("-" * 40)
                employee_menu()
            else:
                print("\n❌ Неверный email или пароль. Пожалуйста, попробуйте снова.")
                print("-" * 40)

        elif choice == '4':
            print("\n🚪 Выход из программы. До свидания!")
            print("="*40)
            break  # Выход из цикла и завершение программы

        else:
            print("\n❌ Неверный выбор. Пожалуйста, выберите опцию от 1 до 4.")
            print("-" * 40)


if __name__ == "__main__":
    main_menu()
