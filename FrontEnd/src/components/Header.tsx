import Button from "./Button";
import { menus } from "../static/menus.ts"

export default function Header() {
    return (
        <div className="h-full w-full bg-[#f7f9fc] flex flex-col justify-center items-center font-roboto p-16">
            <h1 className="select-none cursor-default text-[#1b2330] py-3 text-5xl font-bold">
                FHIR API
            </h1>
            <div className="flex flex-row gap-2 py-4">
                {menus.map((menu, index) => {
                    return (
                        <Button key={index} >
                            {menu.name}
                        </Button>
                    );
                })}
            </div>
        </div>
    );
}