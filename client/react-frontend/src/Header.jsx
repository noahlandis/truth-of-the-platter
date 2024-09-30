import SearchBar from "./SearchBar";
import logo from './assets/logo.svg'; // Adjust the path based on your folder structure
import { Link, useLocation } from 'react-router-dom'; // Import useLocation

function Header() {
    const location = useLocation(); // Get current location

    return (
        <div className="flex flex-col items-center">
            <span className="flex items-center mb-2">
                <Link to="/" className="flex items-center">
                    <img 
                        src={logo} 
                        alt="Logo" 
                        className="w-16 h-16 md:w-24 md:h-24" // Adjust size for mobile and larger screens
                    />
                    <div className="ml-2 text-2xl md:text-4xl font-abel">Truth of the Platter</div> {/* Smaller text on mobile */}
                </Link>
            </span>
            {location.pathname !== '/terms' && <SearchBar />} {/* Conditionally render SearchBar */}
        </div>
    );
}

export default Header;
