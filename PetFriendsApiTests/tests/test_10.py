from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


# test 1
def test_add_new_pet_with_valid_data(name='Penelope', animal_type='Pom', age='12'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple_with_valid_data(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''


# test 2
def test_add_photo_of_pet(pet_photo='images/black-pomeranian-MK-long.jpg'):
    """Проверяем что можно добавить фото в существующий файл питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    assert status == 200
    assert result['pet_photo'] != ''


# test 3

def test_get_api_key_with_no_password(email=valid_email, password=''):
    """"Проверяем, что при отсутствии пароля не возможно войти и получить ключ"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


# test 4
def test_get_api_key_with_no_email(email='', password=valid_password):
    """"Проверяем, что при отсутствии email не возможно войти и получить ключ"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


# test 5
def test_add_new_pet_with_cyrilic_letters(name='Тигра', animal_type='Кот', age='12',
                                          pet_photo='images/Article_Allergies_Pomeranians.jpg'):
    """Проверяем что можно добавить питомца с корректными данными на кирилице"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type


# test 6
def test_add_new_pet_with_latin_letters(name='Penny', animal_type='Dog', age='10',
                                        pet_photo='images/Article_Allergies_Pomeranians.jpg'):
    """Проверяем что можно добавить питомца с корректными данными на латинице"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type


# test 7
def test_add_new_pet_with_no_name(name='', animal_type='Кот', age='12',
                                  pet_photo='images/Article_Allergies_Pomeranians.jpg'):
    """Проверяем что нельзя добавить питомца без имени"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == ''


# test 8
def test_add_new_pet_with_negative_age(name='Dolly', animal_type='Sheep', age='-12',
                                       pet_photo='images/Article_Allergies_Pomeranians.jpg'):
    """Проверяем что нельзя добавить питомца с отрицательным возрастом"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


# test 9
def test_add_new_pet_with_letter_age(name='Dolly', animal_type='Sheep', age='ФФФ',
                                     pet_photo='images/Article_Allergies_Pomeranians.jpg'):
    """Проверяем что нельзя добавить питомца с возрастом указанным буквами"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400

# test 10
def test_add_new_pet_with_invalid_pet_photo(name='Eva', animal_type='Carrot', age='13',pet_photo=''):
    """Проверяем что нельзя добавить питомца, если не указан путь до фала"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        _, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        raise Exception("Файл с фотогпрафией питомца существует!")
    except FileNotFoundError:
        print('\nФайл с фотогпрафией питомца или каталог отсутствует!')

