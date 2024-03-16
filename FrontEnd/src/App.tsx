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
   });

   const { isLoading, error, data, refetch } = useQuery({
      queryKey: ["searchPractitioner", firstName, lastName, npi], // Include search parameters in queryKey
      queryFn: async () => {
         const response = await fetch(
            `http://127.0.0.1:5000/api/getdata?first_name=${encodeURIComponent(
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
            <h2 className="text-green-900 bg-blue-950 ">Search Practitioner</h2>
            <div className="search-form">
               <form onSubmit={handleSubmit} className="form">
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
               </form>
            </div>

            <div className="search-results">
               {isLoading ? (
                  <LoadingIndicator />
               ) : error ? (
                  <div className="error">Error: {error.message}</div>
               ) : data ? (
                  <div className="pract">
                     <h1>Search Results:</h1>
                     <DataTable columns={columns} data={data} pagination />
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
      <div className="h-full w-full bg-[#f7f9fc] flex flex-col justify-center items-center font-roboto">
         <h1 className="select-none cursor-default text-[#1b2330] py-3 text-5xl font-bold">
            FHIR API
         </h1>
         <div className="flex flex-row gap-2">
            {menus.map((menu) => {
               return (
                  <Button onClick={() => setSelection(menu)}>
                     {menu.name}
                  </Button>
               );
            })}
         </div>
         {selection.name.length != 0 && renderContent()}
      </div>
   );
}
