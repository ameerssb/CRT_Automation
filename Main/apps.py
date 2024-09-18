from django.apps import AppConfig
import Main.run_crt_checker as run_crt_checker
# from .management.commands.run_crt_checker import run_crt_checker
import threading

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Main'

    # def ready(self):
        # print("App is ready and signal should be registered.")
        # checker_thread = threading.Thread(target=run_crt_checker.run_crt_checker)
        # checker_thread.daemon = True  # Daemon threads close when the main program closes
        # checker_thread.start()
        # import Main.signals  # Ensure the signals get registered
