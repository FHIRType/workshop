import {createBrowserRouter, RouterProvider, ScrollRestoration} from "react-router-dom";
import PostData from "./pages/PostData"
import Home from "./pages/Home";
import {NextUIProvider} from "@nextui-org/react";
import BasicLayout from "./layouts/BasicLayout.tsx";

const router = createBrowserRouter( [
   {
      path: "/",
      element: (
         <>
            <ScrollRestoration />
            <BasicLayout />
         </>
      ),
      errorElement: (
         <div>
            4xx error
         </div>
      ),
      children: [
         {
           path: "/",
           element: <Home />
         },
         {
            path: "/getdata",
            element: <Home />,
         },
         {
            path: "/postdata",
            element: <PostData/>,
         }
      ]
   }
])

export default function App () {
   return (
       <NextUIProvider>
         <RouterProvider router={router} />
       </NextUIProvider>
   );
};