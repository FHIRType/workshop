import {
   ComponentProps,
   FC,
   MouseEventHandler,
   ReactNode,
   SetStateAction,
} from "react";
import { cn } from "../utils/tailwind-utils";

type ButtonProps = ComponentProps<"button"> & {
   children: ReactNode;
   className?: string;
   onClick?: MouseEventHandler | SetStateAction<Selection>;
};

const Button: FC<ButtonProps> = ({ className, children, onClick }) => {
   return (
      <button
         className={cn(
            "px-5 py-2 font-roboto bg-pacific-blue font-semibold rounded-md border border-[#c7c7d4] hover:bg-[#ceddf0] transition ease-in-out",
            className
         )}
         onClick={onClick}
      >
         {children}
      </button>
   );
};

export default Button;
