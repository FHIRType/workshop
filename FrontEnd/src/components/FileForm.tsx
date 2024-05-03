import React, { useState } from "react";
import { FiUpload } from 'react-icons/fi';

const FileForm = ({ setQueryBody }) => {
    const [csvFileName, setCsvFileName] = useState<string | null>(null);
    const [invalidFormat, setInvalidFormat] = useState<boolean>(false);
    const [invalidFile, setInvalidFile] = useState<boolean>(false);
    //const [processing, setProcessing] = useState<boolean>(false);
    const [fileSize, setFileSize] = useState<number>(0);

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files ? e.target.files[0] : null;
        if (!selectedFile) return;

        const fileType = selectedFile.type;
        const allowedTypes = ["text/csv", "application/vnd.ms-excel", "application/json"];

        if (!allowedTypes.includes(fileType)) {
            //alert("Can only upload CSV or JSON files");
            setInvalidFile(true)
            return;
        }
        setInvalidFile(false);
        setCsvFileName(selectedFile.name);
        setFileSize(selectedFile.size);
        //setProcessing(true);
        parseFile(selectedFile, fileType);
    };

    const parseFile = (file: File) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const contents = event.target.result as string;
            try {
                const jsonData = JSON.parse(contents);
                if (isValidJson(jsonData)) {
                    setQueryBody(jsonData);
                    console.log("Parsed JSON data:", jsonData);
                    setInvalidFormat(false);
                } else {
                    setInvalidFormat(true);
                    console.error("Invalid JSON format.");
                    console.log("Jsondata", jsonData)
                }
            } catch (error) {
                console.error("Error parsing JSON:", error);
            }
        };
        reader.onerror = (error) => {
            console.error("File reading error:", error);
        };
        reader.readAsText(file);
    };

    const isValidJson = (jsonData: any): boolean => {
        if (jsonData && jsonData.practitioners && Array.isArray(jsonData.practitioners)) {
            for (const practitioner of jsonData.practitioners) {
                if (
                    !practitioner ||
                    typeof practitioner.npi !== "string" ||
                    typeof practitioner.first_name !== "string" ||
                    typeof practitioner.last_name !== "string"
                ) {
                    return false;
                }
            }
            return true;
        }
        return false;
    };

    // Function to open file browser when "Upload File" button is clicked
    const openFileBrowser = () => {
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.click();
        }
    };

    // Function to remove uploaded file
    const removeFile = () => {
        setCsvFileName(null); // Clear the file name

        // Reset the file input element
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.value = ''; // Reset the value of the file input
        }
        setInvalidFormat(false);
        setInvalidFile(false);
        //setProcessing(false);
    };

    return (
        <div className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]">
            <div className="bg-gray-200 border border-gray-400 p-6 rounded-lg flex flex-col items-center">
                <FiUpload className="text-4xl mb-2" onClick={openFileBrowser} />
                <button className="text-lg">Click on the icon to upload a file</button>
                <input id="fileInput" type="file" style={{ display: 'none' }} onChange={handleFileSelect} />
                {csvFileName && (
                    <>
                        <p>File uploaded: {csvFileName} (Size: {fileSize} bytes)</p>
                        <button onClick={removeFile} className="bg-red-500 text-white px-4 py-2 rounded mt-2">Remove File</button>
                    </>
                )}
                {/*{processing && (*/}
                {/*    <>*/}
                {/*        <p>Processing...</p>*/}
                {/*        <div className="w-full h-4 bg-gray-300 rounded mt-2 relative">*/}
                {/*            <div className="h-full bg-blue-500 rounded absolute top-0 left-0" style={{ width: '50%' }}></div>*/}
                {/*        </div>*/}
                {/*    </>*/}
                {/*)}*/}
                {invalidFormat && (
                    <p className="text-red-500">Invalid file format</p>
                )}
                {invalidFile && (
                    <p className="text-red-500">Invalid file type. Please upload CSV or JSON files only.</p>
                )}
            </div>
        </div>
    );
};

export default FileForm;
