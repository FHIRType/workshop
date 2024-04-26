import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import Papa from "papaparse";

// Modal component
const Modal = ({ isOpen, onClose, children }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-8">
                <div className="flex justify-end">
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <div className="mt-4">{children}</div>
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
        if (acceptedFiles.length > 0) {
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

    const { getRootProps, getInputProps } = useDropzone({ onDrop: handleDrop });

    return (
        <div className="w-full h-full flex items-center justify-center">
            <div className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]">
                <div {...getRootProps()}>
                    <input {...getInputProps()} />
                    <p onClick={() => setIsModalOpen(true)}>Drag and drop a CSV file here, or click here to upload a file</p>
                    {csvFileName && <p>File: {csvFileName}</p>}
                </div>
                {/* Modal */}
                <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
                    {/* Content of your modal */}
                    <p>Modal Content</p>
                </Modal>
            </div>
        </div>
    );
};

export default GetDataContainer;
