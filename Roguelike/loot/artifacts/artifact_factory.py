# loot/artifacts/artifact_factory.py
import uuid
from .artifact import Artifact
from loot.artifacts_database import ARTIFACTS


def create_artifact(artifact_id):
    """Создать артефакт по ID из базы данных"""
    data = ARTIFACTS.get(artifact_id)
    
    # ✅ ПРОВЕРКА В ПЕРВУЮ ОЧЕРЕДЬ!
    if not data:
        raise ValueError(f"Artifact '{artifact_id}' not found in database")
    
    # ✅ СОЗДАЕМ АРТЕФАКТ
    art = Artifact(**data)
    
    # ✅ ГЕНЕРИРУЕМ UID
    art.uid = str(uuid.uuid4())
    
    return art