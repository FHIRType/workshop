import capstone from "/capstone.svg"
import {Link} from "@nextui-org/react";

const Navbar = () => {
    return (
        <div className="w-full bg-white fixed shadow-sm flex flex-row px-6 py-4 border-b-1 border-pacific-gray justify-between z-50">
            <img
                src={capstone}
                alt="pacific source"
                className={'w-[calc(12vw+10em)] self-center hover:cursor-pointer select-none'}
                onClick={() => (window.location.href = '/')}
            />
            <div className="flex flex-row gap-8">
                <Link href="/about" className="text-[calc(0.2vw+1em)] self-center text-pacific-blue">
                    About
                </Link>
                <Link href="/" className="text-[calc(0.2vw+1em)] self-center text-pacific-blue">
                    API
                </Link>
            </div>
        </div>
    );
};

export default Navbar;
