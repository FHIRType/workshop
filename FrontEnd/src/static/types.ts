import React from "react";

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

export type GetDataFormProps = {
   data: {
      practitioners: [
         {
            firstName: string;
            lastName: string;
            npi: string;
         }
      ],
      endpoint: string;
      consensus: string;
   }
   setData: (data: any) => void;  // Generic type can be replaced with more specific function type
   handleSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
   handleClear: () => void;
}

export const formPropInit = {
   practitioners: [
      {
         firstName: "",
         lastName: "",
         npi: ""
      }
   ],
   endpoint: "All",
   consensus: "False"
}

export type QueryProp =  {
   "practitioners": [
      {
         npi: string;
         first_name: string;
         last_name: string;
      }
   ]
}

export const queryPropInit = {
   "practitioners": [
      {
         npi: "",
         first_name: "",
         last_name: ""
      }
   ]
}

// visibleTable boolean
// Define the type for visibleTables
export type VisibleTablesProps = {
   [key: string]: boolean;
}