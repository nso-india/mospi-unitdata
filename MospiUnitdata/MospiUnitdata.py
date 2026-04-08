import requests
import os
import time
from typing import List, Dict, Any, Optional

BASE_URL = "https://microdata.gov.in/NADA/index.php/api"

MAX_RETRIES = 4
RETRY_DELAY = 3  # seconds


def _request_with_retry(method, url, **kwargs) -> requests.Response:
    """Make an HTTP request with automatic retry on 401/5xx errors."""
    for attempt in range(MAX_RETRIES):
        response = method(url, **kwargs)
        if response.status_code not in (401, 429, 500, 502, 503, 504):
            return response
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY * (attempt + 1))
    return response


def _fetch_page(api_key: str, page: int) -> Optional[Dict[str, Any]]:
    """Fetch a single page of datasets from the API."""
    headers = {"X-API-KEY": api_key}
    try:
        response = _request_with_retry(
            requests.get,
            f"{BASE_URL}/listdatasets",
            params={"page": page},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching dataset list: {e}")
        return None


def list_datasets(api_key: str, page: Optional[int] = None, query: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """List datasets from the MoSPI Microdata Portal.

    Args:
        api_key: Your MoSPI Microdata Portal API key.
        page: Page number to fetch. If None, fetches all pages.
        query: Optional search string to filter by title (case-insensitive).

    Returns:
        List of dataset dicts, or None on failure.
    """
    if page is not None:
        data = _fetch_page(api_key, page)
        if data is None:
            return None
        rows = data["result"]["rows"]
    else:
        first_page = _fetch_page(api_key, 1)
        if first_page is None:
            return None

        result = first_page["result"]
        rows = list(result["rows"])
        total = int(result["total"])
        limit = int(result["limit"])
        pages = total // limit + (1 if total % limit else 0)

        for p in range(2, pages + 1):
            data = _fetch_page(api_key, p)
            if data is None:
                break
            rows.extend(data["result"]["rows"])

    if query:
        query_lower = query.lower()
        rows = [d for d in rows if query_lower in d.get("title", "").lower()]

    return rows


def _resolve_dataset_id(dataset_id: str, api_key: str) -> Optional[str]:
    """Resolve a numeric id to an idno. Returns idno as-is if not numeric."""
    if not dataset_id.isdigit():
        return dataset_id

    datasets = list_datasets(api_key)
    if datasets is None:
        return None

    for d in datasets:
        if d["id"] == dataset_id:
            return d["idno"]

    print(f"No dataset found with id '{dataset_id}'.")
    return None


def list_files(dataset_id: str, api_key: str) -> Optional[List[Dict[str, Any]]]:
    """List files available for a specific dataset.

    Args:
        dataset_id: The numeric id (e.g., '275') or idno
            (e.g., 'DDI-IND-NSO-ASI-2020-21') of the dataset.
        api_key: Your MoSPI Microdata Portal API key.

    Returns:
        List of file dicts with 'name', 'base64', etc. None on failure.
    """
    dataset_id = _resolve_dataset_id(dataset_id, api_key)
    if dataset_id is None:
        return None

    url = f"{BASE_URL}/datasets/{dataset_id}/fileslist"
    headers = {"X-API-KEY": api_key}

    try:
        response = _request_with_retry(requests.get, url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("files", [])
    except requests.RequestException as e:
        print(f"Error fetching file list for '{dataset_id}': {e}")
        return None


def download_file(dataset_id: str, file_name: str, folder_path: str, api_key: str) -> Optional[str]:
    """Download a single file from a dataset.

    Args:
        dataset_id: The numeric id or idno of the dataset.
        file_name: Name of the file to download (as shown by list_files).
        folder_path: Directory to save the file into (created if it doesn't exist).
        api_key: Your MoSPI Microdata Portal API key.

    Returns:
        Path to the downloaded file, or None on failure.
    """
    os.makedirs(folder_path, exist_ok=True)

    files = list_files(dataset_id, api_key)
    if files is None:
        print("Failed to retrieve file list.")
        return None

    match = None
    for f in files:
        if f["name"] == file_name:
            match = f
            break

    if match is None:
        print(f"File '{file_name}' not found in dataset '{dataset_id}'.")
        print(f"Available files: {[f['name'] for f in files]}")
        return None

    headers = {"X-API-KEY": api_key}
    url = f"{BASE_URL}/fileslist/download/{dataset_id}/{match['base64']}"

    try:
        response = _request_with_retry(requests.get, url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading '{file_name}': {e}")
        return None

    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"Downloaded: {file_path}")
    return file_path


def download_dataset(dataset_id: str, folder_path: str, api_key: str) -> List[str]:
    """Download all files for a dataset to a local folder.

    Args:
        dataset_id: The numeric id or idno of the dataset.
        folder_path: Directory to save files into (created if it doesn't exist).
        api_key: Your MoSPI Microdata Portal API key.

    Returns:
        List of paths to successfully downloaded files.
    """
    os.makedirs(folder_path, exist_ok=True)

    files = list_files(dataset_id, api_key)
    if files is None:
        print("Failed to retrieve file list.")
        return []

    if not files:
        print(f"No files found for dataset '{dataset_id}'.")
        return []

    headers = {"X-API-KEY": api_key}
    downloaded = []

    for file_info in files:
        file_name = file_info["name"]
        file_b64 = file_info["base64"]
        url = f"{BASE_URL}/fileslist/download/{dataset_id}/{file_b64}"

        try:
            response = _request_with_retry(requests.get, url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error downloading '{file_name}': {e}")
            continue

        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {file_path}")
        downloaded.append(file_path)

    return downloaded


# --- Backward-compatible interactive function ---

def getDatasets(folderPath: str, apiKey: str):
    """Interactive dataset browser and downloader (legacy interface).

    Presents a paginated list of datasets and prompts the user to
    select one for download.

    Args:
        folderPath: Directory to save downloaded files.
        apiKey: Your MoSPI Microdata Portal API key.
    """
    page = 1

    while True:
        rows = list_datasets(apiKey, page=page)
        if rows is None:
            print("Error occurred while fetching datasets.")
            break

        for item in rows:
            print(f"{item['id']}:{item['title']}")

        # Need total/limit for pagination info - fetch raw page
        data = _fetch_page(apiKey, page)
        if data is None:
            break

        total = int(data["result"]["total"])
        limit = int(data["result"]["limit"])
        pages = total // limit + (1 if total % limit else 0)

        user_input = input(
            f"Total pages:{pages}, Page:{page} of {pages},\n"
            "Enter Survey index number (put n to Navigate to Next Page): "
        )

        if user_input.strip().lower() == "n":
            page += 1
            if page > pages:
                print("No more pages left to browse.")
                break
            continue

        if not user_input.isdigit():
            print("Invalid index number.")
            break

        # Find the dataset idno by matching the id
        idno = None
        for item in rows:
            if item["id"] == user_input:
                idno = item["idno"]
                break

        if idno is None:
            print("No dataset found with that index. Please check and try again.")
            break

        download_dataset(idno, folderPath, apiKey)
        break
