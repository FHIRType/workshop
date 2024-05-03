import React, { useState } from "react";
import Papa from "papaparse";
import { FiUpload } from 'react-icons/fi';

const CSVForm = ({ setQueryBody }) => {
    const [csvFileName, setCsvFileName] = useState<string | null>(null);

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files[0];
        const fileType = selectedFile.type;
        const allowedTypes = ["text/csv", "application/json"];

        if (!allowedTypes.includes(fileType)) {
            alert("Can only upload CSV or JSON files");
            return;
        }

        setCsvFileName(selectedFile.name);
        parseFile(selectedFile);
    };

    const parseFile = (file: File) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const contents = event.target.result as string;
            const parsedData = Papa.parse(contents, { header: true }).data;
            const practitioners = parsedData.map((row: any) => ({
                npi: row.npi,
                first_name: row.first_name,
                last_name: row.last_name
            }));
            const jsonData = { practitioners };
            console.log("Parsed JSON data:", jsonData);
            setQueryBody(jsonData); // Update queryBody state with parsed practitioners data
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
    };

    return (
        <div className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]">
            <div className="bg-gray-200 border border-gray-400 p-6 rounded-lg flex flex-col items-center">
                <FiUpload className="text-4xl mb-2" onClick={openFileBrowser} />
                <button className="text-lg">Click on the icon to upload a file</button>
                <input id="fileInput" type="file" style={{ display: 'none' }} onChange={handleFileSelect} />
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
