# Truth of the Platter

Truth of the Platter is a website that aggregates restaurant reviews from Yelp, TripAdvisor, and Google to provide a more accurate rating.

## Features

- Gets ratings and review counts from Yelp, Google, and TripAdvisor
- Calculates a weighted average rating based on the data from all sources
- Provides a command-line interface for easy interaction
- Supports automatic location detection (when location is not provided)
- Handles errors gracefully and provides informative messages

## Project Structure

- `setup.py`: Project configuration and metadata
- `main.py`: Entry point of the application
- `input.py`: Handles user input and output formatting
- `cli_command.py`: Manages command-line interface commands
- `scrape.py`: Contains the main scraping logic
- `calculate_weighted_average.py`: Calculates the weighted average rating
- `exceptions.py`: Custom exception classes
- `model/`: Contains classes for different review sources (Google, TripAdvisor)
- `utils/`: Utility functions and helpers

## License

This project is licensed under the MIT License.

## Author

Noah Landis 

## Acknowledgements

- This project uses the Yelp API/Google Places API for initial restaurant data
- Thanks to the creators of the libraries used in this project: requests, BeautifulSoup, colorama, and more
