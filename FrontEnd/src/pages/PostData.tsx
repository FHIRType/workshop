import React, { useState } from 'react';
import { GetDataFormProps, SelectionType } from '../static/types';
import { menus } from '../static/menus';
import {useQuery} from "@tanstack/react-query";
import LoadingIndicator from "../components/LoadingIndicator";
import {columns} from "../static/column";
import {conditionalRowStyles} from "../static/endpointColors";
import DataTable from "react-data-table-component";

export default function GetBulkData() {
    const [formData, setFormData] = useState<GetDataFormProps['data'][]>([{
        firstName: '',
        lastName: '',
        npi: ''
    }]);

    const [selection, setSelection] = useState<SelectionType>(menus[1]);

    const [fetchBody, setFetchBody] = useState({})

    const handleChange = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        const updatedFormDatas = [...formData];
        updatedFormDatas[index] = {
            ...updatedFormDatas[index],
            [name]: value
        };
        setFormData(updatedFormDatas);
    };

    const {isLoading, error, data, refetch: refetchBulk} = useQuery({
        queryKey: ["searchBulkPractitioner", fetchBody],
        queryFn: async () => {
            console.log("IN HERE: ")
            const response = await fetch(
                `${selection.baseURL}`, {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(fetchBody)
                }
            );
            if (!response.ok) {
                throw new Error("Failed to fetch data");
            }
            // console.log("fetched!: ", await response.json())
            return response.json();
        },
        enabled: false, // Disable automatic fetching
    });

    const handleAddFields = () => {
        setFormData([...formData, { firstName: '', lastName: '', npi: '' }]);
    };

    const handleRemoveFields = (index: number) => {
        const updatedFormDatas = formData.filter((_, i) => i !== index);
        setFormData(updatedFormDatas);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log('Submitting', formData);
        // Add logic to submit data
        setFetchBody(() => {
            return {
                data: formData.map(item => ({
                    [item.npi]: {
                        first_name: item.firstName,
                        last_name: item.lastName
                    }
                })),
                format: "string"
            }
        })
    };

    return (
        <div className="h-full w-full bg-[#f7f9fc] flex flex-col justify-center items-center font-roboto p-16">
            <h2 className="select-none font-bold text-2xl pt-5 pb-2 text-[#21253b]">{selection.name}</h2>
            <form
                onSubmit={handleSubmit}
                className={"bg-white flex flex-col my-3 p-8 shadow-lg rounded-xl gap-2 w-[60vw] " +
                    "justify-center items-center"}
            >
                {formData.map((data, index) => (
                    <div key={index}
                         className="flex flex-col gap-2 justify-center items-center border-2 w-[40%] rounded py-5">
                        <input
                            name="firstName"
                            className="input"
                            value={data.firstName}
                            onChange={e => handleChange(index, e)}
                            placeholder="Enter First Name"
                        />
                        <input
                            name="lastName"
                            className="input"
                            value={data.lastName}
                            onChange={e => handleChange(index, e)}
                            placeholder="Enter Last Name"
                        />
                        <input
                            name="npi"
                            className="input"
                            value={data.npi}
                            onChange={e => handleChange(index, e)}
                            placeholder="Enter NPI"
                        />
                        {formData.length > 1 && (
                            <button type="button" onClick={() => handleRemoveFields(index)}
                                    className="text-[0.9rem] border-2 px-3 rounded">
                                Remove
                            </button>
                        )}
                    </div>
                ))}
                <div className="flex flex-row justify-center gap-6">
                    <button type="button" onClick={handleAddFields} className="button border-2 px-5 rounded">
                        +
                    </button>
                    <button className="button" type="submit">
                        Submit All
                    </button>
                </div>
            </form>

            <div className="search-results" style={{overflowX: "auto", width: "100%"}}>
                {isLoading ? (
                    <LoadingIndicator/>
                ) : error ? (
                    <div className="error">Error: {error.message}</div>
                ) : data ? (
                    <div className="pract overflow-x-auto">
                        <h1>Search Results:</h1>
                        {
                            Object.keys(data).map( (key, index) =>
                                <DataTable columns={columns} data={data[key]} pagination
                                           conditionalRowStyles={conditionalRowStyles}
                                           key={index+key}
                                />
                            )

                        }

                    </div>
                ) : null}
            </div>
        </div>
    );
}
