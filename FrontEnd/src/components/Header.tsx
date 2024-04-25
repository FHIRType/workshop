import { menus } from "../static/menus"
import {Outlet, NavLink} from "react-router-dom";
import pacificsource from "/pacificsource.svg"

export default function Header() {
    return (
        <div className="w-full h-[5%] flex flex-col">
            <img src={pacificsource}
                 className={"w-[20vw]"}
                 onClick={() => window.location.href = "/"}
            />
            <Outlet />
        </div>
    );
}