import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="mt-auto ">
      <div className="container pb-4 mx-auto text-center">
        <Link to="/terms" className="text-black  hover:text-blue-800">
          Terms of Service
        </Link>
      </div>
    </footer>
  );
}

export default Footer;