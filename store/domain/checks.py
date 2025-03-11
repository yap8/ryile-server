from domain import exceptions as exc


def check_if_dict_is_not_empty(data: dict):
    if data == dict():
        raise exc.ValidationError("Как минимум, одно поле должно быть заполнено!")
