import React, { useRef, useState } from 'react';
import { FiUpload } from 'react-icons/fi';
import { queryPropInit, QueryProps } from '../static/types';
import { Button } from '@nextui-org/react';

type _QueryProps = {
    setQueryBody: (data: FileDataState) => void;
    isLoading: boolean;
};

type FileDataState = QueryProps | boolean;

const FileForm = ({ setQueryBody, isLoading }: _QueryProps) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [csvFileName, setCsvFileName] = useState<string | null>(null);
    const [invalidFile, setInvalidFile] = useState<boolean>(false);
    const [fileSize, setFileSize] = useState<number>(0);
    const [fileData, setFileData] = useState<FileDataState>(queryPropInit);

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files ? e.target.files[0] : null;
        if (!selectedFile) return;

        const fileType = selectedFile.type;
        const allowedTypes = ['text/csv', 'application/vnd.ms-excel', 'application/json'];

        if (!allowedTypes.includes(fileType)) {
            //alert("Can only upload CSV or JSON files");
            setInvalidFile(true);
            return;
        }
        setInvalidFile(false);
        setCsvFileName(selectedFile.name);
        setFileSize(selectedFile.size);
        parseFile(selectedFile, fileType);
    };

    const parseFile = (file: File, fileType: string) => {
        const reader = new FileReader();
        reader.onload = (event: ProgressEvent<FileReader>) => {
            const contents = event.target?.result as string;

            if (fileType.includes('json')) {
                const jsonData = JSON.parse(contents);
                if (isValidJson(jsonData)) {
                    setInvalidFile(false);
                    setFileData(jsonData);
                } else {
                    setInvalidFile(true)
                    alert("The JSON file did not match the required format!")
                }
            } else if (fileType.includes('csv')) {
                const csvData = parseCSV(contents);
                if (csvData) {
                    setInvalidFile(false)
                    setFileData(csvData);
                } else {
                    setInvalidFile(true)
                    alert("The CSV file did not match the required format!")
                }
            }
        };

        reader.onerror = (error) => {
            console.error('File reading error:', error);
        };
        reader.readAsText(file);
    };

    const handleSubmit = () => {
        // Trigger the submission of parsed practitioners' data
        console.log("clicked submit: ", fileData)
        setQueryBody(fileData);
    };

    // Function to open file browser when "Upload File" button is clicked
    const openFileBrowser = () => {
        fileInputRef.current?.click();
    };

    // Function to remove uploaded file
    const removeFile = () => {
        setCsvFileName(null); // Clear the file name
        setInvalidFile(false)
        // Reset the file input element
        if (fileInputRef.current) {
            fileInputRef.current.value = ''; // Clear the file input
        }
    };

    return (
        <div className="flex flex-1 pr-10">
            <div className="flex flex-col justify-center w-full bg-pacific-light-gray border rounded-lg flex flex-col items-center">
                {!csvFileName && (
                    <>
                        <FiUpload className="text-4xl mb-2 hover:cursor-pointer" onClick={openFileBrowser} />
                        <button className="text-lg">Click on the icon to upload a file</button>
                    </>
                )}
                <input
                    ref={fileInputRef}
                    id="fileInput"
                    type="file"
                    style={{ display: 'none' }}
                    onChange={handleFileSelect}
                />
                {invalidFile && <p className="text-red-500">Invalid file format</p>}
                {!csvFileName && (
                    <Button
                        onClick={openFileBrowser}
                        color="primary"
                        variant="shadow"
                        isLoading={isLoading}
                        className="bg-blue-500 text-white px-4 py-2 rounded mt-2">
                        Upload
                    </Button>
                )}
                {csvFileName && (
                    <div className={"flex flex-col justify-center items-center"}>
                        <p className={"text-[calc(1.3vw+0.5em)] text-center"}>
                            File uploaded: {csvFileName} (Size: {fileSize} bytes)
                        </p>
                        <div className={"flex flex-row gap-10"}>
                            {csvFileName && (
                                <Button
                                    color="primary" onClick={removeFile}
                                    className="bg-red-400 text-black px-4 py-2 rounded mt-2">
                                    Remove File
                                </Button>
                            )}
                            <Button
                                onClick={handleSubmit}
                                color="primary"
                                variant="shadow"
                                isLoading={isLoading}
                                isDisabled={invalidFile}
                                className="bg-blue-500 text-white px-4 py-2 rounded mt-2">
                                Submit
                            </Button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default FileForm;

interface Practitioner {
    first_name: string;
    last_name: string;
    npi: string;
}

interface ParsedCSV {
    practitioners: Practitioner[];
}

const parseCSV = (csvText: string): ParsedCSV | false => {
    const lines = csvText.split(/\r?\n/).filter((line) => line); // split and filter out empty lines
    const headers = lines[0].split(',').map((header) => header.trim()); // headers

    // Check if headers are as expected
    if (
        headers.length !== 3 ||
        headers[0] !== 'first_name' ||
        headers[1] !== 'last_name' ||
        headers[2] !== 'npi'
    ) {
        return false;
    }

    const practitioners = lines.slice(1).reduce<Practitioner[]>((acc, line) => {
        const data = line.split(',');
        if (data.length === 3 && data[0] && data[1] && data[2] && data[2].length === 10) {
            acc.push({
                first_name: data[0].trim(),
                last_name: data[1].trim(),
                npi: data[2].trim(),
            });
        }
        return acc;
    }, []);

    return { practitioners };
};


const isValidJson = (jsonData: any): boolean => {
    if (jsonData && jsonData.practitioners && Array.isArray(jsonData.practitioners)) {
        for (const practitioner of jsonData.practitioners) {
            if (
                !practitioner ||
                typeof practitioner.npi !== 'string' ||
                typeof practitioner.first_name !== 'string' ||
                typeof practitioner.last_name !== 'string'
            ) {
                return false;
            }
        }
        return true;
    }
    return false;
};
