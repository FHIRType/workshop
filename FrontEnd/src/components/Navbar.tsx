import { Link } from 'react-router-dom';
import capstone from "/capstone.svg"

const Navbar = () => {
    return (
        <div className="w-full bg-white fixed flex flex-row px-6 py-4 border-b-1 border-pacific-gray justify-between z-50">
            <img
                src={capstone}
                alt="pacific source"
                className={'w-[calc(12vw+10em)] self-center hover:cursor-pointer select-none'}
                onClick={() => (window.location.href = '/')}
            />
            <div className="flex flex-row gap-8">
                <Link to="/about" className="text-[calc(0.2vw+1em)] self-center text-pacific-blue">
                    About
                </Link>
                <Link to="/" className="text-[calc(0.2vw+1em)] self-center text-pacific-blue">
                    API
                </Link>
            </div>
        </div>
    );
};

export default Navbar;
