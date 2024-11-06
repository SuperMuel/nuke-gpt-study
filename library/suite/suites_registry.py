from pydantic import BaseModel

from .nuke_temperature import nuke_temperature_suite
from .suite import Suite

SuitesRegistry = dict[str, Suite[BaseModel]]

SUITES_REGISTRY: SuitesRegistry = {
    "nuke_temperature": nuke_temperature_suite,
}
