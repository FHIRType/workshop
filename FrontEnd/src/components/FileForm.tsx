import React, { useRef, useState } from 'react';
import { FiUpload } from 'react-icons/fi';
import { queryPropInit, QueryProps } from '../static/types';
import { Button } from '@nextui-org/react';

type _QueryProps = {
    setQueryBody: (data: QueryProps) => void;
    isLoading: boolean;
};

const FileForm = ({ setQueryBody, isLoading }: _QueryProps) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [csvFileName, setCsvFileName] = useState<string | null>(null);
    const [invalidFormat, setInvalidFormat] = useState<boolean>(false);
    const [invalidFile, setInvalidFile] = useState<boolean>(false);
    const [fileSize, setFileSize] = useState<number>(0);
    const [fileData, setFileData] = useState<QueryProps>(queryPropInit);

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
                    setInvalidFormat(false);
                    setFileData(jsonData);
                } else {
                    alert("The JSON file did not match our format!")
                }
            } else if (fileType.includes('csv')) {
                const csvData = parseCSV(contents);
                setFileData(csvData);
            }
        };

        reader.onerror = (error) => {
            console.error('File reading error:', error);
        };
        reader.readAsText(file);
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

        // Reset the file input element
        if (fileInputRef.current) {
            fileInputRef.current.value = ''; // Clear the file input
        }
    };

    return (
        <div className="flex flex-1 pr-10">
            <div className="flex flex-col justify-center w-full bg-pacific-light-gray border rounded-lg flex flex-col items-center">
                <FiUpload className="text-4xl mb-2 hover:cursor-pointer" onClick={openFileBrowser} />
                <button className="text-lg">Click on the icon to upload a file</button>
                <input
                    ref={fileInputRef}
                    id="fileInput"
                    type="file"
                    style={{ display: 'none' }}
                    onChange={handleFileSelect}
                />
                {csvFileName && (
                    <>
                        <p>
                            File uploaded: {csvFileName} (Size: {fileSize} bytes)
                        </p>
                        <Button color="primary" onClick={removeFile} className="bg-red-400 text-black">
                            Remove File
                        </Button>
                    </>
                )}
                {invalidFormat && <p className="text-red-500">Invalid file format</p>}
                {invalidFile && (
                    <p className="text-red-500">Invalid file type. Please upload CSV or JSON files only.</p>
                )}
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
                    <Button
                        onClick={handleSubmit}
                        color="primary"
                        variant="shadow"
                        isLoading={isLoading}
                        className="bg-blue-500 text-white px-4 py-2 rounded mt-2">
                        Submit
                    </Button>
                )}
            </div>
        </div>
    );
};

export default FileForm;

const parseCSV = (csvText: string) => {
    const lines = csvText.split(/\r?\n/).filter((line) => line); // split and filter out empty lines
    lines[0].split(',').map((header) => header.trim()); // remove headers

    const practitioners = lines.slice(1).map((line) => {
        const data = line.split(',');
        return {
            first_name: data[0].trim(),
            last_name: data[1].trim(),
            npi: data[2].trim(),
        };
    });

    return { practitioners };
};
