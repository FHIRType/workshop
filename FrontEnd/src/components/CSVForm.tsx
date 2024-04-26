import React, { useState } from "react";
import Papa from "papaparse";

// Modal component
const Modal = ({ isOpen, onClose, csvFileName, setCsvFileName, handleDrop, value }) => {
    // State to store the content of the dropped CSV file
    const [fileContent, setFileContent] = useState("");

    // Function to handle file drop
    const handleFileDrop = (e) => {
        e.preventDefault();
        const droppedFile = e.dataTransfer.files[0];
        console.log("Dropped file:", droppedFile);

        const reader = new FileReader();
        reader.onload = (event) => {
            const contents = event.target.result;
            console.log("File contents:", contents);
            setFileContent(contents);
            handleDrop(droppedFile);
        };
        reader.onerror = (error) => {
            console.error("File reading error:", error);
        };
        reader.readAsText(droppedFile);
    };

    // Function to prevent default behavior
    const handleDragOver = (e) => {
        e.preventDefault();
    };

    // Function to handle file selection from the file input
    const handleFileSelect = (e) => {
        const selectedFile = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (event) => {
            const contents = event.target.result;
            console.log("File contents:", contents);
            setFileContent(contents);
            handleDrop(selectedFile);
        };
        reader.onerror = (error) => {
            console.error("File reading error:", error);
        };
        reader.readAsText(selectedFile);
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
        setFileContent(""); // Clear the file content
        setCsvFileName(null); // Clear the file name
        handleDrop(null); // Pass null to indicate removal of file

        // Reset the file input element
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.value = ''; // Reset the value of the file input
        }
    };

    // Function to handle form submission
    const handleSubmit = () => {
        // Add your logic to handle file submission here
    };

    const openDataFormatModal = () => {

    };

    return (
        <div className={`fixed top-0 left-0 w-full h-full flex items-center justify-center z-50 ${isOpen ? 'block' : 'hidden'}`}>
            <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-50"></div>
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-8 w-[80%] h-[80%]" onDrop={handleFileDrop} onDragOver={handleDragOver}>
                <div className="flex justify-end">
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <div className="mt-4 flex flex-col items-center">
                    {csvFileName ? (
                        <>
                            <p>File uploaded: {csvFileName}</p>
                            <button onClick={onClose} className="bg-blue-500 text-white px-4 py-2 rounded mt-4">Close</button>

                        </>
                    ) : (
                        <div className="flex">
                             <input id="fileInput" type="file" style={{ display: 'none' }} onChange={handleFileSelect} />
                            {/*<button onClick={openDataFormatModal} className="bg-blue-500 text-white px-4 py-2 rounded mt-4 mr-2 hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-400 focus:ring-opacity-50">Data Format</button>*/}
                            <button className="px-1 py-1 mr-5 w-[calc(5vw+2em)] bg-pacific-blue text-white min-w-[50px] transition ease-in-out">Data Format</button>
                            <button className="px-1 py-1 w-[calc(5vw+2em)] bg-pacific-blue text-white min-w-[50px] transition ease-in-out">CSV</button>


                        </div>
                    )}
                    <button onClick={openFileBrowser} className="bg-blue-500 text-white px-4 py-2 rounded mt-4 mr-2">Upload File</button>
                    <p>Drag a file below to upload</p>

                    {fileContent && (
                        <>
                            <p>File Contents:</p>
                            <textarea value={fileContent} readOnly className="w-full h-32 mt-2 px-4 py-2 border border-gray-300 rounded resize-none" />
                            <button onClick={removeFile} className="bg-red-500 text-white px-4 py-2 rounded mt-2">Remove File</button>
                            {/*<button onClick={handleSubmit} className="bg-green-500 text-white px-4 py-2 rounded mt-2">Submit</button>*/}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

const GetDataContainer: React.FC = () => {
    const [csvFileName, setCsvFileName] = React.useState<string | null>(null);
    const [csvData, setCsvData] = React.useState<any[]>([]);
    const [isModalOpen, setIsModalOpen] = useState(false); // State to manage modal visibility

    // Function to handle file drop
    const handleDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        setCsvFileName(file.name);

        const reader = new FileReader();
        reader.onload = () => {
            const csvText = reader.result as string;
            const parsedData = Papa.parse(csvText, { header: true });
            if (parsedData.errors.length === 0) {
                setCsvData(parsedData.data);
            } else {
                console.error('Error parsing CSV file:', parsedData.errors);
            }
        };
        reader.readAsText(file);
    }
};

    return (
        <div className="w-full h-full flex items-center justify-center">
            <div className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]">
                <div onClick={() => setIsModalOpen(true)}>
                    <p>Click here to upload a file</p>
                </div>
                {/* Modal */}
                <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} csvFileName={csvFileName} setCsvFileName={setCsvFileName} handleDrop={handleDrop}>
                    {/* Content of your modal */}
                    <p>Drag and drop a CSV file here</p>
                </Modal>
            </div>
        </div>
    );
};

export default GetDataContainer;
