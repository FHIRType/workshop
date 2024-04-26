import {FormEvent, useState} from "react";
import {useQuery} from "@tanstack/react-query";
import DataTable from "react-data-table-component";
import {columns} from "../static/column.ts";
import {GetDataFormProps, QueryProp, formPropInit, queryPropInit} from "../static/types.ts";
import GetDataForm from "../components/GetData/Form";
import {cn} from "../utils/tailwind-utils.ts";
import CSVForm from "../components/CSVForm.tsx";


export default function Home() {

    const [formData, setFormData] = useState<GetDataFormProps['data']>(formPropInit)
    const [queryBody, setQueryBody] = useState<QueryProp>(queryPropInit)
    const [formVisible, setFormVisible] = useState<boolean>(true)
    const [jsonVisible, setJsonVisible] = useState<boolean>(false)

    const baseUrl = "http://127.0.0.1:5000/api/getdata"

    const {isLoading, error, data, refetch} = useQuery({
        queryKey: ["searchPractitioner", queryBody, formData.endpoint],
        queryFn: async () => {
            console.log("formData: ", formData)
            console.log("queryBody: ", queryBody)
            console.log("endpoint: ", formData.endpoint)
            const response = await fetch(
                `${baseUrl}?endpoint=${formData.endpoint}&format=JSON`, {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(queryBody)
                }
            );

            if (!response.ok) {
                throw new Error("Failed to fetch data");
            }
            const returned = await response.json()
            console.log("data: ", returned)
            return returned;
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
        const updatedPractitioners = formData.practitioners.map(prac => ({
            npi: prac.npi,
            first_name: prac.firstName,
            last_name: prac.lastName
        }));

        // Update the queryBody state
        setQueryBody({ practitioners: updatedPractitioners });

        refetch().catch(err => console.error("Error fetching data: ", err)); // Fetch data when search button is clicked
    };

    const handleClear = () => setFormData(formPropInit)

    const handleToggle = () => {
        setFormVisible(prev => !prev)
        setJsonVisible(prev => !prev)
    }

    return (
        <div className="p-10">
            <div className="flex flex-col">
                <h1 className={"text-[calc(1.5vw+2em)] text-center select-none text-pacific-blue font-semibold"}>Find your
                    doctors!</h1>
                <div className={"text-[calc(1.3vw+0.5em)] text-center mb-6 select-none text-pacific-blue opacity-80"}>Search. Find. Connect. Simplifying your path to healthcare.</div>
                <div className="self-center">
                    <div className={"flex gap-3"}>
                    <button className={cn(`ml-2 w-[calc(5vw+2em)] min-w-[80px] bg-pacific-light-blue text-white transition ease-in-out`, {
                        'bg-pacific-blue': formVisible
                    })} onClick={handleToggle}>Form
                    </button>
                    <button className={cn(`px-4 py-2 w-[calc(5vw+2em)] bg-pacific-light-blue text-white min-w-[80px] transition ease-in-out`, {
                        'bg-pacific-blue': jsonVisible,
                    })} onClick={handleToggle}>JSON
                    </button>
                </div>

                    {
                        formVisible &&
                        <GetDataForm
                            data={formData}
                            setFormData={setFormData}
                            handleSubmit={handleSubmit}
                            handleClear={handleClear}
                            isLoading={isLoading}
                        />
                    }
                    {
                        formVisible &&
                        <CSVForm/>
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
                        Object.keys(data).map((key, index) => {
                            return (
                                    <DataTable columns={columns} data={data[key]} pagination
                                               conditionalRowStyles={conditionalRowStyles} key={index+key}/>
                                )
                        })
                    )}
                </div>
            </div>
        </div>
    )
}