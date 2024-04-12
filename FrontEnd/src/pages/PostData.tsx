import React, {useState} from "react";
import Button from "../components/Button.tsx";
import {menus} from "../static/menus";
import {Selection} from "../static/types.ts";

export default function PostData() {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    //const [NPI, setNPI] = useState("");
    const [selection, setSelection] = useState<Selection>({
      name: "",
      type: "",
      baseURL: "",
      description: [],
   });

    const RenderContent = () => {
            return (
                <React.Fragment>
                     <h2 className="select-none font-bold text-2xl pt-5 pb-2 text-[#21253b]">
                        {selection.name}
                    </h2>
                    <div className="pb-4">
                        {selection.description.map((desc, index) => {
                           return (
                               <div key={index+desc} className="select-none text-sm text-[#4a4b4f]">
                                  {desc}
                               </div>
                           );
                        })}
                    </div>

                    <form>
                        <h1>NPI:</h1>
                        <input
                            className="input"
                            value={firstName}
                            placeholder="Enter First Name"
                        />
                         <input
                            className="input"
                            value={lastName}
                            placeholder="Enter Last Name"
                         />
                    </form>

                    <form>
                        <h1>NPI:</h1>
                        <input
                            className="input"
                            value={firstName}
                            placeholder="Enter First Name"
                        />
                         <input
                            className="input"
                            value={lastName}
                            placeholder="Enter Last Name"
                         />
                    </form>

                    <form>
                        <h1>NPI:</h1>
                        <input
                            className="input"
                            value={firstName}
                            placeholder="Enter First Name"
                        />
                         <input
                            className="input"
                            value={lastName}
                            placeholder="Enter Last Name"
                         />
                    </form>

                </React.Fragment>

        )
    }


    return (
       <div className="h-full w-full bg-[#f7f9fc] flex flex-col justify-center items-center font-roboto p-16">
          <div className="flex flex-row gap-2 py-4">
                <Button onClick={() => {console.log(menus[1]); setSelection(menus[1])}}>
                   {menus[1].name}
                </Button>
          </div>
          {selection.name.length != 0 && RenderContent()}
       </div>
   )
}