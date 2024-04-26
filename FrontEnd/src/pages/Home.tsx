import {FormEvent, useState} from "react";
import {useQuery} from "@tanstack/react-query";
import DataTable from "react-data-table-component";
import {columns} from "../static/column.ts";
import {GetDataFormProps} from "../static/types.ts";
import GetDataForm from "../components/GetData/Form";
import {cn} from "../utils/tailwind-utils.ts";

export default function Home() {

    const [formData, setFormData] = useState<GetDataFormProps['data']>({
        firstName: "",
        lastName: "",
        npi: ""
    })

    const [formVisible, setFormVisible] = useState<boolean>(true)
    const [jsonVisible, setJsonVisible] = useState<boolean>(false)

    const baseUrl = "http://127.0.0.1:5000/api/getdata"

    const {isLoading, error, data, refetch} = useQuery({
        queryKey: ["searchPractitioner", formData.firstName, formData.lastName, formData.npi],
        queryFn: async () => {
            const response = await fetch(
                `${baseUrl}?first_name=${formData.firstName}&last_name=${formData.lastName}&npi=${formData.npi}`
            );
            if (!response.ok) {
                throw new Error("Failed to fetch data");
            }
            return response.json();
        },
        enabled: false, // Disable automatic fetching
    });

    // Define a mapping between endpoints and colors
    const endpointColors: Record<string, string> = {
        'Kaiser': '#ADD8E6', //LightBlue
        'Humana': '#E6E6FA', //Lavender
        'Cigna': '#FFE4E1', //MistyRose
        'PacificSource': '#8FBC8F', //DarkSeaGreen
        'Centene': '#D3D3D3' //DarkSlateBlue
        //other endpoints
    };

    // Define conditional row styles function using the endpointColors mapping
    const conditionalRowStyles = [
        {
            when: (row: { Endpoint: string }) => endpointColors.hasOwnProperty(row.Endpoint),
            style: (row: { Endpoint: string }) => ({
                backgroundColor: endpointColors[row.Endpoint],
            }),
        },
    ];

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        refetch().catch(err => console.error("Error fetching data: ", err)); // Fetch data when search button is clicked
    };

    const handleClear = () => setFormData({ firstName: "", lastName: "", npi: "" })

    const handleFormToggle = () => {
        if (!formVisible) {
            setFormVisible(true)
            setJsonVisible(false)
        }
    }

    const handleJsonToggle = () => {
        if (!jsonVisible) {
            setJsonVisible(true)
            setFormVisible(false)
        }
    }

    return (
        <div className="p-10">
            <div className="flex flex-col">
                <h1 className={"text-[calc(1.5vw+2em)] text-center select-none text-pacific-blue font-semibold"}>Find your
                    doctors!</h1>
                <div className={"text-[calc(1.3vw+0.5em)] text-center mb-6 select-none text-pacific-blue opacity-80"}>Put some sentences that sound intelligent</div>
                <div className="self-center">
                    <div className={"flex gap-3"}>
                    <button className={cn(`ml-2 w-[calc(5vw+2em)] min-w-[80px] bg-pacific-blue text-white transition ease-in-out`, {
                        'bg-pacific-light-blue': formVisible
                    })} onClick={handleFormToggle}>Form
                    </button>
                    <button className={cn(`px-4 py-2 w-[calc(5vw+2em)] bg-pacific-blue text-white min-w-[80px] transition ease-in-out`, {
                        'bg-pacific-light-blue': jsonVisible,
                    })} onClick={handleJsonToggle}>JSON
                    </button>
                </div>

                    {
                        formVisible &&
                        <GetDataForm
                            data={formData}
                            setData={setFormData}
                            handleSubmit={handleSubmit}
                            handleClear={handleClear}
                            isLoading={isLoading}
                        />
                    }
                    {
                        jsonVisible &&
                        <div>
                            JSON Field
                        </div>
                    }
                </div>


                <div className="search-results" style={{overflowX: "auto", width: "100%"}}>
                    {error && <div>Error: {error.message}</div>}
                    {data && (
                        <div className="overflow-x-auto">
                            <DataTable columns={columns} data={data} pagination
                                       conditionalRowStyles={conditionalRowStyles}/>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}