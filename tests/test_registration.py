import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    # Функция create_db() создает базу данных users.db и инициализирует схему
    create_db()
    yield
    # Очистка после выполнения тестов
    os.remove('users.db')

def test_create_db(setup_database):
    """Тест создания базы данных и таблицы пользователей."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Проверяем, существует ли таблица users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database):
    """Тест добавления нового пользователя."""
    result = add_user('testuser', 'testuser@example.com', 'password123')
    assert result, "Пользователь должен быть успешно добавлен."
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_existing_user(setup_database):
    """Тест добавления пользователя с существующим логином."""
    add_user('testuser2', 'testuser2@example.com', 'password123')
    result = add_user('testuser2', 'testuser2@example.com', 'password123')
    assert not result, "Пользователь с таким логином уже существует и не должен быть добавлен повторно."

def test_authenticate_user_success(setup_database):
    """Тест успешной аутентификации пользователя."""
    add_user('authuser', 'authuser@example.com', 'securepassword')
    authenticated = authenticate_user('authuser', 'securepassword')
    assert authenticated, "Пользователь должен быть успешно аутентифицирован."

def test_authenticate_nonexistent_user(setup_database):
    """Тест аутентификации несуществующего пользователя."""
    authenticated = authenticate_user('nonexistentuser', 'password123')
    assert not authenticated, "Несуществующий пользователь не должен быть аутентифицирован."

def test_authenticate_user_wrong_password(setup_database):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('wrongpassuser', 'wrongpassuser@example.com', 'rightpassword')
    authenticated = authenticate_user('wrongpassuser', 'wrongpassword')
    assert not authenticated, "Пользователь с неправильным паролем не должен быть аутентифицирован."

def test_display_users(capsys, setup_database):
    """Тест отображения списка пользователей."""
    add_user('displayuser1', 'displayuser1@example.com', 'password123')
    add_user('displayuser2', 'displayuser2@example.com', 'password123')
    display_users()
    captured = capsys.readouterr()
    assert 'Логин: displayuser1, Электронная почта: displayuser1@example.com' in captured.out
    assert 'Логин: displayuser2, Электронная почта: displayuser2@example.com' in captured.out
