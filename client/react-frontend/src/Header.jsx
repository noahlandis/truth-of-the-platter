import React, { useState, useRef, useEffect } from 'react';
import SearchBar from "./SearchBar";
import MobileSearchBar from "./MobileSearchBar";
import logo from './assets/logo.svg'; // Adjust the path based on your folder structure
import { Link, useLocation } from 'react-router-dom'; // Import useLocation
import useMediaQuery from '@mui/material/useMediaQuery';
import { Button, ClickAwayListener } from '@mui/material';

function Header() {
    const location = useLocation(); // Get current location
    const isMobile = useMediaQuery('(max-width:600px)');
    const [isSearchFocused, setIsSearchFocused] = useState(false);
    const cancelSearchRef = useRef(null);

    // Add this useEffect to listen for route changes
    useEffect(() => {
        handleCancel();
    }, [location]);

    const handleCancel = () => {
        setIsSearchFocused(false);
        if (cancelSearchRef.current) {
            cancelSearchRef.current();
        }
    };

    const handleClickAway = () => {
        setIsSearchFocused(false);
        if (cancelSearchRef.current) {
            cancelSearchRef.current();
        }
    };

    return (
        <div className="flex flex-col items-center w-full">
            <ClickAwayListener onClickAway={handleClickAway}>
                <div className={`flex flex-col items-center w-full`}>
                    <div className={`flex items-center justify-between w-full ${isMobile ? 'px-2' : ''}`}>
                        {isMobile && isSearchFocused && (
                            <Button 
                                onClick={handleCancel}
                                variant="text" 
                                size="small"
                            >
                                Cancel
                            </Button>
                        )}
                        <Link to="/" className="flex items-center justify-center flex-grow">
                            <img 
                                src={logo} 
                                alt="Logo" 
                                className={`${isMobile ? 'w-12 h-12' : 'w-16 h-16 md:w-24 md:h-24'}`}
                            />
                            <div className={`ml-2 font-abel ${isMobile ? 'text-sm' : 'text-2xl md:text-4xl'}`}>
                                Truth of the Platter
                            </div>
                        </Link>
                        {isMobile && isSearchFocused && (
                            <Button 
                                type="submit" 
                                form="mobile-search-form" 
                                variant="text" 
                                size="small"
                            >
                                Search
                            </Button>
                        )}
                    </div>
                    {location.pathname !== '/terms' && (
                        isMobile ? (
                            <MobileSearchBar 
                                onFocus={() => setIsSearchFocused(true)}
                                onBlur={() => setIsSearchFocused(false)} // Add this line
                                cancelSearchRef={cancelSearchRef}
                            />
                        ) : (
                            <SearchBar />
                        )
                    )}
                </div>
            </ClickAwayListener>
        </div>
    );
}

export default Header;
