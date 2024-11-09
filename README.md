# ComfyUI API
This API was made for comfortable usage of ComfyUI tool through automated scripts like XY plot.

# Installation
```bash
pip install git+https://github.com/DeInfernal/comfyui_api.git@v1.0.1
```

or

requirements.txt
```
comfyui_api @ git+https://github.com/DeInfernal/comfyui_api.git@v1.0.1
```

# Usage/Example
```python
import json
from comfyui_api import ComfyUIAPI

comfyapi = ComfyUIAPI('ip-address', 'port')

with open("workflow.json", "r", encoding="utf-8") as fstream:
    apiworkflow = json.load(fstream)

comfyapi.generate_image(apiworkflow, 'image.png')
```
