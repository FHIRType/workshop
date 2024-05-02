import pacificsource from "/pacificsource.svg"

const Navbar = () => {
    return (
        <div className="w-full bg-white flex flex-col p-5 border-b-1 border-pacific-gray">
            <img src={pacificsource}
                 alt="pacific source"
                 className={"w-[calc(10vw+5em)] self-center hover:cursor-pointer select-none"}
                 onClick={() => window.location.href = "/"}
            />
        </div>
    );
};

export default Navbar;