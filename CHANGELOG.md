# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-08

### Added
- `list_datasets(api_key, page=None, query=None)` - list and search datasets programmatically.
- `list_files(dataset_id, api_key)` - list files in a dataset before downloading.
- `download_file(dataset_id, file_name, folder_path, api_key)` - download a single file.
- `download_dataset(dataset_id, folder_path, api_key)` - download all files in a dataset.
- Automatic retry with backoff on transient API errors (401/429/5xx).
- Auto-creation of download directories.

### Changed
- All API calls now require an API key (the `listdatasets` endpoint requires authentication).
- `getDatasets` refactored to use the new functions internally.

### Removed
- Removed redundant `setup.py` (using `pyproject.toml` with Hatchling).

## [0.1.0] - 2026-04-06

### Added
- Initial project setup using `pyproject.toml` and Hatchling.
- Publish `mospi-unitdata` wrapper implementation on PyPI.
- Add CLI paging mechanism to `getDatasets` for iterating through portal surveys.
- Support interactive numeric index selection for microdata downloading.
- Rename package from `mospi-microdata` to `mospi-unitdata` (and related imports).
