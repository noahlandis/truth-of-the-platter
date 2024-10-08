import React, { useState, useEffect, useRef } from 'react';
import { Paper, InputBase, IconButton, Box, List, ListItem, ListItemButton, ListItemText, Typography, Fade } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import { useSearchParams, useNavigate } from "react-router-dom";

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
                setName('');
                setLocation('');
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
    };

    const handleLocationChange = (e) => {
        setLocation(e.target.value);
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

    const handleUserLocationClick = async () => {
        // ... (keep the existing handleUserLocationClick function)
    };

    const handleSearch = (e) => {
        e.preventDefault();
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
                    }}
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
                        onFocus={() => handleInputFocus('location')}
                        placeholder="Location"
                        sx={{ ml: 2, flex: 1, py: 1 }}
                        inputProps={{ 'aria-label': 'location' }}
                    />
                    {location && (
                        <IconButton onClick={handleClearLocation} sx={{ padding: 1 }} aria-label="clear location">
                            <ClearIcon fontSize="small" />
                        </IconButton>
                    )}
                </Box>
            )}
            {activeInput === 'location' && suggestions.length > 0 && (
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
