from enum import Enum

class ExecutionSort(str, Enum):
    UPDATED_AT = "updated_at"
    CREATED_AT = "created_at"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"