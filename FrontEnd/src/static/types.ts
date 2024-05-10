export type test_data = {
   Endpoint: "string";
   DateRetrieved: "string";
   FullName: "string";
   NPI: "string";
   FirstName: "string";
   LastName: "string";
   Gender: "string";
   Taxonomy: "string";
   GroupName: "string";
   ADD1: "string";
   ADD2: "string";
   City: "string";
   State: "string";
   Zip: "string";
   Phone: "string";
   Fax: "string";
   Email: "string";
   lat: "string";
   lng: "string";
   LastPracUpdate: "string";
   LastPracRoleUpdate: "string";
   LastLocationUpdate: "string";
   Accuracy: 0;
};

export type SelectionType = {
   name: string;
   type: string;
   baseURL: string;
   pageURL: string;
   description: string[];
};

export type PractitionerType = {
   npi: string;
   first_name: string;
   last_name: string;
};

export type GetDataFormProps = {
   data: {
      practitioners: PractitionerType[];
      endpoint: string;
      consensus: string;
   };
};

export const formPropInit = {
   practitioners: [
      {
         first_name: "",
         last_name: "",
         npi: "",
      },
   ],
   endpoint: "All",
   consensus: "True",
};

export type QueryProps = {
   practitioners: PractitionerType[];
};

export const queryPropInit = {
   practitioners: [
      {
         npi: "",
         first_name: "",
         last_name: "",
      },
   ],
};

// visibleTable boolean
// Define the type for visibleTables
export type VisibleTablesProps = {
   [key: string]: boolean;
};
