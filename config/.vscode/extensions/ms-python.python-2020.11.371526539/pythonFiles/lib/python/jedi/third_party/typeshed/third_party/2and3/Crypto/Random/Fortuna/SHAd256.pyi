from typing import Any, Optional

class _SHAd256:
    digest_size: Any
    def __init__(self, internal_api_check, sha256_hash_obj) -> None: ...
    def copy(self): ...
    def digest(self): ...
    def hexdigest(self): ...
    def update(self, data): ...

digest_size: Any

def new(data: Optional[Any] = ...): ...
