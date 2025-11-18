# Map Salud

Map Salud is an interactive web application built with Streamlit that visualizes public health establishments on a map using geospatial data. It leverages GeoPandas for data processing and PyDeck for rendering interactive maps, allowing users to explore health facilities in a given region.

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

3. Ensure you have the data file `establecimientos-salud-publicos.csv` in the project directory. This CSV should contain columns for `lat`, `long`, and `fna` (facility name).

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).

3. Interact with the map: Zoom, pan, and hover over points to view facility details.

For exploratory data analysis, you can also run the Jupyter notebook:
```bash
jupyter notebook main.ipynb
```

## Dependencies

- geopandas==1.1.1
- numpy==2.2.6
- pandas==2.3.3
- streamlit (not listed in requirements.txt, install separately)
- pydeck (not listed in requirements.txt, install separately)

## Data

The application requires a CSV file named `establecimientos-salud-publicos.csv` with the following columns:
- `lat`: Latitude of the health establishment
- `long`: Longitude of the health establishment
- `fna`: Name of the health facility

Ensure the data is in the correct format and placed in the project root directory.

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
