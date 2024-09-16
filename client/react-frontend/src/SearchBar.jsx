import React, { useState, useEffect, useRef } from 'react';
import { Paper, InputBase, IconButton, Box, List, ListItem, ListItemButton, ListItemText, Typography } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import axios from 'axios';
import { useSearchParams } from "react-router-dom";
import { useNavigate } from 'react-router-dom';

function SearchBar() {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();

    // State for name, location, suggestions, and error
    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [error, setError] = useState(''); // Error state

    // Ref for storing timeout ID for debouncing
    const debounceTimeoutRef = useRef(null);

    // On component mount, populate input fields from query params
    useEffect(() => {
        const initialName = searchParams.get('name') || '';
        const initialLocation = searchParams.get('location') || '';

        setName(initialName);
        setLocation(initialLocation);
    }, []);

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
        // Debounced API call
        if (location.length > 0) {
            if (debounceTimeoutRef.current) {
                clearTimeout(debounceTimeoutRef.current);
            }

            debounceTimeoutRef.current = setTimeout(async () => {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/autocomplete', {
                        params: { text: location },
                    });
                    console.log('API called');
                    response.data.predictions = response.data.predictions.map((suggestion) => {
                        suggestion.description = suggestion.description.replace(/, USA$/, '');
                        return suggestion;
                    });
                    setSuggestions(response.data.predictions);
                } catch (error) {
                    console.error('Error fetching location suggestions:', error);
                }
            }, 200); // 300ms debounce delay
        } else {
            setSuggestions([]);
        }
        // Cleanup timeout on unmount or when location changes
        return () => {
            if (debounceTimeoutRef.current) {
                clearTimeout(debounceTimeoutRef.current);
            }
        };
    }, [location]);

    const handleLocationChange = (e) => {
        setLocation(e.target.value);
        setShowSuggestions(true);
    };

    const handleUserLocationClick = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/user-location');
            setLocation(response.data);
            setShowSuggestions(false);
            return response.data;
        } catch (error) {
            console.error('Error fetching user location:', error);
        }
    };

    // Handle search and navigate with query params
    const handleSearch = async (e) => {
        e.preventDefault();

        // Check if name is empty and set error if true
        if (!name.trim()) {
            setError('Name field cannot be left blank');
            return; // Prevent form submission
        }
        let searchLocation = location;
        if (!location.trim()) {
            searchLocation = await handleUserLocationClick();
        }


        setError(''); // Clear error if validation passes
        navigate(`/search?name=${name}&location=${searchLocation}`);
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
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Name"
                        sx={{
                            ml: 2,
                            width: '100%',
                            flex: 1,
                        }}
                        inputProps={{ 'aria-label': 'name' }}
                    />

                    {error && (
                        <Typography
                            color="error"
                            sx={{
                                position: 'absolute',
                                bottom: '-15px', // Adjust this value to control the spacing
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

                    {/* Display error message if name is empty */}

                </Box>


                <Box sx={{ position: 'relative', flex: 1 }}>
                    <InputBase
                        value={location}
                        onChange={handleLocationChange}
                        onFocus={handleFocus}
                        onBlur={handleBlur}
                        placeholder="Location"
                        sx={{
                            ml: 2,
                            flex: 1,
                            width: '100%',
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
                    {showSuggestions && (
                        <List
                            sx={{
                                position: 'absolute',
                                top: '97%',
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


// <List
// sx={{
//   position: 'absolute',
//   top: '100%',
//   left: 0,
//   right: 0, // Ensures it spans the full width of the location input
//   width: '100%', // Ensures full width
//   backgroundColor: '#fff',
//   boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
//   zIndex: 1,
//   maxHeight: 200,
//   overflowY: 'auto',
//   borderRadius: '0 0 8px 8px',
// }}
// >
// {['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'].map((suggestion, index) => (
//   <ListItem key={index} disablePadding>
//     <ListItemButton onClick={() => handleSuggestionClick(suggestion)}>
//       <ListItemText primary={suggestion} />
//     </ListItemButton>
//   </ListItem>
// ))}
// </List>
// <List
// sx={{
//   position: 'absolute',
//   top: '100%',
//   left: 0,
//   right: 0, // Ensures it spans the full width of the location input
//   width: '100%', // Ensures full width
//   backgroundColor: '#fff',
//   boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
//   zIndex: 1,
//   maxHeight: 200,
//   overflowY: 'auto',
//   borderRadius: '0 0 8px 8px',
// }}
// >
// {['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'].map((suggestion, index) => (
//   <ListItem key={index} disablePadding>
//     <ListItemButton onClick={() => handleSuggestionClick(suggestion)}>
//       <ListItemText primary={suggestion} />
//     </ListItemButton>
//   </ListItem>
// ))}
// </List>