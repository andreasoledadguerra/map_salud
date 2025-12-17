# Map Salud

Map Salud is an interactive web application built with Streamlit that visualizes public health establishments on a map using geospatial data. It leverages GeoPandas for data processing and PyDeck for rendering interactive maps, allowing users to explore health facilities in a given region from Buenos Aires Province, Argentina. 

## Features

- **Interactive Map Visualization**: Displays health establishments as points on an interactive map.
- **Geospatial Data Processing**: Loads and processes CSV data containing latitude, longitude, and facility names.
- **Tooltip Information**: Hover over points to view facility names.
- **Responsive Design**: Built with Streamlit for easy deployment and sharing.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/map-salud.git
   cd map-salud
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Note: The `requirements.txt` file includes core dependencies. You may need to install additional packages like `streamlit` and `pydeck` if not already present:
   ```bash
   pip install streamlit pydeck
   ```

## Usage

1. Run main.py :
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run app/streamlit_app.py
   ```

3. Open your web browser and navigate to the provided local URL (usually `http://localhost:8003`).

4. Interact with the map: Zoom, pan, and hover over points to view facility details.


## Dependencies

 - geopandas==1.1.1
 - scikit-learn==1.8.0
 - fastapi==0.124.4
 - uvicorn==0.38.0
 - streamlit==1.52.1
 - folium==0.20.0
 - streamlit_folium==0.25.3

## Data

The application requires a CSV file named `establecimientos-salud-publicos.csv` with the following columns:
- `lat` (COL_LAT): Latitude of the health establishment
- `long`(COL_LONG): Longitude of the health establishment
- `fna` (EST_SALUD) : Name of the health facility


## Project Structure

- `main.py`: Main Streamlit application script
- `main.ipynb`: Jupyter notebook for data exploration and prototyping
- `requirements.txt`: Python dependencies
- `README.md`: This file
- `.gitignore`: Git ignore rules
- `LICENSE`: Project license

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the terms specified in the LICENSE file.
