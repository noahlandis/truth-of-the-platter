import SearchBar from "./SearchBar";
import logo from './assets/logo.svg'; // Adjust the path based on your folder structure
import { Link } from 'react-router-dom'; // Import Link from react-router-dom



function Header() {
    return (
        <div className="flex flex-col items-center">
            <span className="flex items-center mb-2">
            <Link to="/" className="flex items-center"> {/* Add flex and alignment classes */}
                <img src={logo} alt="Logo" width="100" height="100" />
                <div className="ml-2 text-4xl font-abel">Truth of the Platter</div>
            </Link>
            </span>
            <SearchBar />
        </div>
    );
}

export default Header;