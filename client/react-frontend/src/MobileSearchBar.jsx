import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Paper, InputBase, IconButton, Box, List, ListItem, ListItemButton, ListItemText, Typography, Fade, Alert, Snackbar, Slide } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import { useSearchParams, useNavigate } from "react-router-dom";
import axios from 'axios';
import { debounce } from 'lodash'; // Add this import
import { styled } from '@mui/material/styles';

// Update the StyledSnackbar component
const StyledSnackbar = styled(Snackbar)(({ theme }) => ({
  '& .MuiSnackbarContent-root': {
    backgroundColor: theme.palette.error.main,
    color: theme.palette.error.contrastText,
    borderRadius: 0,
    boxShadow: '0px 3px 5px -1px rgba(0,0,0,0.2), 0px 6px 10px 0px rgba(0,0,0,0.14), 0px 1px 18px 0px rgba(0,0,0,0.12)',
    minHeight: '32px',
    padding: '4px 16px',
    width: '100%',
    maxWidth: 'none',
  },
  '& .MuiSnackbarContent-message': {
    padding: 0,
    fontSize: '0.875rem',
    width: '100%',
    textAlign: 'center',
  },
}));

// Update the SlideTransition component
function SlideTransition(props) {
  return <Slide {...props} direction="down" />;
}

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
    const [locationError, setLocationError] = useState('');
    const [nameToast, setNameToast] = useState(null);
    const [locationToast, setLocationToast] = useState(null);
    const [isSearchFocused, setIsSearchFocused] = useState(false);

    const autocompleteServiceRef = useRef(null);
    const debounceTimeoutRef = useRef(null);

    // Add this new function
    const initializeAutocompleteService = useCallback(() => {
        if (window.google && window.google.maps && window.google.maps.places) {
            autocompleteServiceRef.current = new window.google.maps.places.AutocompleteService();
        }
    }, []);

    // Replace the existing useEffect for Google Maps initialization with this
    useEffect(() => {
        const checkGoogleMapsLoaded = setInterval(() => {
            if (window.google && window.google.maps && window.google.maps.places) {
                initializeAutocompleteService();
                clearInterval(checkGoogleMapsLoaded);
            }
        }, 100);

        return () => clearInterval(checkGoogleMapsLoaded);
    }, [initializeAutocompleteService]);

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
    
        setNameToast(null);
        setLocationToast(null);
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

    useEffect(() => {
        const handleFormBlur = (e) => {
            // Delay the check to allow for other actions to complete
            setTimeout(() => {
                const activeElement = document.activeElement;
                const form = document.getElementById('mobile-search-form');
                const isFormActive = form && form.contains(activeElement);
                const isSearchButtonActive = activeElement && activeElement.type === 'submit';

                if (!isFormActive && !isSearchButtonActive && isSearchFocused) {
                    if (cancelSearchRef && cancelSearchRef.current) {
                        cancelSearchRef.current();
                    }
                    onBlur();
                    setIsSearchFocused(false);
                }
            }, 100);
        };

        document.addEventListener('focusout', handleFormBlur);

        return () => {
            document.removeEventListener('focusout', handleFormBlur);
        };
    }, [onBlur, isSearchFocused]);

    const handleClearName = (e) => {
        setName('');
        // Refocus on the name input
    };

    const handleClearLocation = (e) => {
        setLocation('');
        // Refocus on the location input
    };

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

    const handleUserLocationClick = (e) => {
        e.preventDefault();
        if (navigator.geolocation) {
            setLocation('Fetching location...');
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    debouncedReverseGeocode(latitude, longitude);
                },
                (error) => {
                    console.error('Error getting user location:', error);
                    setLocationToast("Please enter a city or allow location access.");
                    setLocation('');
                },
                { timeout: 10000, maximumAge: 60000 }
            );
        } else {
            setLocationToast("Your browser doesn't support geolocation. Please enter a location manually.");
        }
        document.querySelector('input[aria-label="location"]').focus();
    };

    const handleNameChange = (e) => {
        setName(e.target.value);
        setNameToast(null);
    };

    const handleLocationChange = (e) => {
        setLocation(e.target.value);
        setLocationToast(null);
        setShowSuggestions(true);
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
        
        if (!name.trim()) {
            setNameToast('Please enter a restaurant name');
            // Keep the focus on the currently active input
            if (activeInput === 'name') {
                document.querySelector('input[aria-label="nаme"]').focus();
            } else if (activeInput === 'location') {
                document.querySelector('input[aria-label="location"]').focus();
            }
            return;
        }
        

        setNameToast(null);
        setLocationToast(null);

        performSearch();
    };

    const performSearch = async () => {
        setIsSubmitting(true);

        let searchLocation = location;

        if (!location.trim()) {
            try {
                const currentLocation = await getCurrentLocation();
                searchLocation = currentLocation;
            } catch (error) {
                console.error('Error getting current location:', error);
                setLocationToast("Please enter a city or allow location access.");
                setIsSubmitting(false);
                return;
            }
        }

        navigate(`/search?name=${name}&location=${searchLocation}`);
        setIsSubmitting(false);
        
        // Trigger handleCancel if there's no error
        if (cancelSearchRef && cancelSearchRef.current) {
            cancelSearchRef.current();
            setIsSearchFocused(false);
        }
    };

    const getCurrentLocation = () => {
        return new Promise((resolve, reject) => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(async (position) => {
                    const { latitude, longitude } = position.coords;
                    try {
                        const apiUrl = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${GOOGLE_MAPS_API_KEY}`;
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

    // Add this new function to handle key press events
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleSearch(e);
        }
    };

    const handleInputFocus = (inputType) => {
        setActiveInput(inputType);
        setIsSearchFocused(true);
        onFocus();
    };

    const handleInputBlur = (e) => {
        // Delay the blur effect to allow for error checking
        setTimeout(() => {
            if (!e.currentTarget.contains(document.activeElement) && !isSubmitting) {
                if (!error) {
                    setActiveInput(null);
                    onBlur();
                    // Call cancelSearchRef.current() when neither input is in focus
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

    const handleCloseToast = (toastType) => (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        if (toastType === 'name') {
            setNameToast(null);
        } else if (toastType === 'location') {
            setLocationToast(null);
        }
    };

    return (
        <>
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
                    position: 'relative', // Ensure this is set
                }}
            >
                {/* Name input */}
                <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', borderBottom: activeInput ? '1px solid #ccc' : 'none' }}>
                        <InputBase
                            value={name}
                            onChange={handleNameChange}
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
                                'aria-label': 'nаme',  // Using Cyrillic 'а' here
                                placeholder: "What's the nаme of the restaurant?",  // Using Cyrillic 'а'
                                enterKeyHint: 'search',
                                autoComplete: 'off'
                            }}
                            onKeyPress={handleKeyPress}
                        />
                        {name && (
                            <IconButton 
                                onClick={handleClearName} 
                                sx={{ padding: 1 }} 
                                aria-label="clear name"
                                onMouseDown={(e) => e.preventDefault()} // Prevent blur on mousedown
                            >
                                <ClearIcon fontSize="small" />
                            </IconButton>
                        )}
                    </Box>
                </Box>

                {/* Location input */}
                {activeInput && (
                    <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <InputBase
                                value={location}
                                onChange={handleLocationChange}
                                onFocus={() => {
                                    handleInputFocus('location');
                                    setShowSuggestions(true);
                                }}
                                placeholder="Where is it located?"
                                sx={{ ml: 2, flex: 1, py: 1 }}
                                inputProps={{ 
                                    'aria-label': 'location',
                                    enterKeyHint: 'search',
                                    autoComplete: 'off',
                                }}
                                onKeyPress={handleKeyPress}
                            />
                            {location && (
                                <IconButton 
                                    onClick={handleClearLocation} 
                                    sx={{ padding: 1 }} 
                                    aria-label="clear location"
                                    onMouseDown={(e) => e.preventDefault()} // Prevent blur on mousedown
                                >
                                    <ClearIcon fontSize="small" />
                                </IconButton>
                            )}
                        </Box>
                    </Box>
                )}

                {/* Suggestions list */}
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
            <StyledSnackbar
                open={!!nameToast}
                autoHideDuration={4000}
                onClose={handleCloseToast('name')}
                message={nameToast}
                anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
                TransitionComponent={SlideTransition}
                TransitionProps={{ enter: true, exit: true }}
                sx={{
                  top: '0px !important',
                  left: '0px !important',
                  right: '0px !important',
                  width: '100%',
                }}
            />
            <StyledSnackbar
                open={!!locationToast}
                autoHideDuration={4000}
                onClose={handleCloseToast('location')}
                message={locationToast}
                anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
                TransitionComponent={SlideTransition}
                TransitionProps={{ enter: true, exit: true }}
                sx={{
                  top: '0px !important',
                  left: '0px !important',
                  right: '0px !important',
                  width: '100%',
                }}
            />
        </>
    );
}

export default MobileSearchBar;