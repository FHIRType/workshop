import Header from "./components/Header";
import {createBrowserRouter, RouterProvider, ScrollRestoration} from "react-router-dom";
import GetData from "./pages/GetData";

const router = createBrowserRouter( [
   {
      path: "/",
      element: [
         <>
            <ScrollRestoration />
            <Header />
         </>
      ],
      errorElement: [
         <div>
            4xx error
         </div>
      ],
      children: [
         {
            path: "/getdata",
            element: <GetData />,
         },
      ]
   }
])

export default function App () {
   return (
       <RouterProvider router={router} />
   );
};