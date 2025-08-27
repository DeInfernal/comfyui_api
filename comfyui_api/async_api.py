import json
import asyncio
import aiohttp
import aiofiles


class ComfyUIAsyncAPI:
    """
    This class makes connections between software and ComfyUI
    Allowing you to generate images remotely
    """

    _session = None
    _base_url = ""

    def __init__(self, session: aiohttp.ClientSession, comfyui_base_url: str) -> None:
        """
        Initalization of ComfyUI.

        Parameters
        ----------
        session : aiohttp.ClientSession
            A session object of AIOHTTP
        comfyui_base_url : str
            Scheme, IP/Port of ComfyUI web server. (Example: http://127.0.0.1:8188)
        """
        self._session = session
        self._base_url = comfyui_base_url

    #  -------------------------------------------------------------------------
    #  ____            _         __                  _   _                   _
    # |  _ \          (_)       / _|                | | (_)                 | |
    # | |_) | __ _ ___ _  ___  | |_ _   _ _ __   ___| |_ _  ___  _ __   __ _| |
    # |  _ < / _` / __| |/ __| |  _| | | | '_ \ / __| __| |/ _ \| '_ \ / _` | |
    # | |_) | (_| \__ \ | (__  | | | |_| | | | | (__| |_| | (_) | | | | (_| | |
    # |____/ \__,_|___/_|\___| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|\__,_|_|
    #
    # -------------------------------------------------------------------------

    async def _request_get(self, path: str):
        """
        Base method for all GET requests to ComfyUI API.

        Parameters
        ----------
        path : str
            API path to access (example: 'prompt' or 'history/22')
        """
        request_uri = "{}/{}".format(self._base_url, path)
        response = await self._session.get(request_uri)
        return await response.text()

    async def _request_post(self, path: str, post_data: str = None):
        """
        Base method for all POST requests to ComfyUI API.

        Parameters
        ----------
        path : str
            API path to access (example: 'prompt' or 'history/22')
        post_data : str, optional
            Data to send though, by default None.
        """
        request_uri = "{}/{}".format(self._base_url, path)
        response = await self._session.post(request_uri, data=bytes(post_data, "utf-8"))
        return await response.text()

    async def _call_api(self, path: str, method: str = "GET", post_data: str = None):
        """
        Base method for calling API. API calls ALWAYS return JSON object.

        Parameters
        ----------
        path : str
            API path to access (example: 'prompt' or 'history/22')
        method : str, optional
            Method, by default "GET"
        post_data : str, optional
            Data to send though, by default None. If data was sent, don't forget to change method to POST.
        """
        if method == "GET":
            response = await self._request_get(path)
        elif method == "POST":
            response = await self._request_post(path, post_data)

        return json.loads(response)

    async def _download(self, path: str, save_to: str):
        """
        Base method for downloading byte-like objects. Used for getting pictures downloaded.

        Parameters
        ----------
        path : str
            Path to download from
        save_to : str
            Path to save to (locally)
        """
        request_uri = "{}/{}".format(self._base_url, path)

        response = await self._session.get(request_uri)

        downloaded_file = await response.read()

        async with aiofiles.open(save_to, "wb") as file:
            await file.write(downloaded_file)

    # -----------------------------------------------------------------
    #           _____ _____                  _   _               _
    #     /\   |  __ \_   _|                | | | |             | |
    #    /  \  | |__) || |    _ __ ___   ___| |_| |__   ___   __| |___
    #   / /\ \ |  ___/ | |   | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` / __|
    #  / ____ \| |    _| |_  | | | | | |  __/ |_| | | | (_) | (_| \__ \
    # /_/    \_\_|   |_____| |_| |_| |_|\___|\__|_| |_|\___/ \__,_|___/
    #
    # -----------------------------------------------------------------

    async def send_generation_request(self, workflow: dict) -> dict:
        """
        Method that puts a single Workflow into queue of ComfyUI server.

        Parameters
        ----------
        workflow : dict
            Dictonary object (jsonable) containing ComfyUI Workflow in API form.

        Returns
        -------
        dict
            JSON-answer from the server, containing things like Prompt ID.
        """
        wrapped_workflow = {"prompt": workflow}
        response = await self._call_api("prompt", "POST", json.dumps(wrapped_workflow))
        return response

    async def get_generation_status(self, prompt_id: str) -> dict:
        """
        Method that asks server about status of specific queued image ID.
        Can return either empty dictionary if there is no such item in history
        or JSON API format else, containing everything from generation including result.

        Returns JSON only in case that image is FINISHED. Not earlier.

        Parameters
        ----------
        prompt_id : str
            ID of task, can be found in send_generation_request()['prompt_id']

        Returns
        -------
        dict
            JSON answer from a server
        """
        response = await self._call_api("history/{}".format(prompt_id))
        return response

    async def download_image(self, path_to_save_file: str, comfy_filename: str, comfy_subfolder: str = "", comfy_type: str = "output") -> None:
        """
        Method that allows to download a single image file from ComfyUI server.
        Should be used in conjunction with get_generation_status to ensure that image exists already.

        Parameters
        ----------
        path_to_save_file : str
            Path where image would be saved
        comfy_filename : str
            File name inside ComfyUI output folder. Returns in get_generation_status.
        comfy_subfolder : str, optional
            Subfolder inside ComfyUI output folder. Returns in get_generation_status. By default ''
        comfy_type : str, optional
            Output type inside ComfyUI output folder. Returns in get_generation_status. By default 'output'
        """
        await self._download("view?filename={}&subfolder={}&type={}".format(comfy_filename, comfy_subfolder, comfy_type), path_to_save_file)

    # -----------------------------------------------------------------------------------------------------------------------------------------
    #   _____                      _                                  _       _                                      _   _               _
    #  / ____|                    | |                                (_)     (_)                                    | | | |             | |
    # | |     ___  _ __ ___  _ __ | | _____  __   ___ ___  _ ____   ___ _ __  _  ___ _ __   ___ ___   _ __ ___   ___| |_| |__   ___   __| |___
    # | |    / _ \| '_ ` _ \| '_ \| |/ _ \ \/ /  / __/ _ \| '_ \ \ / / | '_ \| |/ _ \ '_ \ / __/ _ \ | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` / __|
    # | |___| (_) | | | | | | |_) | |  __/>  <  | (_| (_) | | | \ V /| | | | | |  __/ | | | (_|  __/ | | | | | |  __/ |_| | | | (_) | (_| \__ \
    #  \_____\___/|_| |_| |_| .__/|_|\___/_/\_\  \___\___/|_| |_|\_/ |_|_| |_|_|\___|_| |_|\___\___| |_| |_| |_|\___|\__|_| |_|\___/ \__,_|___/
    #                       | |
    #                       |_|
    # -----------------------------------------------------------------------------------------------------------------------------------------

    async def generate_image(self, workflow: dict, save_path: str) -> None:
        """
        A convinient complex method that allows you to generate image and download in the same command.

        Parameters
        ----------
        workflow : dict
            Dictonary object (jsonable) containing ComfyUI Workflow in API form.
        save_path : str
            Path where image generated from workflow should be saved. Must be ending with '.png'
        """
        # Step 1: Send generation request and record it's ID
        prompt_id_future = await self.send_generation_request(workflow)
        prompt_id = prompt_id_future["prompt_id"]

        # Step 2: Wait till history returns something (meaning, generation is finished)
        history = {}
        while len(history) == 0:
            await asyncio.sleep(3)
            history = await self.get_generation_status(prompt_id)

        # Step 3: Save image somewhere
        if len(history[prompt_id]["outputs"]) == 1:
            for output in history[prompt_id]["outputs"]:
                await self.download_image(save_path,
                                          history[prompt_id]["outputs"][output]["images"][0]["filename"],
                                          history[prompt_id]["outputs"][output]["images"][0]["subfolder"],
                                          history[prompt_id]["outputs"][output]["images"][0]["type"])
        elif len(history[prompt_id]["outputs"]) > 1:
            for output in history[prompt_id]["outputs"]:
                exploded_save_path = save_path.split(".")
                exploded_save_path[-2] = exploded_save_path[-2] + str(output)
                mended_save_path = ".".join(exploded_save_path)
                await self.download_image(mended_save_path,
                                          history[prompt_id]["outputs"][output]["images"][0]["filename"],
                                          history[prompt_id]["outputs"][output]["images"][0]["subfolder"],
                                          history[prompt_id]["outputs"][output]["images"][0]["type"])
