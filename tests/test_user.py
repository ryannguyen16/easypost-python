import pytest

import easypost


@pytest.mark.vcr()
def test_user_create(prod_api_key):
    user = easypost.User.create(name="Test User")

    assert isinstance(user, easypost.User)
    assert str.startswith(user.id, "user_")
    assert user.name == "Test User"

    # Delete the user so we don't clutter up the test environment
    user.delete()


@pytest.mark.vcr()
def test_user_retrieve(prod_api_key):
    authenticated_user = easypost.User.retrieve_me()

    user = easypost.User.retrieve(authenticated_user["id"])

    assert isinstance(user, easypost.User)
    assert str.startswith(user.id, "user_")


@pytest.mark.vcr()
def test_user_retrieve_me(prod_api_key):
    user = easypost.User.retrieve_me()

    assert isinstance(user, easypost.User)
    assert str.startswith(user.id, "user_")


@pytest.mark.vcr()
def test_user_update(prod_api_key):
    user = easypost.User.retrieve_me()

    test_phone = "5555555555"

    user.phone = test_phone
    user.save()

    assert isinstance(user, easypost.User)
    assert str.startswith(user.id, "user_")
    assert user.phone == test_phone


@pytest.mark.vcr()
def test_user_delete(prod_api_key):
    user = easypost.User.create(name="Test User")

    # Nothing gets returned here, simply ensure no error gets raised
    user.delete()


@pytest.mark.vcr()
def test_user_all_api_keys(prod_api_key):
    user = easypost.User.retrieve_me()
    api_keys = user.all_api_keys()

    assert api_keys["keys"]
    assert api_keys["children"]


@pytest.mark.vcr()
def test_user_api_keys(prod_api_key):
    user = easypost.User.retrieve_me()
    api_keys = user.api_keys()

    assert api_keys


@pytest.mark.vcr()
def test_user_update_brand(prod_api_key):
    user = easypost.User.retrieve_me()

    color = "#123456"

    brand = user.update_brand(color=color)

    assert isinstance(brand, easypost.Brand)
    assert str.startswith(brand.id, "brd_")
    assert brand.color == color
