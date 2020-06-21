from accounts.models import User


def sample_user(superuser: bool = False, **params) -> User:
    """
    Create and return a sample user

    email = simon@marsimon.com \n
    pass = testing123
    """
    defaults = {
        'email': 'simon@marsimon.com',
        'password': 'testing123'
    }
    defaults.update(params)

    if superuser:
        return User.objects.create_superuser(**defaults)
    return User.objects.create_user(**defaults)
