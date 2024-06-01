import {Snippet, Textarea} from "@nextui-org/react";

// DO NOT LINT OR CHANGE THIS FORMAT
const jsonFormat = `{
    "practitioners": [
        {
          "npi": "string",
          "first_name": "string",
          "last_name": "string"
        }
    ]
}`

export const RequiredFormat = ()  => {
    return (
        <div className={"relative grid grid-cols-8 min-w-[100%] text-white"}>
            <Textarea
                isReadOnly={true}
                label={"Required Format"}
                variant={"bordered"}
                color={"warning"}
                labelPlacement={"inside"}
                defaultValue={jsonFormat}
                className={"max-w bg-json rounded-[15px] text-white col-span-8"}
                minRows={20}
            />
            <Snippet hideSymbol={true} variant={"flat"} className={"absolute bg-inherit col-span-0 text-white w-full"}>
                <p className={"hidden"}>{jsonFormat}</p>
            </Snippet>
        </div>
    )
}
