import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="mt-auto ">
      <div className="container pb-4 mx-auto text-center">
        <Link to="/terms" className="mr-4 text-black">
          Terms of Service
        </Link>
        <a href="mailto:noahlandis980@gmail.com" className="text-black">
          Contact
        </a>
      </div>
    </footer>
  );
}

export default Footer;