import { TableColumn } from "react-data-table-component";
// import { test_data } from "./types";

// Define columns for the data table
export const columns: TableColumn<any>[] = [
   {
      name: "Endpoint",
      selector: (row: any) => row.Endpoint,
      sortable: true,
   },
   {
      name: "Date Retrieved",
      selector: (row: any) => row.DateRetrieved,
      sortable: true,
   },
   {
      name: "Full Name",
      selector: (row: any) => row.FullName,
      sortable: true,
   },
   { name: "NPI", selector: (row: any) => row.NPI, sortable: true },
   {
      name: "First Name",
      selector: (row: any) => row.FirstName,
      sortable: true,
   },
   {
      name: "Last Name",
      selector: (row: any) => row.LastName,
      sortable: true,
   },
   {
      name: "Gender",
      selector: (row: any) => row.Gender,
      sortable: true,
   },
   {
      name: "Taxonomy",
      selector: (row: any) => row.Taxonomy,
      sortable: true,
   },
   {
      name: "Group Name",
      selector: (row: any) => row.GroupName,
      sortable: true,
   },
   {
      name: "Address 1",
      selector: (row: any) => row.ADD1,
      sortable: true,
   },
   {
      name: "Address 2",
      selector: (row: any) => row.ADD2,
      sortable: true,
   },
   {
      name: "City",
      selector: (row: any) => row.City,
      sortable: true,
   },
   {
      name: "State",
      selector: (row: any) => row.State,
      sortable: true,
   },
   { name: "Zip", selector: (row: any) => row.Zip, sortable: true },
   {
      name: "Phone",
      selector: (row: any) => row.Phone,
      sortable: true,
   },
   { name: "Fax", selector: (row: any) => row.Fax, sortable: true },

   {
      name: "Latitude",
      selector: (row: any) => row.lat,
      sortable: true,
   },
   {
      name: "Longitude",
      selector: (row: any) => row.lng,
      sortable: true,
   },
   {
      name: "Last Prac Update",
      selector: (row: any) => row.LastPracUpdate,
      sortable: true,
   },
   {
      name: "Last Prac Role Update",
      selector: (row: any) => row.LastPracRoleUpdate,
      sortable: true,
   },
   {
      name: "Last Location Update",
      selector: (row: any) => row.LastLocationUpdate,
      sortable: true,
   },
   {
      name: "Accuracy",
      selector: (row: any) => row.Accuracy,
      sortable: true,
   },
];
