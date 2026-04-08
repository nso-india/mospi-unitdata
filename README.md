# MoSPI Unit Data Client

[![PyPI version](https://badge.fury.io/py/mospi-unitdata.svg)](https://badge.fury.io/py/mospi-unitdata)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python client for downloading microdata from the [MoSPI Microdata Portal](https://microdata.gov.in). 
This package provides a convenient interface to browse, search, and download datasets from the Government of India's National Statistical Office (NSO).

## Installation

```bash
pip install mospi-unitdata
```

## Getting an API Key

To use this package, you need an API key from the MoSPI Microdata Portal:

1.  Visit the [MoSPI Microdata Portal](https://microdata.gov.in).
2.  **Create an account** or sign in if you already have one.
3.  **Verify your email** address (check your inbox for a confirmation link).
4.  **Login** to your account.
5.  Navigate to your **Profile** section.
6.  Click on **Generate API Key** (or view your existing key).

## Usage

```python
from MospiUnitdata import list_datasets, list_files, download_file, download_dataset
```

### List datasets

```python
# List all datasets
datasets = list_datasets("YOUR_API_KEY")

# List a specific page
datasets = list_datasets("YOUR_API_KEY", page=1)

# Search by keyword
datasets = list_datasets("YOUR_API_KEY", query="labour force")

for d in datasets:
    print(f"{d['id']} ({d['idno']}): {d['title']}")
```

### List files in a dataset

```python
files = list_files("DDI-IND-NSO-ASI-2020-21", "YOUR_API_KEY")

for f in files:
    print(f"{f['name']} ({f.get('size', '?')})")
```

### Download a single file

```python
download_file("DDI-IND-NSO-ASI-2020-21", "ASI_DATA_2020_21_CSV.zip", "./data", "YOUR_API_KEY")
```

### Download all files in a dataset

```python
download_dataset("DDI-IND-NSO-ASI-2020-21", "./data", "YOUR_API_KEY")
```

### Interactive mode (legacy)

```python
from MospiUnitdata import getDatasets

getDatasets("./data", "YOUR_API_KEY")
```

This opens an interactive prompt to browse and select datasets page by page.

## API Reference

| Function | Description |
|----------|-------------|
| `list_datasets(api_key, page=None, query=None)` | List datasets. Returns all if no page specified. Optional keyword search. |
| `list_files(dataset_id, api_key)` | List files available in a dataset. |
| `download_file(dataset_id, file_name, folder_path, api_key)` | Download a single file from a dataset. |
| `download_dataset(dataset_id, folder_path, api_key)` | Download all files from a dataset. |
| `getDatasets(folder_path, api_key)` | Interactive browser and downloader (legacy). |

## Requirements
- Python 3.9+
- `requests` >= 2.31.0

## License

This project is licensed under the MIT License.
