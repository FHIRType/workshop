import { Link } from 'react-router-dom';
import pacificsource from '/pacificsource.svg';

const Navbar = () => {
    return (
        <div className="w-full bg-white fixed flex flex-row px-6 py-4 border-b-1 border-pacific-gray justify-between z-50">
            <img
                src={pacificsource}
                alt="pacific source"
                className={'w-[calc(10vw+5em)] self-center hover:cursor-pointer select-none'}
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
