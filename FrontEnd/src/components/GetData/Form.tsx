import { Input, Button } from '@nextui-org/react';
import { FaRegSquarePlus } from 'react-icons/fa6';
import { FaFileDownload } from 'react-icons/fa';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { fadeInAnimationVariants } from '../../static/variants';
import { GetDataFormProps, PractitionerType } from '../../static/types';
import JSONForm from "../JSONForm";
import FileForm from "../FileForm";

type _GetDataFormProps = {
    data: GetDataFormProps['data'];
    setFormData: (data: any) => void;
    handleSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
    handleClear: () => void;
    isLoading: boolean;
    handleDownload: () => void;
    JSONVisible: boolean;
    fileVisible: boolean;
    handleSubmitFile: (data: any) => void;
};

export default function GetDataForm({
    data,
    setFormData,
    handleSubmit,
    handleClear,
    isLoading,
    handleDownload,
    JSONVisible,
    fileVisible,
    handleSubmitFile,
}: _GetDataFormProps) {
    const endpoints: string[] = ['All', 'Humana', 'Kaiser', 'Centene', 'Cigna'];
    const [selectedEndpoint, setSelectedEndpoint] = useState<string>('All');
    const [consensus, setConsensus] = useState<boolean>(true);

    const handleChange = (value: string, idx: number, field: keyof PractitionerType) => {
        const newData = {
            ...data,
            practitioners: data.practitioners.map((item, index: number) => {
                if (idx !== index) return item;
                return { ...item, [field]: value }; // Update the specific item
            }),
        };
        setFormData(newData);
    };

    const handleEndpointChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedEndpoint(e.target.value);
        const newFormData = { ...data, endpoint: e.target.value };
        setFormData(newFormData);
    };

    const handleConsensusChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setConsensus(e.target.checked);
        const boolVal = e.target.checked ? 'True' : 'False';
        const newFormData = { ...data, consensus: boolVal };
        setFormData(newFormData);
    };

    // Add a new practitioner to the form data
    const addPractitioner = () => {
        const newPractitioners = [...data.practitioners, { firstName: '', lastName: '', npi: '' }];
        setFormData({ ...data, practitioners: newPractitioners });
    };

    // remove a practitioner from the formData
    const handleRemove = (e: React.MouseEvent<HTMLButtonElement>, index: number) => {
        e.preventDefault();
        setFormData((prevFormData: GetDataFormProps['data']) => ({
            ...prevFormData,
            practitioners: prevFormData.practitioners.filter((_: any, idx: number) => idx !== index),
        }));
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white border-1 border-pacific-gray flex flex-col pt-5 p-10 rounded-lg gap-2 w-[80vw]">
            <div className="flex flex-row justify-center items-center">
                {
                    (!JSONVisible && !fileVisible) &&
                    <button
                        type={'button'}
                        onClick={addPractitioner}
                        className="text-[calc(1vw+1em)] w-full text-pacific-blue hover:text-white border border-pacific-gray hover:bg-pacific-blue rounded-md px-3 py-2 transition ease-in-out flex flex-row items-center justify-center">
                        <FaRegSquarePlus />

                            <div className="pl-4 leading-4 select-none self-center text-base">Add Practitioner</div>
                    </button>
                }
            </div>
            <div className="flex flex-col md:flex-row">
                <div className="flex flex-col md:flex-row flex-1 pb-5 pr-2">
                    <div className="flex flex-row flex-wrap gap-10 justify-center md:justify-normal w-full">
                        {
                            !JSONVisible && !fileVisible &&
                            <>
                                {data.practitioners.map((prac: PractitionerType, idx: number) => (
                                    <motion.div
                                        key={idx}
                                        className="flex flex-col"
                                        initial="initial"
                                        animate="animate"
                                        exit="exit"
                                        viewport={{ once: true }}
                                        variants={fadeInAnimationVariants}>
                                        <Input
                                            type="text"
                                            variant="underlined"
                                            label="First Name"
                                            placeholder="John"
                                            isRequired
                                            value={prac.first_name}
                                            onChange={(e) => handleChange(e.target.value, idx, 'first_name')}
                                            className={'form-inputs'}
                                        />
                                        <Input
                                            type="text"
                                            variant="underlined"
                                            label="Last Name"
                                            placeholder="Doe"
                                            isRequired
                                            value={prac.last_name}
                                            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                                                handleChange(e.target.value, idx, 'last_name')
                                            }
                                            className={'form-inputs'}
                                        />
                                        <Input
                                            type="text"
                                            variant="underlined"
                                            label="NPI"
                                            placeholder="1234567890"
                                            isRequired
                                            value={prac.npi}
                                            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                                                handleChange(e.target.value, idx, 'npi')
                                            }
                                            className={'form-inputs'}
                                        />
                                        {idx !== 0 && (
                                            <button
                                                className={
                                                    'form-inputs mt-2 px-3 py-2 rounded-md text-sm transition ease-in-out bg-[#ded3d2] hover:bg-[#e67474] hover:text-white'
                                                }
                                                onClick={(e) => handleRemove(e, idx)}>
                                                Remove
                                            </button>
                                        )}
                                    </motion.div>
                                ))}
                            </>
                        }
                        {JSONVisible && <JSONForm setQueryBody={handleSubmitFile} isLoading={isLoading} />}
                        {fileVisible && <FileForm setQueryBody={handleSubmitFile} isLoading={isLoading} />}
                    </div>
                </div>

                <div className="flex flex-col md:flex-row gap-8 justify-end mt-2">
                    <div className="flex flex-col h-full self-center items-start gap-2">
                        <div className="bg-pacific-blue text-white pl-4 w-[150px] py-2 select-none">Endpoints</div>
                        {endpoints.map((endpoint, idx) => {
                            return (
                                <div key={idx} className="flex items-center">
                                    <input
                                        type="radio"
                                        id={endpoint}
                                        name="endpointSelection"
                                        value={endpoint}
                                        onChange={handleEndpointChange}
                                        checked={selectedEndpoint === endpoint}
                                        className="mr-2"
                                    />
                                    <label htmlFor={endpoint}>{endpoint}</label>
                                </div>
                            );
                        })}
                    </div>
                    <div className="flex flex-col h-full self-center items-start gap-2">
                        <div className="bg-pacific-blue text-white px-2 w-[150px] py-2 select-none">
                            Advanced Options
                        </div>

                        <div className="text-sm">
                            <input
                                type="checkbox"
                                id="consensusCheckbox"
                                checked={consensus}
                                onChange={handleConsensusChange}
                            />
                            <label htmlFor="consensusCheckbox" className="pl-3">
                                Enable Consensus
                            </label>
                        </div>
                        <div className="mt-3 mx-auto">
                            <Button
                                className={'bg-pacific-blue text-white text-md hover:bg-pacific-blue-9'}
                                onClick={handleDownload}
                                type={'button'}>
                                <FaFileDownload />
                                Download
                            </Button>
                        </div>
                    </div>
                </div>
            </div>

            {
                (!JSONVisible && !fileVisible) &&
                <div className="flex flex-row justify-center gap-2 mt-4">
                    <Button color="primary" variant="shadow" type={'submit'} isLoading={isLoading}>
                        Submit
                    </Button>
                    <Button color="primary" variant="ghost" onClick={handleClear}>
                        Clear
                    </Button>
                </div>
            }
        </form>
    );
}
