import { SelectionType } from "./types";

export const menus: SelectionType[] = [
   {
      name: "GET/ getdata",
      type: "get/getdata",
      baseURL: "http://127.0.0.1:5000/api/getdata",
      pageURL: "/getdata",
      description: [
         "Retrieve data from all endpoints or specified endpoints.",
         "Given a first name, last name, and NPI the routes retrieve data from all endpoints or specified endpoints.",
         "This will return data as JSON, a file, or web page based on their queries.",
         "Optionally it could contain an attribute to limit or specify the endpoints used to gather data.",
      ],
   },
   {
      name: "POST/ getdata",
      type: "post/getdata",
      baseURL: "http://127.0.0.1:5000/api/getdata",
      pageURL: "/postdata",
      description: [
         "Retrieve data from all endpoints or specified endpoints.",
         "Given a first name, last name, and NPI returns list of standard objects indexed by NPI number.",
         "This will return data as JSON, a file, or web page based on their queries.",
         "Replace npi to real value, and fill out the body. Format can be null. (options = page, file)",
      ],
   },
   {
      name: "GET/ getconsensus",
      type: "get/getconsensus",
      baseURL: "http://127.0.0.1:5000/api/getconsensus",
      pageURL: "/getconsensus",
      description: [
         "Given a group of matched records, return those records with a consensus result and an accuracy score built in.",
      ],
   },
   {
      name: "POST/ matchdata",
      type: "post/matchdata",
      baseURL: "http://127.0.0.1:5000/api/matchdata",
      pageURL: "/matchdata",
      description: [
         "Given a list of JSON of flattened data, the service should attempt to match records and return all records as list of lists.",
      ],
   },
];