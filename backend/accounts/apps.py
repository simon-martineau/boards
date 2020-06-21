from django.apps import AppConfig


# noinspection PyUnresolvedReferences
class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
