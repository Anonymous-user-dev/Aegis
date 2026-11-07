from pydantic import StringConstraints
from typing import Annotated

NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
