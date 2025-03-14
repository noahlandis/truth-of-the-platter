import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Paper, InputBase, IconButton, Box, List, ListItem, ListItemButton, ListItemText, Typography } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import axios from 'axios';
import { useSearchParams } from "react-router-dom";
import { useNavigate } from 'react-router-dom';
import { debounce } from 'lodash'; // Add this import

function SearchBar() {
    const apiUrl = import.meta.env.VITE_API_BASE_URL;
    const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;


    const navigate = useNavigate();
    const [searchParams] = useSearchParams();

    // State for name, location, suggestions, and error
    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [error, setError] = useState(''); // Error state
    const [locationError, setLocationError] = useState(''); // New state for location error

    // Ref for storing timeout ID for debouncing
    const debounceTimeoutRef = useRef(null);

    const autocompleteServiceRef = useRef(null);

    // New function to initialize the Autocomplete service
    const initializeAutocompleteService = useCallback(() => {
        if (window.google && window.google.maps && window.google.maps.places) {
            autocompleteServiceRef.current = new window.google.maps.places.AutocompleteService();
        }
    }, []);

    // Separate effect to initialize the Autocomplete service
    useEffect(() => {
        const checkGoogleMapsLoaded = setInterval(() => {
            if (window.google && window.google.maps && window.google.maps.places) {
                initializeAutocompleteService();
                clearInterval(checkGoogleMapsLoaded);
            }
        }, 100);

        return () => clearInterval(checkGoogleMapsLoaded);
    }, [initializeAutocompleteService]);

    // Existing effect for populating input fields
    useEffect(() => {
        const initialName = searchParams.get('name') || '';
        const initialLocation = searchParams.get('location') || '';
        
        if (window.location.pathname === '/') {
            setLocation('');
            setName('');
        } else {
            setName(initialName);
            setLocation(initialLocation);
        }
    
        // Remove the Autocomplete service initialization from here
    }, [searchParams]);

    // Clear name input
    const handleClearName = () => setName('');
    const handleClearLocation = () => setLocation('');

    // Handle suggestion click
    const handleSuggestionClick = (suggestion) => {
        setLocation(suggestion);
        setShowSuggestions(false);
    };

    // Show suggestions on focus
    const handleFocus = () => {
        setShowSuggestions(true);
    };

    const handleBlur = () => {
        setTimeout(() => setShowSuggestions(false), 100);
    };

    useEffect(() => {
        if (location.length > 0) {
            if (debounceTimeoutRef.current) {
                clearTimeout(debounceTimeoutRef.current);
            }

            debounceTimeoutRef.current = setTimeout(() => {
                if (autocompleteServiceRef.current) {
                    autocompleteServiceRef.current.getPlacePredictions(
                        {
                            input: location,
                            types: ['(cities)'],
                            componentRestrictions: { country: 'us' }
                        },
                        (predictions, status) => {
                            if (status === window.google.maps.places.PlacesServiceStatus.OK && predictions) {
                                const formattedPredictions = predictions.map(prediction => ({
                                    ...prediction,
                                    description: prediction.description.replace(/, USA$/, '')
                                }));
                                setSuggestions(formattedPredictions);
                            } else {
                                console.error('Error fetching location suggestions:', status);
                                setSuggestions([]);
                            }
                        }
                    );
                }
            }, 200); // 200ms debounce delay
        } else {
            setSuggestions([]);
            setShowSuggestions(false);
        }

        return () => {
            if (debounceTimeoutRef.current) {
                clearTimeout(debounceTimeoutRef.current);
            }
        };
    }, [location]);

    const handleLocationChange = (e) => {
        setLocation(e.target.value);
        setShowSuggestions(true);
        setLocationError('');
    };

    // Memoize the debounced function
    const debouncedReverseGeocode = useCallback(
        debounce(async (latitude, longitude) => {
            const apiUrl = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${GOOGLE_MAPS_API_KEY}`;
            
            try {
                const response = await axios.get(apiUrl);
                const results = response.data.results;
                if (results.length > 0) {
                    const addressComponents = results[0].address_components;

                    const city = addressComponents.find((component) =>
                        component.types.includes('locality')
                    )?.long_name;

                    const state = addressComponents.find((component) =>
                        component.types.includes('administrative_area_level_1')
                    )?.short_name; // Use short_name for state abbreviation

                    const userLocation = `${city}, ${state}`;
                    setLocation(userLocation);
                    setShowSuggestions(false);
                }
            } catch (error) {
                console.error('Error reverse geocoding location:', error);
            }
        }, 300),
        [GOOGLE_MAPS_API_KEY]
    );

    const handleUserLocationClick = () => {
        if (navigator.geolocation) {
            setLocation('Fetching location...'); // Provide immediate feedback
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    debouncedReverseGeocode(latitude, longitude);
                },
                (error) => {
                    console.error('Error getting user location:', error);
                    setLocationError("We couldn't access your location. Please enter a city or allow location access.");
                    setLocation(''); // Clear the input if there's an error
                },
                { timeout: 10000, maximumAge: 60000 } // Add options for better performance
            );
        } else {
            alert('Geolocation is not supported by this browser.');
        }
    };

    // Updated handleSearch function
    const handleSearch = async (e) => {
        e.preventDefault();

        // Check if name is empty and set error if true
        if (!name.trim()) {
            setError("Please enter a restaurant name");
            return; // Prevent form submission
        }

        setError(''); // Clear name error if validation passes
        setLocationError(''); // Clear location error

        let searchLocation = location;

        // If location is blank, get current location
        if (!location.trim()) {
            try {
                const currentLocation = await getCurrentLocation();
                searchLocation = currentLocation;
            } catch (error) {
                console.error('Error getting current location:', error);
                setLocationError("We couldn't access your location. Please enter a city or allow location access.");
                return; // Prevent form submission
            }
        }

        navigate(`/search?name=${name}&location=${searchLocation}`);
    };

    // Updated getCurrentLocation function
    const getCurrentLocation = () => {
        return new Promise((resolve, reject) => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(async (position) => {
                    const { latitude, longitude } = position.coords;
                    const apiUrl = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${GOOGLE_MAPS_API_KEY}`;
                    
                    try {
                        const response = await axios.get(apiUrl);
                        const results = response.data.results;
                        if (results.length > 0) {
                            const addressComponents = results[0].address_components;
                            const city = addressComponents.find((component) =>
                                component.types.includes('locality')
                            )?.long_name;
                            const state = addressComponents.find((component) =>
                                component.types.includes('administrative_area_level_1')
                            )?.long_name;
                            const userLocation = `${city}, ${state}`;
                            resolve(userLocation);
                        } else {
                            reject(new Error('No results found'));
                        }
                    } catch (error) {
                        reject(error);
                    }
                }, (error) => {
                    reject(new Error("We couldn't access your location. Please try again or enter a location manually."));
                }, {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                });
            } else {
                reject(new Error("Your browser doesn't support geolocation. Please enter a location manually."));
            }
        });
    };

    return (
        <>
            <Paper
                component="form"
                onSubmit={handleSearch}
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    height: 65,
                    width: '100%',
                    borderRadius: '0 8px 8px 0',
                    boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
                    border: '1px solid #ccc',
                }}
            >
                <Box sx={{ position: 'relative', flex: 1, borderRight: '1px solid #ccc' }}>
                    <InputBase
                        value={name}
                        onChange={(e) => {
                            setName(e.target.value);
                            setError('');
                        }}
                        placeholder="What's the name of the restaurant?"
                        sx={{
                            pl: 2,
                            pr: 6, // Increased right padding to accommodate the clear button
                            py: 1,
                            width: '100%', // Changed from calc to 100%
                            height: '100%',
                        }}
                        inputProps={{ 'aria-label': 'name' }}
                    />

                    {error && (
                        <Typography
                            color="error"
                            sx={{
                                position: 'absolute',
                                bottom: '-8px', // Adjust this value to control the spacing
                                left: 6,
                                fontSize: '0.75rem',
                                paddingLeft: '10px',
                                borderTop: '2px solid red', // Add top red border
                                width: 'calc(100% - 12px)', // Increase the width to cover more of the x-axis
                            }}
                        >
                            {error}
                        </Typography>
                    )}
                    {name && (
                        <IconButton
                            onClick={handleClearName}
                            sx={{
                                position: 'absolute',
                                right: 10,
                                top: '50%',
                                transform: 'translateY(-50%)',
                                padding: 0,
                            }}
                            aria-label="clear name"
                        >
                            <ClearIcon fontSize="small" />
                        </IconButton>
                    )}
                </Box>

                <Box sx={{ position: 'relative', flex: 1 }}>
                    <InputBase
                        value={location}
                        onChange={handleLocationChange}
                        onFocus={handleFocus}
                        onBlur={handleBlur}
                        placeholder="Where is it located?"
                        sx={{
                            pl: 2,
                            pr: 6, // Increased right padding to accommodate the clear button
                            py: 1,
                            width: '100%', // Changed from calc to 100%
                            height: '100%',
                        }}
                        inputProps={{ 'aria-label': 'location' }}
                    />
                    {location && (
                        <IconButton
                            onClick={handleClearLocation}
                            sx={{
                                position: 'absolute',
                                right: 10,
                                top: '50%',
                                transform: 'translateY(-50%)',
                                padding: 0,
                            }}
                            aria-label="clear location"
                        >
                            <ClearIcon fontSize="small" />
                        </IconButton>
                    )}
                    {locationError && (
                        <Typography
                            color="error"
                            sx={{
                                position: 'absolute',
                                bottom: '-8px',
                                left: 6,
                                fontSize: '0.75rem',
                                paddingLeft: '10px',
                                borderTop: '2px solid red',
                                width: 'calc(100% - 12px)',
                            }}
                        >
                            {locationError}
                        </Typography>
                    )}
                    {showSuggestions && (
                        <List
                            sx={{
                                position: 'absolute',
                                top: '115%',
                                left: 0,
                                right: 0,
                                width: '100%',
                                backgroundColor: '#fff',
                                boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
                                zIndex: 1,
                                maxHeight: 200,
                                overflowY: 'auto',
                                borderBottomLeftRadius: '8px',
                                borderBottomRightRadius: '8px',
                            }}
                        >
                            <ListItem disablePadding>
                                <ListItemButton onMouseDown={() => handleUserLocationClick()}>
                                    <Box
                                        component="span"
                                        sx={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            mr: 1,
                                        }}
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            version="1.1"
                                            width="24"
                                            height="24"
                                            viewBox="0 0 256 256"
                                        >
                                            <g
                                                style={{
                                                    stroke: 'none',
                                                    strokeWidth: 0,
                                                    fill: 'none',
                                                    fillRule: 'nonzero',
                                                    opacity: 1,
                                                }}
                                                transform="translate(1.4 1.4) scale(2.81 2.81)"
                                            >
                                                <path
                                                    d="M 45 90 c -1.415 0 -2.725 -0.748 -3.444 -1.966 l -4.385 -7.417 C 28.167 65.396 19.664 51.02 16.759 45.189 c -2.112 -4.331 -3.175 -8.955 -3.175 -13.773 C 13.584 14.093 27.677 0 45 0 c 17.323 0 31.416 14.093 31.416 31.416 c 0 4.815 -1.063 9.438 -3.157 13.741 c -0.025 0.052 -0.053 0.104 -0.08 0.155 c -2.961 5.909 -11.41 20.193 -20.353 35.309 l -4.382 7.413 C 47.725 89.252 46.415 90 45 90 z"
                                                    style={{
                                                        fill: 'rgb(4,136,219)',
                                                    }}
                                                    transform="matrix(1 0 0 1 0 0)"
                                                />
                                                <path
                                                    d="M 45 45.678 c -8.474 0 -15.369 -6.894 -15.369 -15.368 S 36.526 14.941 45 14.941 c 8.474 0 15.368 6.895 15.368 15.369 S 53.474 45.678 45 45.678 z"
                                                    style={{
                                                        fill: 'rgb(255,255,255)',
                                                    }}
                                                    transform="matrix(1 0 0 1 0 0)"
                                                />
                                            </g>
                                        </svg>
                                    </Box>
                                    <ListItemText
                                        primary="Current Location"
                                        sx={{
                                            color: '#0688DB',
                                        }}
                                    />
                                </ListItemButton>
                            </ListItem>

                            {suggestions.map((suggestion, index) => (
                                <ListItem key={index} disablePadding>
                                    <ListItemButton onMouseDown={() => handleSuggestionClick(suggestion.description)}>
                                        <ListItemText primary={suggestion.description} />
                                    </ListItemButton>
                                </ListItem>
                            ))}
                        </List>
                    )}
                </Box>
                <IconButton
                    type="submit"
                    sx={{
                        backgroundColor: '#1976d2',
                        color: '#fff',
                        height: '100%',
                        borderRadius: '0 8px 8px 0',
                        width: 65,
                    }}
                    aria-label="search"
                >
                    <SearchIcon />
                </IconButton>
            </Paper>
        </>
    );
}

export default SearchBar;