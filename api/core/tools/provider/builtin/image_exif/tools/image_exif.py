from base64 import b64decode
from typing import Any, Union

from httpx import post

from core.tools.entities.tool_entities import ToolInvokeMessage, ToolParameter
from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.image_exif.tools.test_data import IMAGE_CONTAINS_EXIF_PNG
from core.tools.tool.builtin_tool import BuiltinTool


class ExtractExifDataTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) \
        -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
            invoke tools
        """
        from PIL import Image
        from PIL.ExifTags import TAGS
        import io
        import json

        # 获取图片数据
        image_variable = self.get_default_image_variable()
        image_binary = self.get_variable_file(image_variable.name)
        if not image_binary:
            return self.create_text_message('Image not found, please request user to generate image firstly.')

        # 打开图片并提取EXIF数据
        image = Image.open(io.BytesIO(image_binary))
        exif_data = image._getexif()
        if not exif_data:
            return self.create_text_message('No EXIF data found in the image.')

        exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
        exif_json = json.dumps(exif, indent=4)

        return [
            self.create_text_message('EXIF data extracted successfully.'),
            self.create_blob_message(blob=exif_json.encode('utf-8'),
                                    meta={'mime_type': 'application/json'})
        ]
    
    def get_runtime_parameters(self) -> list[ToolParameter]:
        """
        override the runtime parameters
        """
        return [
            ToolParameter.get_simple_instance(
                name='image_id',
                llm_description=f'the image id that you want to vectorize, \
                    and the image id should be specified in \
                        {[i.name for i in self.list_default_image_variables()]}',
                type=ToolParameter.ToolParameterType.SELECT,
                required=True,
                options=[i.name for i in self.list_default_image_variables()]
            )
        ]
    