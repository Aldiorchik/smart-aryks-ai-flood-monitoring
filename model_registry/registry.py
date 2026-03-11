import json
from pathlib import Path
from datetime import datetime

REGISTRY_PATH = Path("model_registry/registry.json")
REGISTRY_PATH.parent.mkdir(exist_ok=True)


def register_model(model_path, metrics):

    if REGISTRY_PATH.exists():
        registry = json.load(open(REGISTRY_PATH))
    else:
        registry = []

    entry = {
        "model_path": str(model_path),
        "metrics": metrics,
        "timestamp": datetime.utcnow().isoformat()
        
    }

    registry.append(entry)

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)

    print("Model registered")