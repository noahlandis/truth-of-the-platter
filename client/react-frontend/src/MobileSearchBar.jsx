import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Paper, InputBase, IconButton, Box, List, ListItem, ListItemButton, ListItemText, Typography, Fade } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import { useSearchParams, useNavigate } from "react-router-dom";
import axios from 'axios';
import { debounce } from 'lodash'; // Add this import

function MobileSearchBar({ onFocus, onBlur, cancelSearchRef }) {
    const apiUrl = import.meta.env.VITE_API_BASE_URL;
    const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [error, setError] = useState(null);
    const [activeInput, setActiveInput] = useState(null);
    const [searchParams, setSearchParams] = useSearchParams();
    const navigate = useNavigate();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [nameError, setNameError] = useState('');
    const [showNameError, setShowNameError] = useState(false);
    const [nameErrorOpacity, setNameErrorOpacity] = useState(1);
    const [showSuggestions, setShowSuggestions] = useState(true);

    const autocompleteServiceRef = useRef(null);
    const debounceTimeoutRef = useRef(null);

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
    
        if (window.google && window.google.maps && window.google.maps.places) {
            autocompleteServiceRef.current = new window.google.maps.places.AutocompleteService();
        }
    }, [searchParams]);

    useEffect(() => {
        if (cancelSearchRef) {
            cancelSearchRef.current = () => {
                setActiveInput(null);
                setError(null);
                setSuggestions([]);
                setIsSubmitting(false);
                onBlur();
            };
        }
    }, [cancelSearchRef, onBlur]);

    const handleClearName = () => setName('');
    const handleClearLocation = () => setLocation('');

    const handleSuggestionClick = (suggestion) => {
        setLocation(suggestion);
        setSuggestions([]);
        setShowSuggestions(false);
        // Focus the input and move cursor to the end
        const inputElement = document.querySelector('input[aria-label="location"]');
        if (inputElement) {
            inputElement.focus();
            inputElement.setSelectionRange(suggestion.length, suggestion.length);
        }
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
                    setSuggestions([]);
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
                    setLocation(''); // Clear the input if there's an error
                },
                { timeout: 10000, maximumAge: 60000 } // Add options for better performance
            );
        } else {
            alert('Geolocation is not supported by this browser.');
        }
    };

    const handleLocationChange = (e) => {
        setLocation(e.target.value);
        setShowSuggestions(true);  // Show suggestions when user starts typing
        if (e.target.value.length > 0) {
            if (debounceTimeoutRef.current) {
                clearTimeout(debounceTimeoutRef.current);
            }

            debounceTimeoutRef.current = setTimeout(() => {
                if (autocompleteServiceRef.current) {
                    autocompleteServiceRef.current.getPlacePredictions(
                        {
                            input: e.target.value,
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
            }, 200);
        } else {
            setSuggestions([]);
        }
    };

    const handleSearch = (e) => {
        e.preventDefault();
        performSearch();
    };

    const performSearch = () => {
        setIsSubmitting(true);
        if (!name.trim()) {
            setNameError('Name field cannot be left blank');
            setShowNameError(true);
            setActiveInput('name');
            setIsSubmitting(false);
            return;
        }

        setNameError('');
        setShowNameError(false);
        navigate(`/search?name=${name}&location=${location}`);
        setIsSubmitting(false);
        
        // Trigger handleCancel if there's no error
        if (cancelSearchRef && cancelSearchRef.current) {
            cancelSearchRef.current();
        }
    };

    // Add this new function to handle key press events
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch();
        }
    };

    const handleInputFocus = (inputType) => {
        setActiveInput(inputType);
        onFocus();
    };

    const handleInputBlur = (e) => {
        // Delay the blur effect to allow for error checking
        setTimeout(() => {
            if (!e.currentTarget.contains(document.activeElement) && !isSubmitting) {
                if (!error) {
                    setActiveInput(null);
                    onBlur();
                    // Add this line to trigger handleCancel when the input loses focus
                    if (cancelSearchRef && cancelSearchRef.current) {
                        cancelSearchRef.current();
                    }
                }
            }
        }, 100);
    };

    useEffect(() => {
        if (showNameError) {
            setNameErrorOpacity(1);
            const fadeOutTimer = setTimeout(() => {
                setNameErrorOpacity(0);
            }, 500); // Start fading out after 2 seconds

            const hideTimer = setTimeout(() => {
                setShowNameError(false);
            }, 1000); // Hide completely after 3 seconds

            return () => {
                clearTimeout(fadeOutTimer);
                clearTimeout(hideTimer);
            };
        }
    }, [showNameError]);

    return (
        <Paper
            component="form"
            id="mobile-search-form"
            onSubmit={handleSearch}
            sx={{
                display: 'flex',
                flexDirection: 'column',
                width: '100%',
                borderRadius: '8px',
                boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
                border: '1px solid #ccc',
                position: 'relative', // Add this line
            }}
            onBlur={handleInputBlur}
        >
            <Box sx={{ display: 'flex', alignItems: 'center', borderBottom: activeInput ? '1px solid #ccc' : 'none' }}>
                <InputBase
                    value={showNameError ? nameError : name}
                    onChange={(e) => {
                        setName(e.target.value);
                        setNameError('');
                        setShowNameError(false);
                        setNameErrorOpacity(1);
                    }}
                    onFocus={() => handleInputFocus('name')}
                    sx={{
                        ml: 2,
                        flex: 1,
                        py: 1,
                        '& input': {
                            color: showNameError ? 'error.main' : 'inherit',
                            opacity: showNameError ? nameErrorOpacity : 1,
                            transition: 'color 0.3s, opacity 1s',
                        },
                    }}
                    inputProps={{
                        'aria-label': 'name',
                        placeholder: 'Name',
                        enterKeyHint: 'search', // Add this line
                    }}
                    onKeyPress={handleKeyPress}
                    onBlur={handleInputBlur}
                />
                {name && !showNameError && (
                    <IconButton onClick={handleClearName} sx={{ padding: 1 }} aria-label="clear name">
                        <ClearIcon fontSize="small" />
                    </IconButton>
                )}
            </Box>
            {activeInput && (
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <InputBase
                        value={location}
                        onChange={handleLocationChange}
                        onFocus={() => {
                            handleInputFocus('location');
                            setShowSuggestions(true);  // Show suggestions when input is focused
                        }}
                        placeholder="Location"
                        sx={{ ml: 2, flex: 1, py: 1 }}
                        inputProps={{ 
                            'aria-label': 'location',
                            enterKeyHint: 'search', // Add this line
                        }}
                        onKeyPress={handleKeyPress}
                        onBlur={handleInputBlur}
                    />
                    {location && (
                        <IconButton onClick={handleClearLocation} sx={{ padding: 1 }} aria-label="clear location">
                            <ClearIcon fontSize="small" />
                        </IconButton>
                    )}
                </Box>
            )}
            {activeInput === 'location' && showSuggestions && (
                <List 
                    sx={{ 
                        maxHeight: 200, 
                        overflowY: 'auto', 
                        bgcolor: 'background.paper',
                        position: 'absolute',
                        top: '100%',
                        left: 0,
                        right: 0,
                        zIndex: 1,
                        boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
                        border: '1px solid #ccc',
                        borderTop: 'none',
                    }}
                >
                    <ListItem disablePadding>
                        <ListItemButton onClick={handleUserLocationClick}>
                            <LocationOnIcon sx={{ mr: 2, color: '#0688DB' }} />
                            <ListItemText primary="Use Current Location" sx={{ color: '#0688DB' }} />
                        </ListItemButton>
                    </ListItem>
                    {suggestions.map((suggestion, index) => (
                        <ListItem key={index} disablePadding>
                            <ListItemButton onClick={() => handleSuggestionClick(suggestion.description)}>
                                <ListItemText primary={suggestion.description} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            )}
        </Paper>
    );
}

export default MobileSearchBar;