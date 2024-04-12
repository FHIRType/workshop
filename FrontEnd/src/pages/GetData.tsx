import React from "react";
import {FormEvent, useState} from "react";
import {useQuery} from "@tanstack/react-query";
import DataTable from "react-data-table-component";
import LoadingIndicator from "../components/LoadingIndicator.tsx";
import {columns} from "../static/column.ts";
import {SelectionType, GetDataFormProps} from "../static/types.ts";
import {menus} from "../static/menus"
import GetDataForm from "../components/GetData/Form";

export default function GetData() {

    const [formData, setFormData] = useState<GetDataFormProps['data']>({
        firstName: "",
        lastName: "",
        npi: ""
    })

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

    return (
        <div className="h-full w-full bg-[#f7f9fc] flex flex-col justify-center items-center font-roboto p-16">
            <React.Fragment>
                <h2 className="select-none font-bold text-2xl pt-5 pb-2 text-[#21253b]">
                    {selection.name}
                </h2>
                <div className="pb-4">
                    {selection.description.map((desc, index) => {
                        return (
                            <div key={index + desc} className="select-none text-sm text-[#4a4b4f] text-center">
                                {desc}
                            </div>
                        );
                    })}
                </div>

                <GetDataForm
                    data={formData}
                    setData={setFormData}
                    handleSubmit={handleSubmit}
                    handleClear={handleClear}
                />

                <div className="search-results" style={{overflowX: "auto", width: "100%"}}>
                    {isLoading ? (
                        <LoadingIndicator/>
                    ) : error ? (
                        <div className="error">Error: {error.message}</div>
                    ) : data ? (
                        <div className="pract overflow-x-auto">
                            <h1>Search Results:</h1>
                            {(selection.name === "GET/ getdata" ||
                                selection.name === "POST/ getdata" ||
                                selection.name === "GET/ getconsensus" ||
                                selection.name === "POST/ matchdata") && (
                                <DataTable columns={columns} data={data} pagination
                                           conditionalRowStyles={conditionalRowStyles}
                                />
                            )}

                        </div>
                    ) : null}
                </div>
            </React.Fragment>
        </div>
    )
}