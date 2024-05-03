import { FormEvent, useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import DataTable from "react-data-table-component";
import GetDataForm from "../components/GetData/Form";
import FileForm from "../components/FileForm.tsx";
import { IoIosArrowDown, IoIosArrowUp } from "react-icons/io";
import { Button } from "@nextui-org/react";
import { cn } from "../utils/tailwind-utils.ts";
import { conditionalRowStyles } from "../static/endpointColors";
import {
   GetDataFormProps,
   QueryProps,
   formPropInit,
   queryPropInit,
   VisibleTablesProps,
} from "../static/types.ts";
import { columns } from "../static/column.ts";
import JSONForm from "../components/JSONForm.tsx";

export default function Home() {
    const [formData, setFormData] = useState<GetDataFormProps['data']>(formPropInit);
    const [queryBody, setQueryBody] = useState<QueryProp>(queryPropInit);
    const [formVisible, setFormVisible] = useState<boolean>(true);
    const [fileVisible, setFileVisible] = useState<boolean>(false);
    const [jsonVisible, setJsonVisible] = useState<boolean>(false);
    const [visibleTables, setVisibleTables] = useState({});
    const [query, setQuery] = useState<boolean>(false);

   const toggleTableVisibility = (key: string) => {
      setVisibleTables((prevState) => ({
         ...prevState,
         [key]: !prevState[key], // Toggle the visibility
      }));
   };

   const baseUrl = import.meta.env.VITE_API_BASE_URL;

   const { isLoading, error, data, refetch } = useQuery({
      queryKey: ["searchPractitioner", queryBody, formData.endpoint, formData],
      queryFn: async () => {
         const response = await fetch(
            `${baseUrl}?endpoint=${formData.endpoint}&format=JSON&consensus=${formData.consensus}`,
            {
               method: "POST",
               headers: {
                  "Content-Type": "application/json",
               },
               body: JSON.stringify(queryBody),
            }
         );

         if (!response.ok) {
            throw new Error("Failed to fetch data");
         }
         const returned = await response.json();
         setQuery(false);
         return returned;
      },
      enabled: false, // Disable automatic fetching
   });

   const handleSubmit = (e: FormEvent) => {
      e.preventDefault();
      const updatedPractitioners = formData.practitioners.map((prac) => ({
         npi: prac.npi,
         first_name: prac.first_name,
         last_name: prac.last_name,
      }));

      // Update the queryBody state
      setQueryBody({ practitioners: updatedPractitioners });
      setQuery(true);
   };

   useEffect(() => {
      if (query) {
         refetch().catch((err) => console.error("Error fetching data: ", err));
      }
   }, [queryBody]);

   const handleClear = () => setFormData(formPropInit);

   const handleToggleForm = () => {
      setFormVisible(true);
      setFileVisible(false);
      setJsonVisible(false);
   };

   const handleToggleFile = () => {
      setFormVisible(false);
      setFileVisible(true);
      setJsonVisible(false);
   };

   const handleToggleJson = () => {
      setFormVisible(false);
      setFileVisible(false);
      setJsonVisible(true);
   };

   const handleSubmitCSV = (jsonData: GetDataFormProps["data"]) => {
      setQueryBody(jsonData); // Update queryBody state with parsed CSV data
      setQuery(true); // Trigger refetch to fetch practitioners based on the parsed CSV data
   };

   return (
      <div className="p-5 bg-neutral-100">
         <div className="flex flex-col">
            <h1
               className={
                  "text-[calc(1.5vw+2em)] text-center select-none text-pacific-blue font-semibold"
               }
            >
               Find your doctors!
            </h1>
            <div
               className={
                  "text-[calc(1.3vw+0.5em)] text-center mb-6 select-none text-pacific-blue opacity-80"
               }
            >
               Search. Find. Connect. Simplifying your path to healthcare.
            </div>
            <div className="self-center">
               <div className={"flex gap-3"}>
                  <button
                     className={cn(
                        `ml-2 w-[calc(5vw+2em)] min-w-[80px] bg-pacific-light-blue text-white transition ease-in-out`,
                        {
                           "bg-pacific-blue": formVisible,
                        }
                     )}
                     onClick={handleToggleForm}
                  >
                     Form
                  </button>
                  <button
                     className={cn(
                        `px-4 py-2 w-[calc(5vw+2em)] bg-pacific-light-blue text-white min-w-[80px] transition ease-in-out`,
                        {
                           "bg-pacific-blue": fileVisible,
                        }
                     )}
                     onClick={handleToggleFile}
                  >
                     File
                  </button>
                  <button
                     className={cn(
                        `px-4 py-2 w-[calc(5vw+2em)] bg-pacific-light-blue text-white min-w-[80px] transition ease-in-out`,
                        {
                           "bg-pacific-blue": jsonVisible,
                        }
                     )}
                     onClick={handleToggleJson}
                  >
                     JSON
                  </button>
               </div>

               {formVisible && (
                  <GetDataForm
                     data={formData}
                     setFormData={setFormData}
                     handleSubmit={handleSubmit}
                     handleClear={handleClear}
                     isLoading={isLoading}
                  />
               )}

                {fileVisible &&
                    <FileForm
                        setQueryBody={handleSubmitCSV}
                    />
                }
                {jsonVisible &&
                    <JSONForm />
                }
            </div>

            <div className="w-[85%] mt-10 rounded-[5px] mx-auto">
               {error && <div>Error: {error.message}</div>}
               {data &&
                  Object.keys(data).map((key, index) => {
                     const isVisible = visibleTables[key] || false;
                     return (
                        <div key={index + key}>
                           <div className={"flex justify-between my-2"}>
                              <h2 className={"font-bold text-[calc(1vw+1em)]"}>
                                 {data[key][0]["FullName"]}
                              </h2>
                              <Button
                                 isIconOnly
                                 aria-label="Expand/Contract"
                                 color={"danger"}
                                 className="rounded-full bg-pacific-blue"
                                 onClick={() => toggleTableVisibility(key)}
                              >
                                 {!isVisible ? (
                                    <IoIosArrowDown />
                                 ) : (
                                    <IoIosArrowUp />
                                 )}
                              </Button>
                           </div>
                           {!isVisible && (
                              <DataTable
                                 columns={columns}
                                 data={data[key]}
                                 pagination
                                 conditionalRowStyles={conditionalRowStyles}
                                 key={index + key}
                              />
                           )}
                           <div
                              className={
                                 "w-full h-[2px] rounded-[10px] bg-pacific-light-blue my-5"
                              }
                           >
                              .
                           </div>
                        </div>
                     );
                  })}
            </div>
         </div>
      </div>
   );
}
