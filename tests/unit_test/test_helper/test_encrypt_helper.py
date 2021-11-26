from figure_hook.Helpers.encrypt_helper import EncryptHelper


def test_encrypt_str_to_str():
    value = "cool"
    e_value = EncryptHelper.encrypt_str(value)
    assert type(e_value) is str


def test_decrpyt_str_to_str():
    value = "cool"
    e_value = EncryptHelper.encrypt_str(value)
    d_value = EncryptHelper.decrypt_str(e_value)
    assert type(d_value) is str
