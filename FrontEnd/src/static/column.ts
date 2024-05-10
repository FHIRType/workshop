import { TableColumn } from "react-data-table-component";

interface Practitioner {
   Endpoint: string;
   DateRetrieved: string;
   FullName: string;
   NPI: string;
   FirstName: string;
   LastName: string;
   Gender: string;
   Taxonomy: string;
   GroupName: string;
   ADD1: string;
   ADD2: string;
   City: string;
   State: string;
   Zip: string;
   Phone: string;
   Fax: string;
   lat: number;
   lng: number;
   LastPracUpdate: string;
   LastPracRoleUpdate: string;
   LastLocationUpdate: string;
   Accuracy: string;
}

// Define columns for the data table
export const columns: TableColumn<Practitioner>[] = [
   {
      name: "Endpoint",
      selector: row => row.Endpoint,
      sortable: true,
   },
   {
      name: "Date Retrieved",
      selector: row => row.DateRetrieved,
      sortable: true,
   },
   {
      name: "Full Name",
      selector: row => row.FullName,
      sortable: true,
   },
   { name: "NPI", selector: row => row.NPI, sortable: true },
   {
      name: "First Name",
      selector: row => row.FirstName,
      sortable: true,
   },
   {
      name: "Last Name",
      selector: row => row.LastName,
      sortable: true,
   },
   {
      name: "Gender",
      selector: row => row.Gender,
      sortable: true,
   },
   {
      name: "Taxonomy",
      selector: row => row.Taxonomy,
      sortable: true,
   },
   {
      name: "Group Name",
      selector: row => row.GroupName,
      sortable: true,
   },
   {
      name: "Address 1",
      selector: row => row.ADD1,
      sortable: true,
   },
   {
      name: "Address 2",
      selector: row => row.ADD2,
      sortable: true,
   },
   {
      name: "City",
      selector: row => row.City,
      sortable: true,
   },
   {
      name: "State",
      selector: row => row.State,
      sortable: true,
   },
   { name: "Zip", selector: row => row.Zip, sortable: true },
   {
      name: "Phone",
      selector: row => row.Phone,
      sortable: true,
   },
   { name: "Fax", selector: row => row.Fax, sortable: true },

   {
      name: "Latitude",
      selector: row => row.lat,
      sortable: true,
   },
   {
      name: "Longitude",
      selector: row => row.lng,
      sortable: true,
   },
   {
      name: "Last Prac Update",
      selector: row => row.LastPracUpdate,
      sortable: true,
   },
   {
      name: "Last Prac Role Update",
      selector: row => row.LastPracRoleUpdate,
      sortable: true,
   },
   {
      name: "Last Location Update",
      selector: row => row.LastLocationUpdate,
      sortable: true,
   },
   {
      name: "Accuracy",
      selector: row => row.Accuracy,
      sortable: true,
   },
];
