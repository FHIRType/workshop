import { Input, Button } from "@nextui-org/react";
import { FaRegSquarePlus } from "react-icons/fa6";
import {useState} from "react";


export default function GetDataForm ( { data, setFormData, handleSubmit, handleClear, isLoading } ) {
    const endpoints: string[] = ["All", "Humana", "Kaiser", "Centene", "Cigna", "PacificSource"]
    const options: string[] = ["JSON", "File"]

    const [selectedEndpoint, setSelectedEndpoint] = useState<string>('All')
    const [consensus, setConsensus] = useState<boolean>(false)

    const handleChange = (value: string, idx: number, field: keyof typeof data) => {
        const newData = {
            ...data,
            practitioners: data.practitioners.map((item, index) => {
                if (idx !== index) return item;
                return { ...item, [field]: value };  // Update the specific item
            })
        };
        setFormData(newData);
    };

    const handleEndpointChange = (e) => {
        setSelectedEndpoint(e.target.value)
        const newFormData = {...data, endpoint: e.target.value}
        setFormData(newFormData)
    }

    const handleConsensusChange = (e) => {
        setConsensus(e.target.checked)
        const boolVal = e.target.checked === true ? "True" : "False"
        const newFormData = {...data, consensus: boolVal}
        setFormData(newFormData)
    }
    // Add a new practitioner to the form data
    const addPractitioner = () => {
        const newPractitioners = [...data.practitioners, { firstName: "", lastName: "", npi: "" }];
        setFormData({...data, practitioners: newPractitioners});
    };

    // remove a practitioner from the formData
    const handleRemove = (index) => {
        setFormData(prevFormData => ({
            ...prevFormData,
            practitioners: prevFormData.practitioners.filter((_, idx) => idx !== index)
        }));
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]"
        >
            <div className="flex flex-col md:flex-row gap-6">
                <div className={"flex flex-row flex-wrap gap-10"} >
                    {data.practitioners.map((prac, idx) => (
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
                                <Button className={"form-inputs mt-1 bg-orange-200"} onClick={() => handleRemove(idx)}>Remove</Button>
                            )}
                        </div>
                    ))}
                </div>
                <div className="flex flex-col flex-1 h-full self-center justify-center items-center">
                    <button
                        type={"button"}
                        onClick={addPractitioner}
                        className="text-[calc(1vw+2em)] text-pacific-blue hover:scale-105 transition ease-in-out">
                        <FaRegSquarePlus/>
                    </button>
                    <div className="mt-2 max-w-[100px] text-pacific-light-blue opacity-50 select-none text-center">Search Multiple Practitioners</div>
                </div>
                <div className="flex flex-col md:flex-row flex-1 gap-8">
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
                            )
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
                            <input type="checkbox" id="scales" checked={consensus} onChange={handleConsensusChange}/>
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