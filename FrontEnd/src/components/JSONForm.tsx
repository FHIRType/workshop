import { useState } from 'react';

const JSONForm = () => {
    const [jsonBody, setJsonBody] = useState<string>('');

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setJsonBody(e.target.value);
    };

    const handleClear = () => {
        setJsonBody('');
    };

    return (
        <div className="w-full h-full flex flex-col items-center justify-center">
            <div className="bg-white border-1 border-pacific-gray flex flex-col p-8 rounded-lg gap-2 w-[80vw]">
                <textarea
                    onChange={(e) => {
                        handleChange(e);
                    }}
                    placeholder="Copy and paste your JSON"
                    value={jsonBody}
                    className="text-white outline-none w-full h-[45vh] bg-[#292524] resize-none rounded-md border border-pacific-gray p-3"
                />
                <div className="flex flex-row gap-4 justify-center items-center mt-4">
                    <button
                        onClick={(e) => {
                            e.preventDefault();
                        }}
                        className="min-w-[100px] bg-pacific-blue text-white px-6 py-2 rounded drop-shadow-md hover:bg-pacific-light-blue transition ease-in-out">
                        Confirm
                    </button>
                    <button
                        className="min-w-[100px] bg-white outline-2 outline outline-offset-[-2px] outline-pacific-blue text-pacific-blue px-6 py-2 rounded drop-shadow-md hover:bg-pacific-blue hover:text-white transition ease-in-out"
                        onClick={handleClear}>
                        Clear
                    </button>
                </div>
            </div>
        </div>
    );
};

export default JSONForm;
