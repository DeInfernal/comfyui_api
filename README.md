# ComfyUI API

This API was made for comfortable usage of ComfyUI tool through automated scripts like XY plot.

## Installation

```bash
pip install git+https://github.com/DeInfernal/comfyui_api.git@v2.0.0
```

or

requirements.txt
```
comfyui_api @ git+https://github.com/DeInfernal/comfyui_api.git@v2.0.0
```

## Usage/Example

### Synchronous

```python
import json
from comfyui_api import ComfyUIAPI

def main():
    comfyapi = ComfyUIAPI('http://ip-address:port')

    with open("workflow.json", "r", encoding="utf-8") as fstream:
        apiworkflow = json.load(fstream)

    comfyapi.generate_image(apiworkflow, 'image.png')

main()
```

### Asynchronous

```python
import json
import aiohttp
import asyncio
from comfyui_api import ComfyUIAsyncAPI

async def main():
    async with aiohttp.ClientSession() as session:
        comfyapi = ComfyUIAsyncAPI(session, 'http://ip-address:port')

        with open("workflow.json", "r", encoding="utf-8") as fstream:
            apiworkflow = json.load(fstream)

        await comfyapi.generate_image(apiworkflow, 'image.png')

asyncio.run(main())
```
