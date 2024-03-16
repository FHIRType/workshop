// import { DataColumn } from "react-data-table-component";
// import { test_data } from "./types";

// Define columns for the data table
// export const columns: DataColumn<test_data>[] = [
export const columns = [
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
