# Real-Time Cryptocurrency Dashboard

## Overview
The **Real-Time Cryptocurrency Dashboard** is a Streamlit-based web application that fetches live cryptocurrency market data, processes it, and visualizes it in an interactive dashboard. Users can filter and sort cryptocurrencies by market cap, price, and trading volume. The app also provides interactive charts and a clean UI for data visualization.

## Features
- Fetches real-time cryptocurrency market data from an API.
- Data transformation using Pandas.
- Interactive Streamlit interface.
- Visualizes price comparisons and market cap share using Altair and Matplotlib.
- Filters to sort and select the number of cryptocurrencies displayed.
- Supports deployment on Streamlit Cloud and Docker.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python (>=3.7)
- pip
- Git

### Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/real-time-data-pipeline.git
cd real-time-data-pipeline
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Running the Application
To launch the Streamlit app, run:
```bash
streamlit run src/app.py
```

## Project Structure
```
real-time-data-pipeline
├── src
│   ├── app.py             # Streamlit app main script
│   ├── data_fetcher.py     # API fetching and data processing
├── tests
│   ├── test_data_fetcher.py  # Pytest test cases
├── .github/workflows
│   ├── test.yml            # GitHub Actions CI/CD workflow
├── requirements.txt        # Required dependencies
├── Dockerfile              # Docker containerization setup
└── README.md               # Project documentation
```

## Usage
1. Open the app by running `streamlit run src/app.py`.
2. Select the number of cryptocurrencies to display using the sidebar slider.
3. Sort cryptocurrencies by Market Cap, Price, or Volume.
4. View the interactive bar chart for price comparison.
5. Analyze market cap share using a pie chart.

## Deployment

### Deploy on Streamlit Cloud
1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and log in.
3. Create a new app and connect your GitHub repository.
4. Set the entry point to:
   ```
   src/app.py
   ```
5. Click **Deploy**.

### Deploy with Docker
1. Build the Docker image:
   ```bash
   docker build -t crypto-dashboard .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 8501:8501 crypto-dashboard
   ```
3. Open `http://localhost:8501` in your browser.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Added new feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

## Contact
For questions or suggestions, reach out at `luisnietohueso@gmail.com` or open an issue in the repository.

Happy coding!
