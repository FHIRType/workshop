import { Selection } from "./types";

export const menus: Selection[] = [
   {
      name: "GET/ getdata",
      type: "get/getdata",
      baseURL: "http://127.0.0.1:5000/api/getdata",
   },
   {
      name: "POST/ getdata",
      type: "post/getdata",
      baseURL: "http://127.0.0.1:5000/api/getdata",
   },
   {
      name: "GET/ getconsensus",
      type: "get/getconsensus",
      baseURL: "http://127.0.0.1:5000/api/getconsensus",
   },
   {
      name: "POST/ matchdata",
      type: "post/matchdata",
      baseURL: "http://127.0.0.1:5000/api/matchdata",
   },
];
