from contextlib import nullcontext as does_not_raise
from datetime import timedelta
import pytest
from src.api import *


class Pagination:
    def __init__(self, page_param, limit_param):
        self.page = page_param
        self.limit = limit_param


@pytest.fixture()
def user():
    user = create_user(firstname="Davdid", lastname="Jiglov")
    return user


@pytest.fixture(scope="session", autouse=True)
def prints():
    print("Тесты начаты")
    yield
    print("Тесты завергены")


class TestAutorized:

    def test_getusers_non_autorized(self):
        assert get_users(api_key='322').status_code == 403

    def test_getusers_autorized(self):
        assert get_users().status_code == 200


def test_pagination_speed():
    response = get_users(pagination=Pagination(1, 50))
    assert response.status_code == 200
    assert response.elapsed <= timedelta(milliseconds=700)


def test_pagination_():
    pagination = Pagination(1, 50)
    response = get_users(pagination=pagination)
    assert response.status_code == 200
    assert response.json()['page'] == pagination.page
    assert response.json()['limit'] == pagination.limit


@pytest.mark.parametrize("firstname, lastname, status", [("Stivejkn", "Sigal", 200),
                                                         ("9999999999999999999999999999999999", "Elephant", 400),
                                                         ("True", "2", 400),
                                                         ("2", "Irrvan", 400),
                                                         ("True", "9999999999999999999999999999999999", 400),
                                                         ("None", "12", 200),
                                                         ("<script>", "<script>", 200), ])
def test_create_user(firstname, lastname, status):
    assert create_user(firstname, lastname).status_code == status


@pytest.mark.parametrize("gender, firstname, lastname, status", [("other", "a", "olala", 200),
                                                                 ("fio", "ababab", "o", 200),
                                                                 ("helicopter", "David", "positivovi4", 200), ])
def test_update_user(user, gender, firstname, lastname, status):
    user_id = get_user_id(user)
    resp_updated_user = update_user(user_id=user_id, gender=gender, firstname=firstname, lastname=lastname)
    user_info = get_user(id=user_id)
    assert resp_updated_user.status_code == status
    assert resp_updated_user.json()['gender'] == gender
    assert resp_updated_user.json()['firstName'] == firstname
    assert resp_updated_user.json()['lastName'] == lastname
    assert user_info.status_code == status


@pytest.mark.parametrize("json_data, expectation", [({"text": "g", "likes": "0"}, does_not_raise()),
                                                    ({"text": "1ffffff25", "likes": "e"}, pytest.raises(KeyError)),
                                                    ({"text": "", "likes": "1000000"}, does_not_raise()), ])
def test_create_post(json_data, expectation):
    firstname = 'Vika'
    json_user = create_user(firstname, lastname="Frolkina")
    user_id = get_user_id(json_user)
    respo = create_post(user_id, json_data)
    with expectation:
        assert respo.json()[('owner')]['firstName'] == firstname
        assert respo.json()['text'] == json_data['text']

# def test_update_user():
#   my_cool_response1 = create_user()
#  response2 = create_user()
#
#   user_id1 = get_user_id(my_cool_response1)
#  user_id2 = get_user_id(response2)
# print (f'{user_id1}+{user_id2}')
# assert update_user(user_id).status_code == 200
