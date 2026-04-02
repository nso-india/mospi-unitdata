# MoSPI Microdata Client

[![PyPI version](https://badge.fury.io/py/mospi-microdata.svg)](https://badge.fury.io/py/mospi-microdata)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python client for downloading microdata from the [MoSPI Microdata Portal](https://microdata.gov.in). 
This package provides a convenient interface to browse and download datasets from the Government of India's National Statistical Office (NSO).

### About
This package is used to download the data from the MoSPI Microdata Portal. Specifically, you can browse available datasets interactively and download them by calling the provided methods with your API key.

## Installation

You can install the package directly from PyPI:

```bash
pip install mospi-microdata
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

To download datasets, use the `getDatasets` method. This method takes two mandatory parameters:
1.  **First parameter (`folderPath`)**: The location/folder on your computer where you want to save the downloaded data.
2.  **Second parameter (`apiKey`)**: Your API key generated from the [MicroData Portal Profile Section](https://microdata.gov.in/NADA/index.php/auth/profile).

```python
from MospiMicrodata import getDatasets

# Provide the save location and your API Key
getDatasets("path/to/save/data", "YOUR_API_KEY")
```

The function provides an interactive prompt to browse through the available datasets:

```text
277:Annual Survey of Industries 2019-20
275:Annual Survey of Industries 2020-21
256:Annual Survey of Industries 2023-24
...
Total pages:13,Page:1 of 13,
Enter Survey index number(put n to Navigate to Next Page): 
```

Type the numeric index to download the associated dataset, or `n` to view the next page.

## Requirements
- Python 3.9+
- `requests` >= 2.31.0


## License

This project is licensed under the MIT License.

