import json

from pathlib import Path
from typing import List
from pydantic import ValidationError

from src.presentation.interfaces.protocols import IConfigValidator
from src.presentation.resources.strings import UIStrings
from src.forza_core.api.schemas import SessionStartRequest

class ConfigValidator(IConfigValidator):
    def validate(self, file_path: str) -> List[str]:
        path = Path(file_path)
        errors = []

        if not path.exists():
            return [UIStrings.ERR_FILE_NOT_FOUND.format(file_path)]

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate against Pydantic model
            SessionStartRequest(**data)
            
        except json.JSONDecodeError as e:
            errors.append(UIStrings.ERR_INVALID_JSON_FORMAT.format(str(e)))
        except ValidationError as e:
            for error in e.errors():
                msg = error.get('msg', '')
                loc = " -> ".join(str(l) for l in error.get('loc', []))
                
                # Basic mapping logic - can be extended
                if error['type'] == 'value_error.missing':
                    errors.append(UIStrings.ERR_MISSING_FIELD.format(loc))
                else:
                    # Provide a generic formatted error for other types
                    errors.append(f"{loc}: {msg}")
        except Exception as e:
            errors.append(UIStrings.ERR_GENERIC.format(str(e)))

        return errors
