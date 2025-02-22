
from manager.secret_santa_manager import SecretSantaManager
import os

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    manager = SecretSantaManager()
    manager.run()