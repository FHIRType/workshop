import React, { FormEvent, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import DataTable from "react-data-table-component";
import LoadingIndicator from "./components/LoadingIndicator.tsx";
import { columns } from "./static/column.ts";
import { menus } from "./static/menus.ts";
import { Selection } from "./static/types.ts";
import Button from "./components/Button.tsx";

export default function App() {
   const [firstName, setFirstName] = useState("");
   const [lastName, setLastName] = useState("");
   const [npi, setNPI] = useState("");
   const [selection, setSelection] = useState<Selection>({
      name: "",
      type: "",
      baseURL: "",
      description: [],
   });

   const { isLoading, error, data, refetch } = useQuery({
      queryKey: ["searchPractitioner", firstName, lastName, npi], // Include search parameters in queryKey
      queryFn: async () => {
         const response = await fetch(
            `${selection.baseURL}?first_name=${encodeURIComponent(
               firstName
            )}&last_name=${encodeURIComponent(
               lastName
            )}&npi=${encodeURIComponent(npi)}`
         );
         if (!response.ok) {
            throw new Error("Failed to fetch data");
         }
         return response.json();
      },
      enabled: false, // Disable automatic fetching
   });

   const renderContent = () => {
      return (
         <React.Fragment>
            <h2 className="select-none font-bold text-2xl pt-5 pb-2 text-[#21253b]">
               {selection.name}
            </h2>
            <div className="pb-4">
               {selection.description.map((desc, index) => {
                  return (
                     <div key={index} className="select-none text-sm text-[#4a4b4f]">
                        {desc}
                     </div>
                  );
               })}
            </div>
            <form
               onSubmit={handleSubmit}
               className="bg-white flex flex-col my-3 p-8 shadow-lg rounded-xl gap-2"
            >
               <input
                  className="input"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  placeholder="Enter First Name"
               />
               <input
                  className="input"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  placeholder="Enter Last Name"
               />
               <input
                  className="input"
                  value={npi}
                  onChange={(e) => setNPI(e.target.value)}
                  placeholder="Enter NPI"
               />
               <div className="flex flex-row justify-center gap-2">
                  <button className="button" type="submit">
                     Search
                  </button>
                  <button
                     className="button"
                     type="button"
                     onClick={handleClear}
                  >
                     Clear
                  </button>
               </div>
            </form>

            <div className="search-results">
               {isLoading ? (
                  <LoadingIndicator />
               ) : error ? (
                  <div className="error">Error: {error.message}</div>
               ) : data ? (
                  <div className="pract">
                     <h1>Search Results:</h1>
                     {selection.name === "GET/ getdata" && (
                         <DataTable columns={columns} data={data} pagination/>
                     )}
                     {selection.name === "POST/ getdata" && (
                         <DataTable columns={columns} data={data} pagination/>
                     )}
                     {selection.name === "GET/ getconsensus" && (
                         <DataTable columns={columns} data={data} pagination/>
                     )}
                     {selection.name === "POST/ matchdata" && (
                         <DataTable columns={columns} data={data} pagination/>
                     )}

                  </div>
               ) : null}
            </div>
         </React.Fragment>
      );
   };

   const handleSubmit = (e: FormEvent) => {
      e.preventDefault();
      refetch(); // Fetch data when search button is clicked
   };

   const handleClear = () => {
      // Clear search fields and search parameters
      setFirstName("");
      setLastName("");
      setNPI("");
   };

   return (
      <div className="h-full w-full bg-[#f7f9fc] flex flex-col justify-center items-center font-roboto p-16">
         <h1 className="select-none cursor-default text-[#1b2330] py-3 text-5xl font-bold">
            FHIR API
         </h1>
         <div className="flex flex-row gap-2 py-4">
            {menus.map((menu, index) => {
               return (
                  <Button key={index} onClick={() => setSelection(menu)}>
                     {menu.name}
                  </Button>
               );
            })}
         </div>
         {selection.name.length != 0 && renderContent()}
      </div>
   );
}
