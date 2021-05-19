# Flickr Random Picker

Pick random photos from Flickr and download them.

## Requirement

[pyproject.toml](pyproject.toml)

Environments under poetry.

```bash
poetry install
```

## Usage

1. Get Flickr API key  
  https://www.flickr.com/services/api/

2. Create config.py  
  Copy [config_sample.py](config_sample.py) to config.py and edit `api_key`.

3. Pick random photos  

  ```bash
  poetry run python flickr_random_picker.py random_pick --get_num=50 --output_csv="photos.csv"
  ```

4. Download image  

  ```bash
  poetry run python flickr_random_picker.py download --input_csv="photos.csv" --output_dir="output"
  ```
