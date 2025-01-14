import pytest

import easypost


@pytest.mark.vcr()
def test_carrier_account_create(prod_api_key, basic_carrier_account):
    carrier_account = easypost.CarrierAccount.create(**basic_carrier_account)

    assert isinstance(carrier_account, easypost.CarrierAccount)
    assert str.startswith(carrier_account.id, "ca_")
    assert carrier_account.type == "UpsAccount"

    carrier_account.delete()  # Delete the carrier account once it's done being tested.


@pytest.mark.vcr()
def test_carrier_account_retrieve(prod_api_key, basic_carrier_account):
    carrier_account = easypost.CarrierAccount.create(**basic_carrier_account)

    retrieved_carrier_account = easypost.CarrierAccount.retrieve(carrier_account.id)

    assert isinstance(retrieved_carrier_account, easypost.CarrierAccount)
    # status changes between creation and retrieval, so we can't compare the whole object
    assert carrier_account.id == retrieved_carrier_account.id

    carrier_account.delete()  # Delete the carrier account once it's done being tested.


@pytest.mark.vcr()
def test_carrier_account_all(prod_api_key, page_size):
    carrier_accounts = easypost.CarrierAccount.all(page_size=page_size)

    assert all(isinstance(carrier_account, easypost.CarrierAccount) for carrier_account in carrier_accounts)


@pytest.mark.vcr()
def test_carrier_account_update(prod_api_key, basic_carrier_account):
    carrier_account = easypost.CarrierAccount.create(**basic_carrier_account)

    test_description = "My custom description"

    carrier_account.description = test_description
    carrier_account.save()

    assert isinstance(carrier_account, easypost.CarrierAccount)
    assert str.startswith(carrier_account.id, "ca_")
    assert carrier_account.description == test_description

    carrier_account.delete()  # Delete the carrier account once it's done being tested.


@pytest.mark.vcr()
def test_carrier_account_delete(prod_api_key, basic_carrier_account):
    carrier_account = easypost.CarrierAccount.create(**basic_carrier_account)

    response = carrier_account.delete()
    assert isinstance(response, easypost.CarrierAccount)


@pytest.mark.vcr()
def test_carrier_account_type(prod_api_key):
    types = easypost.CarrierAccount.types()

    assert isinstance(types, list)
