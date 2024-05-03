import { Input, Button } from '@nextui-org/react';
import { FaRegSquarePlus } from 'react-icons/fa6';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { fadeInAnimationVariants } from '../../static/variants';

export default function GetDataForm({ data, setFormData, handleSubmit, handleClear, isLoading }) {
    const endpoints: string[] = ['All', 'Humana', 'Kaiser', 'Centene', 'Cigna', 'PacificSource'];
    const options: string[] = ['JSON', 'File', 'Page'];

    const [selectedEndpoint, setSelectedEndpoint] = useState<string>('All');

    const handleChange = (value: string, idx: number, field: keyof typeof data) => {
        const newData = {
            ...data,
            practitioners: data.practitioners.map((item, index) => {
                if (idx !== index) return item;
                return { ...item, [field]: value }; // Update the specific item
            }),
        };
        setFormData(newData);
    };

    const handleEndpointChange = (e) => {
        setSelectedEndpoint(e.target.value);
        const newFormData = { ...data, endpoint: e.target.value };
        setFormData(newFormData);
    };

    // Add a new practitioner to the form data
    const addPractitioner = () => {
        const newPractitioners = [...data.practitioners, { firstName: '', lastName: '', npi: '' }];
        setFormData({ ...data, practitioners: newPractitioners });
    };

    // remove a practitioner from the formData
    const handleRemove = (e, index) => {
        e.preventDefault();
        setFormData((prevFormData) => ({
            ...prevFormData,
            practitioners: prevFormData.practitioners.filter((_, idx) => idx !== index),
        }));
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]">
            <div className="flex flex-col md:flex-row">
                <div className="flex flex-col md:flex-row flex-1 pr-9 pb-5">
                    <div className="flex flex-row flex-wrap gap-10 justify-center md:justify-normal">
                        {data.practitioners.map((prac, idx) => (
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
                                    placeholder="Ex. John"
                                    isRequired
                                    value={prac.firstName}
                                    onChange={(e) => handleChange(e.target.value, idx, 'firstName')}
                                    className={'form-inputs'}
                                />
                                <Input
                                    type="text"
                                    variant="underlined"
                                    label="Last Name"
                                    placeholder="Ex. Doe"
                                    isRequired
                                    value={prac.lastName}
                                    onChange={(e) => handleChange(e.target.value, idx, 'lastName')}
                                    className={'form-inputs'}
                                />
                                <Input
                                    type="text"
                                    variant="underlined"
                                    label="NPI"
                                    placeholder="Ex. 1234567890"
                                    isRequired
                                    value={prac.npi}
                                    onChange={(e) => handleChange(e.target.value, idx, 'npi')}
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
                        <div className="flex flex-col self-center justify-center items-center">
                            <button
                                type={'button'}
                                onClick={addPractitioner}
                                className="text-[calc(1vw+2em)] text-pacific-blue hover:scale-105 transition ease-in-out">
                                <FaRegSquarePlus />
                            </button>
                            <div className="max-w-[100px] mt-2 mb-4 leading-4 text-pacific-light-blue opacity-50 select-none text-center text-sm">
                                Add Practitioner
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex flex-col md:flex-row gap-8 justify-end">
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
                        <div className="bg-pacific-blue text-white pl-4 w-[150px] py-2 select-none">Settings</div>
                        <div className="select-none text-sm">Returned Data Type</div>
                        <select className="border-2 rounded-sm w-[150px]">
                            {options.map((option, idx) => {
                                return (
                                    <option key={idx} value={option}>
                                        {option}
                                    </option>
                                );
                            })}
                        </select>
                        <div className="mt-3">
                            <input type="checkbox" id="scales" name="isAccuracy" value="isAccuracy" />
                            <label htmlFor="endpoint" className="pl-3">
                                Get accuracy
                            </label>
                        </div>
                    </div>
                </div>
            </div>

            <div className="flex flex-row justify-center gap-2 mt-4">
                <Button color="primary" variant="shadow" type={'submit'} isLoading={isLoading}>
                    Submit
                </Button>
                <Button color="primary" variant="ghost" onClick={handleClear}>
                    Clear
                </Button>
            </div>
        </form>
    );
}
