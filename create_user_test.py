import sender_stand_request
import data

def get_user_body(first_name):
     current_body = data.user_body.copy()
     current_body["firstName"] = first_name
     return current_body

# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1

# Функция для негативной проверки
def negative_assert_symbol(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)

    # В переменную response сохраняется результат запроса
    response = sender_stand_request.post_new_user(user_body)

    # Проверка, что код ответа равен 400
    assert response.status_code == 400

    # Проверка, что в теле ответа атрибут "code" равен 400
    assert response.json()["code"] == 400
    # Проверка текста в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"


# Функция для негативной проверки
# В ответе ошибка: "Не все необходимые параметры были переданы"
def negative_assert_no_first_name(user_body):
    # В переменную response сохрани результат вызова функции
    response = sender_stand_request.post_new_user(user_body)

    # Проверь, что код ответа — 400
    assert response.status_code == 400

    # Проверь, что в теле ответа атрибут "code" — 400
    assert response.json()["code"] == 400

    # Проверь текст в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"


# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2. Успешное создание пользователя
# Параметр fisrtName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
   positive_assert("Ааааааааааааааа")

# Тест 3. Ошибка создания пользователя
# Параметр fisrtName состоит из 1 символа
def test_create_user_1_letter_in_first_name_get_error_response():
   negative_assert_symbol("А")

# Тест 4. Ошибка создания пользователя
# Параметр fisrtName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
   negative_assert_symbol("Аааааааааааааааа")

# Тест 5. Успешное создание пользователя
# Параметр fisrtName состоит из ангийских буквв
def test_create_user_english_letter_in_first_name_get_success_response():
   positive_assert("QWErty")

# Тест 6. Успешное создание пользователя
# Параметр fisrtName состоит из русских буквв
def test_create_user_russian_letter_in_first_name_get_success_response():
   positive_assert("Мария")

# Тест 7. Ошибка создания пользователя
# Параметр fisrtName содержит пробелы
def test_create_user_has_space_in_first_name_get_error_response():
   negative_assert_symbol("Человек и Ко")

# Тест 8. Ошибка создания пользователя
# Параметр fisrtName содержит спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
   negative_assert_symbol("№%@")

# Тест 9. Ошибка создания пользователя
# Параметр fisrtName содержит цифры
def test_create_user_has_number_in_first_name_get_error_response():
   negative_assert_symbol("123")

# Тест 10. Ошибка
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

# Тест 12. Ошибка
# Тип параметра firstName: число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
