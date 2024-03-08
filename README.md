# ComfyUI API
This API was made for comfortable usage of ComfyUI tool through automated scripts like XY plot.

# Installation
```bash
pip install git+https://github.com/DeInfernal/comfyui_api.git@v1.0.0
```

or

requirements.txt
```
-e git://github.com/DeInfernal/comfyui_api.git@v1.0.0
```

# Usage/Example
```python
import json
from comfyui_api import ComfyUIAPI

comfyapi = ComfyUIAPI('ip-address', 'port')

apiworkflow = json.load(open('comfyui-workflow-api.json', 'r', encoding='utf-8'))

comfyapi.generate_image(apiworkflow, 'image.png')
```
