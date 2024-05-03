import React, { useRef, useState } from "react";
import { FiUpload } from 'react-icons/fi';

import { QueryProps } from "../static/types";

type _QueryProps = {
    setQueryBody: (data: QueryProps) => void;
 };

const CSVForm = ({ setQueryBody }: _QueryProps) => {
    const [csvFileName, setCsvFileName] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null)

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files ? e.target.files[0] : null;
        if (!selectedFile) return;

        const fileType = selectedFile.type;
        const allowedTypes = ["text/csv", "application/vnd.ms-excel", "application/json"];

        if (!allowedTypes.includes(fileType)) {
            alert("Can only upload CSV or JSON files");
            return;
        }

        setCsvFileName(selectedFile.name);
        parseFile(selectedFile, fileType);
    };

    const parseFile = (file: File, fileType: string) => {
        const reader = new FileReader();

        reader.onload = (event: ProgressEvent<FileReader>) => {
            const contents = event.target?.result as string;

            if (fileType.includes("json")) {
                const jsonData = JSON.parse(contents)
                console.log("json parsed: ", jsonData)
                setQueryBody(jsonData)
            }
        };
        reader.onerror = (error) => {
            console.error("File reading error:", error);
        };
        reader.readAsText(file);
    };

    const handleSubmit = () => {
        // Trigger the submission of parsed practitioners' data
        // This can be handled by the parent component (Home.tsx)
    };

    // Function to open file browser when "Upload File" button is clicked
    const openFileBrowser = () => {
        fileInputRef.current?.click()
    };

    // Function to remove uploaded file
    const removeFile = () => {
        setCsvFileName(null); // Clear the file name

        // Reset the file input element
        if (fileInputRef.current) {
            fileInputRef.current.value = '';  // Clear the file input
        }
    };

    return (
        <div className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]">
            <div className="bg-gray-200 border border-gray-400 p-6 rounded-lg flex flex-col items-center">
                <FiUpload className="text-4xl mb-2" onClick={openFileBrowser} />
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
                        <p>File uploaded: {csvFileName}</p>
                        <button onClick={removeFile} className="bg-red-500 text-white px-4 py-2 rounded mt-2">Remove File</button>
                    </>
                )}
                <button onClick={handleSubmit} className="bg-blue-500 text-white px-4 py-2 rounded mt-2">Submit</button>
            </div>
        </div>
    );
};

export default CSVForm;
