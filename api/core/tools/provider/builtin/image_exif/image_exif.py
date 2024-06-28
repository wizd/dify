from typing import Any

from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.image_exif.tools.image_exif import ExtractExifDataTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class ImageExifProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            ExtractExifDataTool().invoke(
                user_id='',
                tool_parameters={
                    "mode": "test",
                    "image_id": "__test_123"
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
        