from django.apps import AppConfig

import threading
from evm_bff.api.mqtt import outside_service_receive_message

class EvmBffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evm_bff'

    def ready(self):
        # start mqtt listener thread here
        thread = threading.Thread(target=outside_service_receive_message)
        thread.start()