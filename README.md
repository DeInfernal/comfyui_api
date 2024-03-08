# ComfyUI API
This API was made for comfortable usage of ComfyUI tool through automated scripts like XY plot.

# Usage/Example
```python
import json
from comfyui_api import ComfyUIAPI

comfyapi = ComfyUIAPI('ip-address', 'port')

apiworkflow = json.load(open('comfyui-workflow-api.json', 'r', encoding='utf-8'))

comfyapi.generate_image(apiworkflow, 'image.png')
```
