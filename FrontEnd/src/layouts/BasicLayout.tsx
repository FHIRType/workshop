import {ComponentProps, FC} from "react";
import {cn} from "../utils/tailwind-utils.ts";
import Navbar from "../components/Navbar.tsx";
import {Outlet} from "react-router-dom";

type LayoutProps = ComponentProps<'div'> & {
    className?: string;
};

const BasicLayout: FC<LayoutProps> = ({className}) => {
    return (
        <div className={cn("h-full w-full flex-col font-roboto", className)}>
            <Navbar />
            <Outlet />
        </div>
    );
};

export default BasicLayout;