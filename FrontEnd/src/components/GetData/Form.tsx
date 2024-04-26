import { Input, Button } from "@nextui-org/react";
import { FaRegSquarePlus } from "react-icons/fa6";


export default function GetDataForm ( { data, setData, handleSubmit, handleClear, isLoading } ) {
    const endpoints: string[] = ["Humana", "Kaiser", "Centene", "Cigna", "PacificSource"]
    const options: string[] = ["JSON", "File", "Page"]
    const handleChange = (value: string, field: keyof typeof data) => {
        setData({
            ...data,
            [field]: value
        });
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white border-1 border-pacific-gray flex flex-col p-10 rounded-lg gap-2 w-[80vw]"
        >
            <div className="flex flex-col md:flex-row gap-6">
                <div className="flex flex-col flex-1">
                    <Input type="text" variant={"underlined"} label="First Name" placeholder="John" isRequired
                           value={data.firstName}
                           onChange={(e) => handleChange(e.target.value, 'firstName')}
                    />
                    <Input
                        type={"text"} variant={"underlined"} label={"Last name"} placeholder={"Doe"} isRequired
                        value={data.lastName}
                        onChange={(e) => handleChange(e.target.value, 'lastName')}
                    />
                    <Input
                        type={"text"} variant={"underlined"} label={"NPI"} placeholder={"1234567890"} isRequired
                        value={data.npi}
                        onChange={(e) => handleChange(e.target.value, 'npi')}
                    />
                </div>
                <div className="flex flex-col flex-1 h-full self-center justify-center items-center">
                    <button className="text-[calc(2vw+5em)] text-pacific-blue hover:scale-105 transition ease-in-out">
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