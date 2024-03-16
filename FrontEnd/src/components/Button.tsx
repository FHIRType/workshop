import {
   ComponentProps,
   FC,
   MouseEventHandler,
   ReactNode,
   SetStateAction,
} from "react";
import { cn } from "../lib/tailwind-utils";

type ButtonProps = ComponentProps<"button"> & {
   children: ReactNode;
   className?: string;
   onClick?: MouseEventHandler | SetStateAction<Selection>;
};

const Button: FC<ButtonProps> = ({ className, children, onClick }) => {
   return (
      <button
         className={cn("px-3 py-1 font-roboto", className)}
         onClick={onClick}
      >
         {children}
      </button>
   );
};

export default Button;
