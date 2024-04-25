import React from "react";

import {Input, Button} from "@nextui-org/react";

export default function GetDataForm ( { data, setData, handleSubmit, handleClear, isLoading } ) {
    const handleChange = (value: string, field: keyof typeof data) => {
        setData({
            ...data,
            [field]: value
        });
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-gray-200 flex flex-col my-3 p-8 shadow-lg rounded-xl gap-2"
        >
            <Input type="text" variant={"underlined"} label="First Name" placeholder="John"
                   value={data.firstName}
                   onChange={(e) => handleChange(e.target.value, 'firstName')}
            />
            <Input
                type={"text"} variant={"underlined"} label={"Last name"} placeholder={"Doe"}
                value={data.lastName}
                onChange={(e) => handleChange(e.target.value, 'lastName')}
            />
            <Input
                type={"text"} variant={"underlined"} label={"NPI"} placeholder={"1234567890"}
                value={data.npi}
                onChange={(e) => handleChange(e.target.value, 'npi')}
            />
            <div className="flex flex-row justify-center gap-2">
                <Button color="primary" variant="shadow" type={"submit"} isLoading={isLoading}>
                    Submit
                </Button>
                <Button color="primary" variant="ghost" onClick={handleClear}>
                    Clear
                </Button>
            </div>
        </form>
    );
}