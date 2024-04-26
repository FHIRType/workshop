import { Input, Button } from "@nextui-org/react";
import { FaRegSquarePlus } from "react-icons/fa6";


export default function GetDataForm ( { data, setFormData, handleSubmit, handleClear, isLoading } ) {
    const endpoints: string[] = ["Humana", "Kaiser", "Centene", "Cigna", "PacificSource"]
    const options: string[] = ["JSON", "File", "Page"]

    const handleChange = (value: string, idx: number, field: keyof typeof data) => {
        // setFormData(prevFormData => ({
        //     ...prevFormData,
        //     [field]: value
        // }));
        const newData = data.map((item, index) => {
            if (idx !== index) return item;
            return { ...item, [field]: value };
        });
        setFormData(newData);
    };

    // Add a new practitioner to the form data
    const addPractitioner = () => {
        setFormData(data.concat([{ firstName: "", lastName: "", npi: "" }]));
    };

    // Function to remove a practitioner from the formData
    const handleRemove = (index) => {
        setFormData(prevFormData => prevFormData.filter((_, idx) => idx !== index));
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]"
        >
            <div className="flex flex-col md:flex-row gap-6">
                <div className={"flex flex-row flex-wrap gap-10"}>
                    {data.map((prac, idx) => (
                        <div key={idx} className="flex flex-col flex-1">
                            <Input type="text" variant="underlined" label="First Name" placeholder="John" isRequired
                                   value={prac.firstName} onChange={(e) => handleChange(e.target.value, idx, 'firstName')}
                                   className={"form-inputs"}
                            />
                            <Input type="text" variant="underlined" label="Last Name" placeholder="Doe" isRequired
                                   value={prac.lastName} onChange={(e) => handleChange(e.target.value, idx, 'lastName')}
                                   className={"form-inputs"}
                            />
                            <Input type="text" variant="underlined" label="NPI" placeholder="1234567890" isRequired
                                   value={prac.npi} onChange={(e) => handleChange(e.target.value, idx, 'npi')}
                                   className={"form-inputs"}
                            />
                            {idx !== 0 && (
                                <Button color="error" onClick={() => handleRemove(idx)}>Remove</Button>
                            )}
                        </div>
                    ))}
                </div>
                {/*<div className="flex flex-col flex-1">*/}
                {/*    <Input type="text" variant={"underlined"} label="First Name" placeholder="John" isRequired*/}
                {/*           value={data.firstName}*/}
                {/*           onChange={(e) => handleChange(e.target.value, 'firstName')}*/}
                {/*    />*/}
                {/*    <Input*/}
                {/*        type={"text"} variant={"underlined"} label={"Last name"} placeholder={"Doe"} isRequired*/}
                {/*        value={data.lastName}*/}
                {/*        onChange={(e) => handleChange(e.target.value, 'lastName')}*/}
                {/*    />*/}
                {/*    <Input*/}
                {/*        type={"text"} variant={"underlined"} label={"NPI"} placeholder={"1234567890"} isRequired*/}
                {/*        value={data.npi}*/}
                {/*        onChange={(e) => handleChange(e.target.value, 'npi')}*/}
                {/*    />*/}
                {/*</div>*/}
                <div className="flex flex-col flex-1 h-full self-center justify-center items-center">
                    <button
                        type={"button"}
                        onClick={addPractitioner}
                        className="text-[calc(1.5vw+3em)] text-pacific-blue hover:scale-105 transition ease-in-out">
                        <FaRegSquarePlus/>
                    </button>
                    <div className="mt-2 text-pacific-light-blue opacity-50 select-none">Search Multiple</div>
                    <div className="text-pacific-light-blue opacity-50 select-none">Pracitioners</div>
                </div>
                <div className="flex flex-col md:flex-row flex-1 gap-8">
                    <div className="flex flex-col h-full self-center items-start gap-2">
                        <div className="bg-pacific-blue text-white pl-4 w-[150px] py-2 select-none">Endpoints</div>
                        {endpoints.map((endpoint, idx) => {
                            return <div key={idx}>
                                <input type="checkbox" id="scales" name={endpoint} value={endpoint}/>
                                <label htmlFor="endpoint" className="pl-3">{endpoint}</label>
                            </div>
                        })}
                    </div>
                    <div className="flex flex-col h-full self-center items-start gap-2">
                        <div className="bg-pacific-blue text-white pl-4 w-[150px] py-2 select-none">Settings</div>
                        <div className="select-none text-sm">Returned Data Type</div>
                        <select className="border-2 rounded-sm w-[150px]">
                            {
                                options.map((option, idx) => {
                                    return (
                                        <option key={idx} value={option}>
                                            {option}
                                        </option>
                                    )
                                })
                            }
                        </select>
                        <div className="mt-3">
                            <input type="checkbox" id="scales" name="isAccuracy" value="isAccuracy"/>
                            <label htmlFor="endpoint" className="pl-3">Get accuracy</label>
                        </div>
                    </div>
                </div>


            </div>

            <div className="flex flex-row justify-center gap-2">
                <Button color="primary" variant="shadow" type={"submit"} isLoading={isLoading}>
                    Submit
                </Button>
                <Button color="primary" variant="ghost" onClick={handleClear}>
                    Clear
                </Button>
            </div>
        </form>
    );
}