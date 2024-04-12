import React from "react";

export default function GetDataForm ( { data, setData, handleSubmit, handleClear } ) {
    const handleChange = (value: string, field: keyof typeof data) => {
        setData({
            ...data,
            [field]: value
        });
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white flex flex-col my-3 p-8 shadow-lg rounded-xl gap-2"
        >
            <input
                className="input"
                value={data.firstName}
                onChange={(e) => handleChange(e.target.value, 'firstName')}
                placeholder="Enter First Name"
            />
            <input
                className="input"
                value={data.lastName}
                onChange={(e) => handleChange(e.target.value, 'lastName')}
                placeholder="Enter Last Name"
            />
            <input
                className="input"
                value={data.npi}
                onChange={(e) => handleChange(e.target.value, 'npi')}
                placeholder="Enter NPI"
            />
            <div className="flex flex-row justify-center gap-2">
                <button className="button" type="submit">
                    Search
                </button>
                <button
                    className="button"
                    type="button"
                    onClick={handleClear}
                >
                    Clear
                </button>
            </div>
        </form>
    );
}