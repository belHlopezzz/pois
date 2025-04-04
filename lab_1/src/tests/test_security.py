import pytest
from os_simulation.security import DefaultSecurity


def test_default_security_initialization():
    security = DefaultSecurity()
    assert security.user_info == {"password": "stud", "username": "stud"}


def test_authenticate_success():
    security = DefaultSecurity()
    assert security.authenticate("stud", "stud") is True


def test_authenticate_wrong_username():
    security = DefaultSecurity()
    assert security.authenticate("wrong_user", "stud") is False


def test_authenticate_wrong_password():
    security = DefaultSecurity()
    assert security.authenticate("stud", "wrong_password") is False


def test_authenticate_wrong_username_and_password():
    security = DefaultSecurity()
    assert security.authenticate("wrong_user", "wrong_password") is False


def test_authenticate_case_sensitivity():
    security = DefaultSecurity()
    assert security.authenticate("Stud", "stud") is False
    assert security.authenticate("stud", "Stud") is False
