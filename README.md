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
  <https://www.flickr.com/services/api/>

2. Create config.py  
  Copy [config_sample.py](config_sample.py) to config.py and edit `api_key`.

3. Pick random photos  

  ```bash
  poetry run python flickr_random_picker.py random_pick --get_num=50 --output_csv="photos.csv"
  ```

4. Download images  

  ```bash
  poetry run python flickr_random_picker.py download --input_csv="photos.csv" --output_dir="output"
  ```


## Output sample

[photos10000.csv](photos10000.csv) is a list of 10000 photos picked up randomly.  
These are royalty-free licensed (mostly CC0) photos of over 2000 x 2000px.  


## Note

The current algorithm is not able to select all photos equally.  
The photos uploaded on the datetime when there are fewer photos are more likely to be selected than the photos uploaded on the datetime when there are more photos.
