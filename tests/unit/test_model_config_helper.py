from agentrules.core.agents.gemini import GeminiArchitect
from agentrules.core.types.models import GEMINI_FLASH
from agentrules.core.utils.model_config_helper import get_model_config_name


def test_get_model_config_name_predefined_constant():
    assert get_model_config_name(GEMINI_FLASH) == "GEMINI_FLASH"


def test_get_model_config_name_from_dict_matches_constant():
    cfg_dict = {
        "provider": GEMINI_FLASH.provider,
        "model_name": GEMINI_FLASH.model_name,
        "reasoning": GEMINI_FLASH.reasoning,
        "temperature": GEMINI_FLASH.temperature,
    }
    assert get_model_config_name(cfg_dict) == "GEMINI_FLASH"


def test_get_model_config_name_from_architect_instance():
    arch = GeminiArchitect(model_name=GEMINI_FLASH.model_name, reasoning=GEMINI_FLASH.reasoning)
    assert get_model_config_name(arch) == "GEMINI_FLASH"

