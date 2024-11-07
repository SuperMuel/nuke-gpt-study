import logging
from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType

from . import suites_registry
from .suite import Suite

logger = logging.getLogger(__name__)


def get_suites_registry(
    mod: ModuleType = suites_registry, *, ignore_warnings: bool = False
) -> dict[str, Suite]:
    suites: dict[str, Suite] = {}

    for suite_mod in iter_modules(mod.__path__):
        mod_name = f"{mod.__name__}.{suite_mod.name}"
        suite_mod_obj = import_module(mod_name)

        if suite := suite_mod_obj.__dict__.get("suite"):
            if isinstance(suite, Suite):
                suites[suite_mod.name] = suite
            else:
                raise ValueError(
                    f"Module '{mod_name}' is not a Suite instance. Make sure to export it as 'suite'"
                )
        else:
            if not ignore_warnings:
                logger.warning(
                    f"Module '{mod_name}' does not have a suite instance. Make sure to export it as 'suite'"
                )

    if not suites:
        raise ValueError(f"No suites found in '{mod.__name__}'")

    return suites
