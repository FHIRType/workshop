import { useState } from 'react';
import { QueryProps } from '../static/types';
import { Button } from '@nextui-org/react';

type _QueryProps = {
    setQueryBody: (data: QueryProps) => void;
    isLoading: boolean;
};

const JSONForm = ({ setQueryBody, isLoading }: _QueryProps) => {
    const [jsonBody, setJsonBody] = useState<string>('');

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setJsonBody(e.target.value);
    };

    const handleClear = () => {
        setJsonBody('');
    };

    const handleSubmit = () => {
        try {
            const jsonData: QueryProps = JSON.parse(jsonBody);
            console.log('Parsed JSON body: ', jsonData);
            setQueryBody(jsonData);
        } catch (error) {
            console.error('Failed to parse JSON:', error);
            alert('Invalid JSON format. Please check your input and try again.');
        }
    };

    return (
        <div className={"flex flex-1 pr-10"}>
            <div className="flex flex-col w-full">
                <textarea
                    onChange={handleChange}
                    placeholder="Copy and paste your JSON"
                    value={jsonBody}
                    className="text-white outline-none w-full h-[45vh] bg-[#292524] resize-none rounded-md border border-pacific-gray p-3"
                />
                <div className="flex flex-row gap-4 justify-center items-center mt-4">
                    <Button
                        color="primary"
                        variant="shadow"
                        isLoading={isLoading}
                        onClick={handleSubmit}
                        className="min-w-[100px] bg-pacific-blue text-white px-6 py-2 rounded drop-shadow-md hover:bg-pacific-light-blue transition ease-in-out">
                        Confirm
                    </Button>
                    <Button
                        color="primary"
                        variant="ghost"
                        className="min-w-[100px] bg-white outline-2 outline outline-offset-[-2px] outline-pacific-blue text-pacific-blue px-6 py-2 rounded drop-shadow-md hover:bg-pacific-blue hover:text-white transition ease-in-out"
                        onClick={handleClear}>
                        Clear
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default JSONForm;
