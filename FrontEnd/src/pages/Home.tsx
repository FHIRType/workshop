import React from "react";
import {FormEvent, useState} from "react";
import {useQuery} from "@tanstack/react-query";
import DataTable from "react-data-table-component";
import LoadingIndicator from "../components/LoadingIndicator.tsx";
import {columns} from "../static/column.ts";
import {SelectionType, GetDataFormProps} from "../static/types.ts";
import {menus} from "../static/menus"
import GetDataForm from "../components/GetData/Form";

export default function Home() {

    const [formData, setFormData] = useState<GetDataFormProps['data']>({
        firstName: "",
        lastName: "",
        npi: ""
    })

    const [formVisible, setFormVisible] = useState<boolean>(true)
    const [jsonVisible, setJsonVisible] = useState<boolean>(false)


    const [selection, setSelection] = useState<SelectionType>(menus[0])

    const {isLoading, error, data, refetch} = useQuery({
        queryKey: ["searchPractitioner", formData.firstName, formData.lastName, formData.npi],
        queryFn: async () => {
            const response = await fetch(
                `${selection.baseURL}?first_name=${formData.firstName}&last_name=${formData.lastName}&npi=${formData.npi}`
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

    const handleToggle = () => {
        setFormVisible(prev => !prev)
        setJsonVisible(prev => !prev)
    }

    return (
        <div className="p-10">
            <div>
                <h1 className={"text-[4rem] text-center"}>Find your doctors!</h1>

                <div className={"flex gap-5"}>
                    <button className={`p-3 ${formVisible ? 'toggled' : 'notToggled'} rounded`} onClick={handleToggle}>Form</button>
                    <button className={`p-3 ${jsonVisible ? 'toggled' : 'notToggled'} rounded`} onClick={handleToggle}>JSON</button>
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

                <div className="search-results" style={{overflowX: "auto", width: "100%"}}>
                    {error && <div>Error: {error.message}</div>}
                    {data && (
                        <div className="overflow-x-auto">
                            <DataTable columns={columns} data={data} pagination conditionalRowStyles={conditionalRowStyles} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}