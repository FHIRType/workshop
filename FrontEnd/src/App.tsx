import { FormEvent, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import DataTable from "react-data-table-component";
import LoadingIndicator from "./components/LoadingIndicator.tsx";
import "tailwindcss/tailwind.css";
import { test_data } from "./static/types.ts";
import { DataColumn } from "react-data-table-component";

export default function App() {
   const [firstName, setFirstName] = useState("");
   const [lastName, setLastName] = useState("");
   const [npi, setNPI] = useState("");

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

   // Define columns for the data table
   const columns: DataColumn<test_data>[] = [
      {
         name: "Endpoint",
         selector: (row: { Endpoint: any }) => row.Endpoint,
         sortable: true,
      },
      {
         name: "Date Retrieved",
         selector: (row: { DateRetrieved: any }) => row.DateRetrieved,
         sortable: true,
      },
      {
         name: "Full Name",
         selector: (row: { FullName: any }) => row.FullName,
         sortable: true,
      },
      { name: "NPI", selector: (row: { NPI: any }) => row.NPI, sortable: true },
      {
         name: "First Name",
         selector: (row: { FirstName: any }) => row.FirstName,
         sortable: true,
      },
      {
         name: "Last Name",
         selector: (row: { LastName: any }) => row.LastName,
         sortable: true,
      },
      {
         name: "Gender",
         selector: (row: { Gender: any }) => row.Gender,
         sortable: true,
      },
      {
         name: "Taxonomy",
         selector: (row: { Taxonomy: any }) => row.Taxonomy,
         sortable: true,
      },
      {
         name: "Group Name",
         selector: (row: { GroupName: any }) => row.GroupName,
         sortable: true,
      },
      {
         name: "Address 1",
         selector: (row: { ADD1: any }) => row.ADD1,
         sortable: true,
      },
      {
         name: "Address 2",
         selector: (row: { ADD2: any }) => row.ADD2,
         sortable: true,
      },
      {
         name: "City",
         selector: (row: { City: any }) => row.City,
         sortable: true,
      },
      {
         name: "State",
         selector: (row: { State: any }) => row.State,
         sortable: true,
      },
      { name: "Zip", selector: (row: { Zip: any }) => row.Zip, sortable: true },
      {
         name: "Phone",
         selector: (row: { Phone: any }) => row.Phone,
         sortable: true,
      },
      { name: "Fax", selector: (row: { Fax: any }) => row.Fax, sortable: true },
      {
         name: "Email",
         selector: (row: { Email: any }) => row.Email,
         sortable: true,
      },
      {
         name: "Latitude",
         selector: (row: { lat: any }) => row.lat,
         sortable: true,
      },
      {
         name: "Longitude",
         selector: (row: { lng: any }) => row.lng,
         sortable: true,
      },
      {
         name: "Last Prac Update",
         selector: (row: { LastPracUpdate: any }) => row.LastPracUpdate,
         sortable: true,
      },
      {
         name: "Last Prac Role Update",
         selector: (row: { LastPracRoleUpdate: any }) => row.LastPracRoleUpdate,
         sortable: true,
      },
      {
         name: "Last Location Update",
         selector: (row: { LastLocationUpdate: any }) => row.LastLocationUpdate,
         sortable: true,
      },
      {
         name: "Accuracy Score",
         selector: (row: { AccuracyScore: any }) => row.AccuracyScore,
         sortable: true,
      },
   ];

   return (
      <div className="h-full w-full bg-slate-300">
         <h1>FHIR API</h1>
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
               <button className="button" type="button" onClick={handleClear}>
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
      </div>
   );
}
